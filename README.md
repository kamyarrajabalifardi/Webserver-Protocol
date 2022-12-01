# Webserver-Protocol
The goal of this project is to implement a functional HTTP server and client system. Clients and servers
communicate by exchanging individual messages (as opposed to a stream of data). The messages sent by
the client, usually a Web browser, are called requests, and the messages sent by the server as an answer are
called responses. Some HTTP protocols that are implemented in this project are as follows:
`GET`, `POST`, `PUT`, `HEAD`, `DELETE` (Mostly `GET` and `POST`), and detecting errors such as `405` (Method Not Allowed) and `501` (Not Implemented).

Additionally, information of the connections between server and clients is stored in .json files. 


Web Server
----------
In this part, we built a web server and then connect to this web server with our browser!
After running the `serverWEB.py` code, a butterfly is plotted by typing `"http://localhost:YOUR_PORT"` in the browser.
