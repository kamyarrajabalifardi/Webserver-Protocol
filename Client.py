import socket
import os
import datetime

def msg_checker(a_string):
    if a_string == 'Ready to receive':                      # Used for handshakes
        return ('-1' ,-1, 'POST')
    
    b = a_string.split('\n')                                # divide string to lines
    first_line = b[0]
    state = first_line.split(' ')[2]                        # state of message
    if state == 'OK':
        type_of_file = b[-2].split(': ')[1].split('/')[1]
        #size_of_file = int(b[-3].split(': ')[1])
        return (type_of_file , int(b[-3].split(': ')[1]), 'GET')
    return('-1', -1, '-1')

PORT = 5050
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = '!DISCONNECT'
SERVER = '192.168.56.1'
ADDR = (SERVER, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)


def get(Method, version, HOST, Language, path):
# sending get messages
    msg = Method + ' ' + path + ' HTTP/' + version + '\n' + 'HOST: ' + HOST + '\n' + 'Accept-Language: ' + Language

    f = open('Client\\file_names.txt', 'w') # open a file to save the name and URL
    Client_path = 'Client\\' + path.split('\\')[-1]
    f.write(Client_path)
    f.close()
    
    return msg


def post(Method, version, HOST, Language, Forbidden, Name_of_file, Client_path):
    request_time = str(datetime.datetime.now())             # fetch now time
    type_of_file = os.path.splitext(Client_path)[1][1::]    #  fetch type of file
    if type_of_file == 'jpg' or type_of_file == 'png':
        type_of_file = 'image/' + type_of_file
    else:
        type_of_file = 'text/' + type_of_file               # add proper string to the type of file
    
    f = open('Client\\file_names.txt', 'w')
    f.write(Client_path)
    f.close()
    length_of_file = os.path.getsize(Client_path)           # extract the length of file
    if Forbidden == False:                                  # the body is valid
        msg = Method + ' ' + Name_of_file + ' ' + 'HTTP/' + version + '\n'    +\
          'HOST: ' + HOST + '\n'                                              +\
          'Accept-Language: ' + Language + '\n'                               +\
          'Content-Length: ' +  str(length_of_file) + '\n'                    +\
          'Content-Type: ' + type_of_file    + '\n'                           +\
          'Date: ' + request_time
        return msg

    if Forbidden == True:                                   # the body is invalid
        msg = Method + ' ' + Name_of_file + ' ' + 'HTTP/' + version + '\n'    +\
          'HOST: ' + HOST + '\n'                                              +\
          'Accept-Language: ' + Language + '\n'                               +\
          'Content-Length: ' +  str(length_of_file) + '\n'                    +\
          'Content-Type: ' + type_of_file    + '\n'                           +\
          'Date: ' + request_time + '\n\n'                                    +\
          '<html><body><h1>FORBIDDEN!</h1></body></html>'
        return msg

def send(msg):
    message = msg.encode(FORMAT)
    client.send(message)                                         # sending message
    response = client.recv(2048).decode(FORMAT)                  # receiving message
    
    print(response)
    (type_of_file, size_of_file, Method) = msg_checker(response) # analyze the received message

    
    if type_of_file != '-1' and Method == 'GET':                    #get file
####################################### Handshaking Protocol ##################################################
        client.send('Ready to receive'.encode(FORMAT))              # ready to receive
        
        f = open('Client\\file_names.txt', 'r')
        Client_path = f.read()                                      # fetch the address of file
        f.close()
        os.remove('Client\\file_names.txt')

        f = open(Client_path, 'wb')
        data = client.recv(size_of_file)                            # receiving data
        f.write(data)
        f.close()
        return
    
    if type_of_file == '-1' and Method == 'POST':                   # post file
####################################### Handshaking Protocol ##################################################
        length_of_file = msg.split('\n')[-3].split(': ')[1]         # fetch length of file

        f = open('Client\\file_names.txt','r')
        Client_path = f.read()
        f.close()
        os.remove('Client\\file_names.txt')

        f = open(Client_path, 'rb')
        data = f.read(int(length_of_file))
        client.send(data)                                           # sending data
        f.close()
        response = client.recv(2048).decode(FORMAT)                 # receive 200 ok message
        print(response)        
        
send(post('POST', '1.1', 'developer.mozilla.org', 'fr', False, 'jungle', 'Client\\jungle.png'))
send(get('HEAD', '1.0', 'developer.mozilla.org', 'fr','Server\\postfile.txt'))
send(get('METHOD ', '1.6', 'developer.mozilla.org', 'fr','Server\\postfile.txt'))


#send('number of connected clients')        



#send(get('Server\\kambiz.'))
#send('request stats')
#send('number of connected clients')
#send('file type stats')
#send('disconnect')