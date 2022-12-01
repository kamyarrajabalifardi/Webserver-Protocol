# Webserver-Protocol
The goal of this project is to implement a functional HTTP server and client system. Clients and servers
communicate by exchanging individual messages (as opposed to a stream of data). The messages sent by
the client, usually a Web browser, are called requests, and the messages sent by the server as an answer are
called responses. Some HTTP protocols that are implemented in this project are as follows:
`GET`, `POST`, `PUT`, `HEAD`, `DELETE` (Mostly `GET` and `POST`), and detecting errors such as `405` (Method Not Allowed) and `501` (Not Implemented).

Additionally, information of the connections between server and clients is stored in .json files. 

Telnet
------
In this section, we are going to connect to the HTTP server via Telnet. The server
waits for a connection on its port and we connect to it using Telnet Protocol.
To connect to a Server with a specific IP and port number, we enter the following command in the terminal:


> telnet <server_ip> <server_port>


After entering the aforementioned command, we can send some requests and the server should send an appropriate response for each request. The server handles these commands:

**Note:** This section should be executed in Linux terminal.

Web Server
----------
In this part, we built a web server and then connect to this web server with our browser!
After running the `ServerWEB.py` code, a butterfly is plotted by typing `"http://localhost:YOUR_PORT"` in the browser.
