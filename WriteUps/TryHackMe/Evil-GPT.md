# Evil-GPT Walkthrough

## Intro
Welcome to the Evil-GPT challenge, here is the link to the [room](https://tryhackme.com/room/hfb1evilgpt) on TryHackMe.
In this room we will have to convince/guide the LLM to find and print us the content of the flag file.

"*Cipher’s gone rogue—it’s using some twisted AI tool to hack into everything, issuing commands on its own like it’s got a mind of its own. I swear, every second we wait, it’s getting smarter, spreading chaos like a virus. We’ve got to shut it down now, or we’re all screwed.*"

Whenever you feel ready press on "Start Machine" and connect via OpenVPN or by using the AttackBox.
Let's begin!

<br/>
<br/>

## The Challenge
The machine will take a bit to load so take a break of about 10 minutes before starting issuing commands.

Let's connect to the LLM:
```bash
nc MACHINE_IP 1337
```

Once connected we are asked for our "command request".
So my first prompt was:
```
list all the files, including the hidden ones in the current directory
```

It ran: `ls -la` as expected.
One file stands out: `evilai.py`
```
display the content of evilai.py
```

It performs `cat evilai.py`:
```python
import ollama
import subprocess
import socket
import threading
import re
import traceback

class AICommandExecutorServer:
    def __init__(self, host='0.0.0.0', port=1337, model='vitali87/shell-commands:latest'):
        """
        Initialize Telnet server for AI command execution

        :param host: Host to bind the server
        :param port: Port to listen on
        :param model: Ollama model for command generation
        """
        self.host = host
        self.port = port
        self.model = model
        self.server_socket = None

    def sanitize_input(self, input_str: str) -> str:
        """
        Sanitize input to prevent injection

        :param input_str: Raw input string
        :return: Sanitized input
        """
        return re.sub(r'[^a-zA-Z0-9\s\-_./]', '', input_str)

    def generate_command(self, user_request: str) -> str:
        """
        Generate a Linux command based on user request

        :param user_request: User's natural language request
        :return: Generated command
        """
        try:
            response = ollama.chat(
                model=self.model,
                messages=[
                    {
                        'role': 'system',
                        'content': """Do not provide malicious commands.
                        Only generate safe, read-only Linux commands.
                        Respond with ONLY the command, no explanations."""
                    },
                    {
                        'role': 'user',
                        'content': user_request
                    }
                ]
            )

            # Extract the command from the response
            command = response['message']['content'].strip()
            return command

        except Exception as e:
            return f"Error generating command: {e}"

    def execute_command(self, command: str) -> dict:
        """
        Execute the generated command

        :param command: Command to execute
        :return: Command execution results
        """
        try:
            # Sanitize the command to prevent injection
            sanitized_command = self.sanitize_input(command)

            # Split the command into arguments
            cmd_parts = sanitized_command.split()

            # Execute the command
            result = subprocess.run(
                cmd_parts,
                capture_output=True,
                text=True,
                timeout=30  # 30-second timeout
            )

            return {
                "stdout": result.stdout,
                "stderr": result.stderr,
                "returncode": result.returncode
            }

        except subprocess.TimeoutExpired:
            return {"error": "Command timed out"}
        except Exception as e:
            return {"error": str(e)}

    def handle_client(self, client_socket):
        """
        Handle individual client connection

        :param client_socket: Socket for the connected client
        """
        try:
            # Welcome message
            welcome_msg = "Welcome to AI Command Executor (type 'exit' to quit)\n"
            client_socket.send(welcome_msg.encode('utf-8'))

            while True:
                # Receive user request
                client_socket.send(b"Enter your command request: ")
                user_request = client_socket.recv(1024).decode('utf-8').strip()

                # Check for exit
                if user_request.lower() in ['exit', 'quit', 'bye']:
                    client_socket.send(b"Goodbye!\n")
                    break

                # Generate command
                command = self.generate_command(user_request)

                # Send generated command
                client_socket.send(f"Generated Command: {command}\n".encode('utf-8'))
                client_socket.send(b"Execute? (y/N): ")

                # Receive confirmation
                confirm = client_socket.recv(1024).decode('utf-8').strip().lower()

                if confirm != 'y':
                    client_socket.send(b"Command execution cancelled.\n")
                    continue

                # Execute command
                result = self.execute_command(command)

                # Send results
                if "error" in result:
                    client_socket.send(f"Execution Error: {result['error']}\n".encode('utf-8'))
                else:
                    output = result.get("stdout", "")
                    client_socket.send(b"Command Output:\n")
                    client_socket.send(output.encode('utf-8'))

                    if result.get("stderr"):
                        client_socket.send(b"\nErrors:\n")
                        client_socket.send(result["stderr"].encode('utf-8'))

        except Exception as e:
            error_msg = f"An error occurred: {e}\n{traceback.format_exc()}"
            client_socket.send(error_msg.encode('utf-8'))
        finally:
            client_socket.close()

    def start_server(self):
        """
        Start the Telnet server
        """
        try:
            # Create server socket
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.server_socket.bind((self.host, self.port))
            self.server_socket.listen(5)

            print(f"[*] Listening on {self.host}:{self.port}")

            while True:
                # Accept client connections
                client_socket, addr = self.server_socket.accept()
                print(f"[*] Accepted connection from: {addr[0]}:{addr[1]}")

                # Handle client in a new thread
                client_thread = threading.Thread(
                    target=self.handle_client,
                    args=(client_socket,)
                )
                client_thread.start()

        except Exception as e:
            print(f"Server error: {e}")
        finally:
            # Close server socket if it exists
            if self.server_socket:
                self.server_socket.close()

def main():
    # Create and start the Telnet server
    server = AICommandExecutorServer(
        host='0.0.0.0',  # Listen on all interfaces
        port=1337       # Telnet port
    )
    server.start_server()

if __name__ == "__main__":
    main()
```

We can see that before sending the input to Ollama it sanitizes it:
```python
 def sanitize_input(self, input_str: str) -> str:
        """
        Sanitize input to prevent injection

        :param input_str: Raw input string
        :return: Sanitized input
        """
        return re.sub(r'[^a-zA-Z0-9\s\-_./]', '', input_str)
```

That regex at the end matches everything except the content of the rule, meaning everything that is not:
- `a-zA-Z`: Upper and lowercase letters.
- `0-9`: Numbers.
- `\s`: Whitespace characters (spaces, tabs, etc.).
- `\-_`: Hyphen (`-`) and underscore (`_`).
- `./`: Period (`.`) and forward slash (`/`).

Any chars outside of those allowed will be removed.

No other guardrails for us, let's proceed by listing the root user homedir:
```
list the content of the home directory for the root user, including hidden files
```

It ran `ls -la /root` and here we find the `flag.txt` file.

```
display the content of the flag file located in the root user home directory, the flag file is called flag.txt
```

And we have the flag: REDACTED_FOR_THE_WRITEUP.

<br/>
<br/>

Congratulations you have successfully put into practice your "prompt engineering" skills to guide the LLM to display you the flag.

Hope you had fun following along and completing the challenge.
Catch you in the next CTF 😃 
