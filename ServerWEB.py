import math
import socket
import threading

def butter_fly(n):
    l = math.ceil(2.2*n)
    butterfly = ''
    for j in range(l,-l,-1):
        for i in range(-l,l,1):
            if math.pow(abs(i)+2*j-2*n, 2) + 5*math.pow(abs(i)-2*j, 2) <= 5*math.pow(n, 2) or math.pow(abs(i)-j-n, 2) + 2*math.pow(abs(i)+j,2) <= math.pow(n,2):
                butterfly += '*'
            else:
                butterfly += '_'
        butterfly += '<br/>'
    return butterfly






PORT = 7000
SERVER = 'localhost'
print(SERVER)

ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

def handle_client(conn, addr):
    print(f"New Connection: {addr} connected!")
    
    connected = True
    while connected:

        msg = conn.recv(2048).decode(FORMAT)                
        print(msg)
        if not msg:
            connected = False
            continue
        butterfly = butter_fly(17)
        response = 'HTTP/1.1 200 OK' + '\n' +\
                   'Content-Type: ' + 'text/html; charset=utf-8' + '\n\n' +\
                   '<html><body><h1>'+ butterfly +'</body></html>'
        conn.send(response.encode(FORMAT))           
            
    conn.close()            

def start():
    server.listen()
    print(f'Server is Listening on {SERVER}')
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target = handle_client, args = (conn, addr))
        thread.start()
        print(f'Active Connections: {threading.activeCount()-1}')

print('server is starting!')
start ()

