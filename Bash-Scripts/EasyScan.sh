#!/bin/bash

# This is a very simple scanning script for CTFs that combines nmap, gobuster and nikto scans.
# It will also clean and reorganize their results in a report file for you.
# If you are not using the default Kali Linux user or OS you need to change the path for the Wordlist and your username.
# You might also need to change your terminal type on line 20 to correctly open a new term session to install apps if needed.

# Display the script name
figlet -f slant EasyScan | awk -v term_width=$(tput cols) '{printf "%-*s\n", int((term_width-39)/2), $0}' 


# Checking if the required tools are installed
REQUIRED_TOOLS=("nmap" "gobuster" "nikto")
TOOLS_INSTALLED=0

for tool in "${REQUIRED_TOOLS[@]}"; do
        if ! dpkg -l | grep -q "$tool";then
                echo "$tool not found! Do you want to install it? yes/no"
                read CHOICE
                if [ $CHOICE == "yes" ];then 
                        tmux new-session "sudo -E apt install -y $tool"\;  
                        TOOLS_INSTALLED=$((TOOLS_INSTALLED + 1)) 
                        continue
                else
                        echo "Warning: You will not get a complete report"
                        TOOLS_INSTALLED=$((TOOLS_INSTALLED - 1))  
                        continue
                fi
        else 
                TOOLS_INSTALLED=$((TOOLS_INSTALLED + 1))
                continue
        fi
done

if [ $TOOLS_INSTALLED -ge 3 ];then 
        echo -e "\n\nAll required tools are installed.\n\n"
else 
        echo "You are still missing some tools"
fi

# Creating the directories for our investigations
mkdir /home/kali/Documents/Scans 2>/dev/null
mkdir /home/kali/Documents/Scans/nmap 2>/dev/null
mkdir /home/kali/Documents/Scans/gobuster 2>/dev/null
mkdir /home/kali/Documents/Scans/nikto 2>/dev/null
mkdir /home/kali/Documents/Scans/Reports 2>/dev/null


# Loop that ask for the domain to scan and creates a report of the findings
INPUT="BLANK"
PORT="BLANK"
while [ $INPUT != "quit" ];do 

        # Add the IP to the hosts file
        echo "Hey before starting let's add the IP address to the hosts file" 
        echo "Insert the IP: " 
        read INPUT 
        echo "Nice now provide the domain name" 
        read DOMAIN 

        FOR_HOSTS_FILE="$INPUT $DOMAIN" 
        echo "You entered: $FOR_HOSTS_FILE" 

        sudo zsh -c "echo '$FOR_HOSTS_FILE' >> /etc/hosts" 

        # Scanning for open ports, hidden directories, subdomains and virtual hosts
   
                
        echo "Starting the nmap scan "sV mode", chose 1 to scan common ports or 2 to scan all ports" 
        read MODE 

        if [ $MODE -eq 1 ];then
        sudo nmap -sV -vv $INPUT | pv -l -s $(sudo nmap -sV -vv $INPUT | grep -c 'Nmap scan report for') > /home/kali/Documents/Scans/nmap/nmap_scan_$INPUT.txt
        fi
        if [ $MODE -eq 2 ];then
        sudo nmap -sV -vv -p- $INPUT | pv -l -s $(sudo nmap -sV -vv $INPUT | grep -c 'Nmap scan report for') > /home/kali/Documents/Scans/nmap/nmap_scan_$INPUT.txt
        fi

        EXTRACT_PORTS=$(cat /home/kali/Documents/Scans/nmap/nmap_scan_$INPUT.txt | grep -E 'open  (http|ssl/http)')
        HTTP_PORTS=($(echo "$EXTRACT_PORTS" |  grep -E 'open  http' | cut -d' ' -f1 | cut -d'/' -f1))
        HTTPS_PORTS=($(echo "$EXTRACT_PORTS" | grep -E 'open  ssl/http' | cut -d' ' -f1 | cut -d'/' -f1))
        echo $HTTP_PORTS
        echo $HTTPS_PORTS

        # Looping through each http port
        for PORT in "${HTTP_PORTS[@]}"; do
                echo $PORT
                gobuster dir -u http://$INPUT:$PORT/ -w /usr/share/wordlists/dirb/common.txt -t 50 | sed '1,13d'  >> /home/kali/Documents/Scans/gobuster/gobuster_scan_$INPUT.txt
                gobuster dns -d $DOMAIN -w /usr/share/wordlists/seclists/Discovery/DNS/subdomains-top1million-5000.txt -t 50 | sed  '1,10d'  >> /home/kali/Documents/Scans/gobuster/gobuster_scan_$INPUT.txt
                gobuster vhost -u http://$DOMAIN -w /usr/share/wordlists/seclists/Discovery/DNS/subdomains-top1million-5000.txt -t 50 --append-domain | sed '1,13d' >> /home/kali/Documents/Scans/gobuster/gobuster_scan_$INPUT.txt
                #nikto -h http://$INPUT -o /home/kali/Documents/Scans/nikto/nikto_scan_$INPUT.txt
        done

        # Looping through each https port and skip tsl validation
        for PORT in "${HTTPS_PORTS[@]}"; do
                echo $PORT
                gobuster dir -u https://$INPUT:$PORT/ -w /usr/share/wordlists/dirb/common.txt -t 50 -k | sed '1,13d' >> /home/kali/Documents/Scans/gobuster/gobuster_scan_$INPUT.txt
                gobuster dns -d $DOMAIN -w /usr/share/wordlists/seclists/Discovery/DNS/subdomains-top1million-5000.txt -t 50 | sed  '1,10d'  >> /home/kali/Documents/Scans/gobuster/gobuster_scan_$INPUT.txt
                gobuster vhost -u https://$DOMAIN -w /usr/share/wordlists/seclists/Discovery/DNS/subdomains-top1million-5000.txt -t 50 --append-domain -k | sed '1,13d' >> /home/kali/Documents/Scans/gobuster/gobuster_scan_$INPUT.txt
                #nikto -h http://$INPUT -o /home/kali/Documents/Scans/nikto/nikto_scan_$INPUT.txt
        done



        # cleaning nmap report
        echo "# NMAP SCAN" >> /home/kali/Documents/Scans/Reports/report_$INPUT.txt 
        # Input file
        input_file=/home/kali/Documents/Scans/nmap/nmap_scan_$INPUT.txt 

        # Find the line that starts with "PORT"
        port_line=$(grep -n "^PORT" "$input_file" | head -n 1 | cut -d ":" -f 1) 

        # Find the line that starts with "Service Info"
        service_info_line=$(grep -n "^Service Info" "$input_file" | head -n 1 | cut -d ":" -f 1) 

        # Find the line that starts with "SF:"
        sf_line=$(grep -n "^SF:" "$input_file" | head -n 1 | cut -d ":" -f 1) 

        # If there is a line starting with "SF:", subtract 1 from the line number
        if [ -n "$sf_line" ]; then
        sf_line=$((sf_line - 1))
        fi

        # Print the lines between the two found lines, excluding the lines starting with "SF:"
        sed -n "$((port_line+1)),$((sf_line-1))p" "$input_file" | grep -v "^SF:" >> /home/kali/Documents/Scans/Reports/report_$INPUT.txt 


        # Addinf the gobuster scans
        echo -e "\n\n# DIRECTORY SCAN" >> /home/kali/Documents/Scans/Reports/report_$INPUT.txt 
        cat /home/kali/Documents/Scans/gobuster/gobuster_scan_$INPUT.txt >> /home/kali/Documents/Scans/Reports/report_$INPUT.txt 

        # adding nikto scan result 
        #echo -e "\n\n# VULNERABILITY SCAN" >> /home/kali/Documents/Scans/Reports/report_$INPUT.txt 
        #cat /home/kali/Documents/Scans/nikto/nikto_scan_$INPUT.txt >> /home/kali/Documents/Scans/Reports/report_$INPUT.txt 

        echo -e "\n Here is what has been found:" 
        echo -e "\n---------------------------------------------------\n" 
        cat /home/kali/Documents/Scans/Reports/report_$INPUT.txt 

        echo -e "\n\n The scan has been completed, I am ready for another one, if you want to exit write 'quit'\n\n" 
done

echo "bye"
