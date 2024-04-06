#!/bin/bash

# This is a very simple scanning script for CTFs it will combine nmap and gobuster scans.
# It will also clean and reorganize their results in a file for you.
# If you are not using Kali Linux you need to change the path for the Wordlist and your username.

# Creating the directories for our investigations
mkdir /home/kali/Documents/Scans 2>/dev/null
mkdir /home/kali/Documents/Scans/nmap 2>/dev/null
mkdir /home/kali/Documents/Scans/gobuster 2>/dev/null
mkdir /home/kali/Documents/Scans/Reports 2>/dev/null

# Loop that ask for the domain to scan and creates a report of the findings
INPUT="BLANK"
while [ $INPUT != "quit" ];do 
        echo "Enter the domain you want to scan, write quit to exit"
        read INPUT
        if [ $INPUT != "quit" ];then 
                sudo nmap -sV -vv $INPUT > /home/kali/Documents/Scans/nmap/nmap_scan_$INPUT.txt
                gobuster dir -u http://$INPUT/ -w /usr/share/wordlists/dirb/common.txt > /home/kali/Documents/Scans/gobuster/gobuster_scan_$INPUT.txt

                echo "# NMAP SCAN" >> /home/kali/Documents/Scans/Reports/report_$INPUT.txt
                # Input file
                input_file=/home/kali/Documents/Scans/nmap/nmap_scan_$INPUT.txt

                # Find the line that starts with "PORT"
                port_line=$(grep -n "^PORT" "$input_file" | head -n 1 | cut -d ":" -f 1)

                # Find the line that starts with "Service Info"
                service_info_line=$(grep -n "^Service Info" "$input_file" | head -n 1 | cut -d ":" -f 1)

                # Print the lines between the two found lines
                sed -n "$((port_line+1)),$((service_info_line-1))p" "$input_file" >> /home/kali/Documents/Scans/Reports/report_$INPUT.txt

                echo -e "\n\n# DIRECTORY SCAN" >> /home/kali/Documents/Scans/Reports/report_$INPUT.txt
                sed '1,13d' /home/kali/Documents/Scans/gobuster/gobuster_scan_$INPUT.txt >> /home/kali/Documents/Scans/Reports/report_$INPUT.txt
                echo -e "\n Here is what has been found:"
                echo -e "\n---------------------------------------------------\n"
                cat /home/kali/Documents/Scans/Reports/report_$INPUT.txt

        fi
 done
