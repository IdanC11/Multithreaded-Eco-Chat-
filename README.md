# Multithreaded Eco Chat
The Eco Chat Room is a simple chat application that allows clients to communicate with a server.
It supports basic commands such as sending messages, retrieving server information, and disconnecting from the server.

## Features

* Server-Client architecture for communication
* Support for multiple simultaneous client connections
* Command-based communication with the server
* Commands:
  
  * QUIT: Disconnects the client from the server (requires a password)
  * TIME: Retrieves the current time from the server
  * WHRU: Retrieves the server's name
  * MAC: Retrieves the server's MAC address
  * CLIENTS NUM: Retrieves the number of clients connected to the server

## Prerequisites
Python 3.x


## Getting Started
### Clone the repository in shell:

git clone [<[repository-url](https://github.com/IdanC11/Multithreaded-Eco-Chat-)>]

### Run the server in shell:

python server.py

### Run the client in shell:

python client.py

Enter messages in the client's GUI and press Send to communicate with the server.

## Usage
* Server:
  * The server is responsible for handling client connections and processing commands.
  * It listens on a specified host and port for incoming connections.
  * Clients can connect to the server and send commands for processing.
  * The server will respond to commands accordingly and relay messages between clients.
  * The server supports a maximum number of concurrent client connections.
* Client:
  * The client is a graphical user interface (GUI) application.
  * It connects to the server using the specified host and port.
  * The client can enter messages in the input field and send them to the server.
  * The server's responses and other clients' messages are displayed in the chat log.

## Notes
* The server uses a password (default: 12345) for the QUIT command to ensure secure disconnection.
* The server provides additional commands to retrieve server information such as time, server name, MAC address, and the number of connected clients.
* The client communicates with the server using a TCP/IP socket connection.
* The client GUI is implemented using the Tkinter library.
