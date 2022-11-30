import socket
import threading
import os.path
import time
import datetime
import json



def stat_HTTP_disconnect(a_string):
#This function checks the type of the message. The types are written below:
# 1. stat : asks for statistical information of transmissions
# 2. disconnect : in order to stop the session
# 3. HTTP : Messages based on http protocol
    if a_string == 'number of connected clients' or a_string == 'file type stats' or a_string == 'request stats' or a_string =='response stats':                          
        return 'stat'
    
    if a_string == 'disconnect':
        return 'disconnect'
    
    else:
        return 'HTTP'

def stat_msg(a_string):
# This function executes statistical messages and send json's data files to the client

    if a_string == 'number of connected clients':
        return 'number of connected clients : ' + str(int(threading.activeCount()-1)) + '\n'
        
    if a_string == 'file type stats':
        try:
            response = JSON_TO_STRING("JSON_FILE_TYPE_STAT.json")
            return response                             
        except:  #if there was no file existed
            response = 'image/jpg : 0\n' +\
                        'text/txt : 0\n' +\
                       'image/png : 0\n' +\
                       'text/html : 0' 
            return response           
    
    if a_string == 'request stats':
        try:
            response = JSON_TO_STRING("JSON_REQUEST_STAT.json")
            return response                             
        except:  #if there was no file existed
            response = 'GET : 0\n'      +\
                       'PUT : 0\n'      +\
                       'POST : 0\n'     +\
                       'DELETE : 0\n'   +\
                       'HEAD : 0\n'     +\
                       'Improper : 0'    
            return response           
     
    if a_string == 'response stats':
        try:
            response = JSON_TO_STRING("JSON_RESPONSE_STAT.json")                             
            return response
        except:  #if there was no file existed
            response = '400 : 0\n'      +\
                       '501 : 0\n'      +\
                       '405 : 0\n'      +\
                       '200 : 0\n'      +\
                       '301 : 0\n'      +\
                       '403 : 0'    
            return response           


def string_with_calculated_length(a_string):
# This function calculates the length of the messages sent by server to client to inform
# the invalidity of the received message.
        location_of_length = 2                                      # location of length number
        length_of_string = len(a_string)                            # length of string without length_number
        length_of_the_length_of_string = len(str(length_of_string))
        length_of_string += int(length_of_the_length_of_string)     # length of string with length_number
        lines_of_string = a_string.split('\n')
        lines_of_string[location_of_length] += str(length_of_string)
        return '\n'.join(lines_of_string)                           # convert list to string

                
def HTTP_msg(a_string, addr):
# This function creates proper response to the received message.
    lines_of_string = a_string.split('\n')                          # spilt string in to lines
    body_loc = -1                                                   # location of statring body part of the message
    for i in range(0,len(lines_of_string)):
        if lines_of_string[i] == '':
            break
        body_loc = i                                                # location of body found!
        
    if body_loc == -1:                                              # if the message has no body part
        b = lines_of_string[0::]     
    else:                                                           # if the message consists of body part
        b = lines_of_string[0:body_loc+1]
        
    first_line = b[0].split(' ')                                    # extract first line
    flag = 0
    
    for i in range(1,len(b)):                                       # to check if ': ' is used properly
        temp = b[i].split(': ')
        if len(temp) == 2:
            continue
        flag = 1
        break

    # 400 bad request
    version = first_line[-1].split('/')[-1]                         # extract version of http protocol
    HTTP_versions = ['1.0', '1.1']
    if flag == 1 or len(first_line) != 3 or HTTP_versions.count(version) == 0:
        request_time = str(datetime.datetime.now())
        msg = 'HTTP/1.0 400 Bad Request\n'                                                              +\
              'Connetion: close\n'                                                                      +\
              'Content-Length: '+ '\n'                                                                  +\
              'Content-Type: text/html\n'                                                               +\
              'Date: '+ request_time + '\n\n'                                                           +\
              '<html><body><h1>BADREQUEST!</h1></body></html>'
        msg = string_with_calculated_length(msg)                    # insert length of the message

        # Save the statistical data of this message in JSON files
        JSON_LOG(addr, lines_of_string[0].split(' ')[0], '400 Bad Request', request_time)
        JSON_REQUEST_STAT(a_string.split('\n')[0].split(' ')[0])    
        JSON_RESPONSE_STAT('400')
        
        return ('-1','-1', msg, '-1')

    # 501 Not Implemented
    service_type = ['GET','HEAD','DELETE','POST','PUT']
    if  service_type.count(first_line[0]) == 0:
        request_time = str(datetime.datetime.now())                 # calculate date time
        msg = 'HTTP/1.0 501 Not Implemented\n'                                                          +\
              'Connetion: close\n'                                                                      +\
              'Content-Length: ' + '\n'                                                                 +\
              'Content-Type: text/html\n'                                                               +\
              'Date: ' + request_time  + '\n\n'                                                         +\
              '<html><body><h1>NOTIMPLEMENTED!</h1></body></html>'
        msg = string_with_calculated_length(msg)

        # Save the statistical data of this message in JSON files
        JSON_LOG(addr, lines_of_string[0].split(' ')[0], '501 Not Implemented', request_time)
        JSON_REQUEST_STAT('Improper')
        JSON_RESPONSE_STAT('501')

        #{firstline, length, msg,  method}
        return ('-1','-1', msg, '-1')

     # 405 Method Not Allowed
    method = ['GET','POST']
    if  method.count(first_line[0]) == 0:
        request_time = str(datetime.datetime.now())        
        msg = 'HTTP/1.0 405 Method Not Allowed\n'                                                       +\
              'Connetion: close\nContent-Length: '+ '\n'                                                +\
              'Content-Type: text/html\n'                                                               +\
              'Allow: GET\n'                                                                            +\
              'Date: ' + request_time + '\n\n'                                                          +\
              '<html><body><h1>NOTALLOWED!</h1></body></html>'        
        msg = string_with_calculated_length(msg)

        # Save the statistical data of this message in JSON files
        JSON_LOG(addr, lines_of_string[0].split(' ')[0], '405 Method Not Allowed', request_time)
        JSON_REQUEST_STAT(lines_of_string[0].split(' ')[0])
        JSON_RESPONSE_STAT('405')
       
        return ('-1','-1', msg, '-1')

    # GET 200 OK
    if first_line[0] == 'GET':
        request_time = str(datetime.datetime.now())        
        if os.path.isfile(first_line[1]):                           # check if the file is existed
            type_of_file = os.path.splitext(first_line[1])[1][1::]  # extract type of file
            if type_of_file == 'jpg' or type_of_file == 'png':
                type_of_file = 'image/' + type_of_file
            else:
                type_of_file = 'text/' + type_of_file
                
            length_of_file = os.path.getsize(first_line[1])       
            msg = 'HTTP/1.0 200 OK\n'                                                                  +\
                  'Connetion: close\n'                                                                 +\
                  'Content-Length: '+ str(length_of_file) + '\n'                                       +\
                  'Content-Type: ' + type_of_file + '\n'                                               +\
                  'Date: ' + request_time

            # Save the statistical data of this message in JSON files
            JSON_LOG(addr, lines_of_string[0].split(' ')[0], '200 OK', request_time)
            JSON_FILE_TYPE_STAT(type_of_file)
            JSON_REQUEST_STAT("GET")
            JSON_RESPONSE_STAT('200')

            return (first_line[1], length_of_file, msg, 'GET')

        # 301 Moved Permanently
        else:
            request_time = str(datetime.datetime.now())            
            msg = 'HTTP/1.0 301 Moved Permanently\n'                                                   +\
                  'Connetion: close\n'                                                                 +\
                  'Content-Length: '+ '\n'                                                             +\
                  'Content-Type: text/html\n'                                                          +\
                  'Date: ' + request_time + '\n\n'                                                     +\
                  '<html><body><h1>MOVEDPERMANENTLY!</h1></body></html>'              
            msg = string_with_calculated_length(msg)

            # Save the statistical data of this message in JSON files
            JSON_LOG(addr, lines_of_string[0].split(' ')[0], '301 Moved Permanently', request_time)
            JSON_REQUEST_STAT("GET")
            JSON_RESPONSE_STAT('301')
            
            return ('-1','-1', msg, '-1')

    # HTTP 200 ok
    if first_line[0] == 'POST' and  len(lines_of_string) == body_loc+1:
        type_of_file = lines_of_string[body_loc-1].split(': ')[1].split('/')[1]
        size_of_file = a_string.split('\n')[-3].split(': ')[1]
        msg = 'HTTP/1.0 200 OK' + '\n'                                         +\
              'Connetion: close\nContent-Length: ' + str(len(a_string)) + '\n' +\
              'Content-Type: text/html' + '\n'                                 +\
              'Date: ' + str(datetime.datetime.now()) + '\n\n'                 +\
              '<html><body><h1>POST!</h1></body></html>'

        # Save the statistical data of this message in JSON files
        JSON_REQUEST_STAT("POST")
        JSON_RESPONSE_STAT('200')

        return ('Server\\'+first_line[1]+'.'+ type_of_file, size_of_file, msg, 'POST')
    
    # 403 Forbidden
    if True:
        request_time = str(datetime.datetime.now())        
        msg = 'HTTP/1.0 403 Forbidden\n'                                                               +\
              'Connetion: close\n'                                                                     +\
              'Content-Length: '+ '\n'                                                                 +\
              'Content-Type: text/html\n'                                                              +\
              'Date: ' + request_time + '\n\n'                                                         +\
              '<html><body><h1>FORBIDDEN!</h1></body></html>'
        msg = string_with_calculated_length(msg)

        # Save the statistical data of this message in JSON files
        JSON_LOG(addr, lines_of_string[0].split(' ')[0], '403 Forbidden', request_time)
        JSON_REQUEST_STAT('POST')
        JSON_RESPONSE_STAT('403')
        
        return ('-1', '-1 ', msg, '-1')           


def JSON_LOG(addr, Method, status_message, date_time):
# Create and Update Log json file.
    try: # if file was existed
        if Method != '' or Method != None:
            jsonFile = open("JSON_LOG.json", "r")
            data = json.load(jsonFile)                                                                   # loading json data
            jsonFile.close()
            
            connection_i = str(int(list(data.keys())[-1].split(' ')[-1]) + 1)                            # i^th connection of the server
            data.update({'connection ' + connection_i : [str(addr), Method, status_message, date_time]}) #updating JSON file
            
            jsonFile = open("JSON_LOG.json", "w")
            jsonFile.write(json.dumps(data))
            jsonFile.close()    
    except: # if there were no file
            jsonFile = open("JSON_LOG.json", "w")
            data = {'connection 1' : [str(addr), Method, status_message, date_time]}
            jsonFile.write(json.dumps(data))
            jsonFile.close()
    return 0   
            
def JSON_FILE_TYPE_STAT(type_of_file):
# Count file types
    try:# if file was existed
        jsonFile = open("JSON_FILE_TYPE_STAT.json",'r')
        data = json.load(jsonFile)                                                                      # loading json data
        jsonFile.close()
        
        data[type_of_file] += 1
        
        jsonFile = open("JSON_FILE_TYPE_STAT.json", "w")                                                # i^th connection of the server
        jsonFile.write(json.dumps(data))                                                                #updating JSON file
        jsonFile.close()      
    except:# if there were no file
        jsonFile = open("JSON_FILE_TYPE_STAT.json", "w")
        data = {'image/jpg': 0, 'text/txt': 0, 'image/png': 0, 'text/html': 0}
        data[type_of_file] += 1
        jsonFile.write(json.dumps(data))                                                                #updating JSON file
        jsonFile.close()
                
    return

def JSON_REQUEST_STAT(Method):
# Count Methods and update JSON file
    try:# if file was existed
        jsonFile = open("JSON_REQUEST_STAT.json",'r')
        data = json.load(jsonFile)                                                                      # loading json data
        jsonFile.close()
        try:                                                                                            # proper method
            data[Method] += 1
        except:                                                                                         # improper method
            data['Improper'] += 1
        jsonFile = open("JSON_REQUEST_STAT.json", "w")
        jsonFile.write(json.dumps(data))                                                                # updating JSON file
        jsonFile.close()
    except:# if there were no file
        jsonFile = open("JSON_REQUEST_STAT.json", "w")
        data = {'GET': 0, 'PUT': 0, 'POST': 0, 'DELETE': 0, 'HEAD': 0, 'Improper': 0}
        try:
            data[Method] += 1                                                                           # proper method
            jsonFile.write(json.dumps(data))                                                            # updating JSON file
            jsonFile.close()
        except:    
            data['Improper'] += 1                                                                       # Improper method
            jsonFile.write(json.dumps(data))                                                            # updating JSON file
            jsonFile.close()
    return

def JSON_RESPONSE_STAT(Number):# Number = 400, 301 ,....
# Count Number and update JSON file
    try:# if file was existed
        jsonFile = open("JSON_RESPONSE_STAT.json",'r')
        data = json.load(jsonFile)                                                                      # loading json data
        jsonFile.close()
        
        data[Number] += 1
        
        jsonFile = open("JSON_RESPONSE_STAT.json", "w")
        jsonFile.write(json.dumps(data))                                                                # updating JSON file
        jsonFile.close()      
    except:# if there were no file
        jsonFile = open("JSON_RESPONSE_STAT.json", "w")
        data = {'400': 0, '501': 0, '405': 0, '200': 0, '301': 0, '403': 0}

        data[Number] += 1

        jsonFile.write(json.dumps(data))                                                                # updating JSON file
        jsonFile.close()
    return

def JSON_TO_STRING(address):
# Convert Dictionary to string
    response = ''
    jsonFile = open(address,'r')
    data = json.load(jsonFile)
    jsonFile.close()
    for i in list(data.keys()):
        response += i + ' : ' + str(data[i]) + '\n'
    return response


PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname()) # Fetching IP address
print(SERVER)

ADDR = (SERVER, PORT)                               # IP - PORT tuple
FORMAT = 'utf-8'


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)                                   # binding tuple of address to server


def handle_client(conn, addr):
# Handling Clinet messages/ Handshakes/ Responses and so on
    print(f"New Connection: {addr} connected!\n")
    
    connected = True
    while connected:

        msg = conn.recv(2048).decode(FORMAT)
        time.sleep(6)                                                              # This line of code will be used in part 2
        if not msg:
            connected = False
            continue                                                                # to prevent from receiving None messages
            
        print(f'{addr} :\n{msg}\n')                                                 # showing reveived message
        type_of_msg = stat_HTTP_disconnect(msg) # msg.split('\r')[0] for linux      # Evaluate the type of the message(disconnect/stats/HTTP)
    
        if type_of_msg == 'stat':
            # analyzing stat messages
            response = stat_msg(msg) # msg.split('\r')[0] for linux                 # create proper response to the reveived messsage
            conn.send(response.encode(FORMAT))                                      # send message
        
        if type_of_msg == 'HTTP':
            # analyzing HTTP messages
            (URL, size_of_file, response, Method) = HTTP_msg(msg, addr)
            # URL : address of file
            # size_of_file : size of the file
            # Method : check if the message is invalid/ Get/ POST

            if Method == '-1':                                  #invalid message
                conn.send(response.encode(FORMAT))              #send proper message

            if URL != '-1' and Method == 'GET':                 # Get message
####################################### Handshaking Protocol ##################################################
                conn.send(response.encode(FORMAT))              # sending the info about file
                msg = conn.recv(2048).decode(FORMAT)            # reveiving message
                if msg == 'Ready to receive':                   # receiver is ready to receive the file
                    time.sleep(1)                               # in order to have plenty of time to send the message
                    f = open(URL,'rb')
                    L = f.read(int(size_of_file))
                    conn.send(L)                                # seding file
                    print('data sent.\n')                       # file sent
                    
            if URL != '-1' and Method == 'POST':                # POST message
####################################### Handshaking Protocol ##################################################
                conn.send('Ready to receive'.encode(FORMAT))    # Server is ready to receive
                f = open(URL, 'wb')
                L = conn.recv(int(size_of_file))
                f.write(L)                                      # saving the received file
                f.close()
                conn.send(response.encode(FORMAT))              # Sending HTTP 200 OK message
                print('data received.\n')
        if type_of_msg == 'disconnect':
            conn.send('Thanks for connecting!!\n'.encode(FORMAT))
            break
            
    conn.close()            

def start():
    server.listen()                                                             # listening until receive a message
    print(f'Server is Listening on {SERVER}')
    while True:
        conn, addr = server.accept()                                            # accept the request
        thread = threading.Thread(target = handle_client, args = (conn, addr))  # multi threading
        thread.start()
        print(f'Active Connections: {threading.activeCount()-1}\n')             # print number of active connections

print('server is starting!')
start ()        

