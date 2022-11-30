import socket
import threading
import os.path
import time
import datetime
import json



def stat_HTTP_disconnect(a_string):
    if a_string == 'number of connected clients' or a_string == 'file type stats' or a_string == 'request stats' or a_string =='response stats':                          
        return 'stat'
    
    if a_string == 'disconnect':
        return 'disconnect'
    
    else:
        return 'HTTP'

def stat_msg(a_string):
    if a_string == 'number of connected clients':
        return 'number of connected clients : ' + str(int(threading.activeCount()-1)) + '\n'
        
    if a_string == 'file type stats':
        try:
            response = JSON_TO_STRING("JSON_FILE_TYPE_STAT.json")
            return response                             
        except:
            response = 'image/jpg : 0\n' +\
                        'text/txt : 0\n' +\
                       'image/png : 0\n' +\
                       'text/html : 0' 
            return response           
    
    if a_string == 'request stats':
        try:
            response = JSON_TO_STRING("JSON_REQUEST_STAT.json")
            return response                             
        except:
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
        except:
            response = '400 : 0\n'      +\
                       '501 : 0\n'      +\
                       '405 : 0\n'      +\
                       '200 : 0\n'      +\
                       '301 : 0\n'      +\
                       '403 : 0'    
            return response           


def string_with_calculated_length(a_string):
        location_of_length = 2
        length_of_string = len(a_string)
        length_of_the_length_of_string = len(str(length_of_string))
        length_of_string += int(length_of_the_length_of_string)
        lines_of_string = a_string.split('\n')
        lines_of_string[location_of_length] += str(length_of_string)
        return '\n'.join(lines_of_string)

                
def HTTP_msg(a_string, addr):
    lines_of_string = a_string.split('\n')
    body_loc = -1
    for i in range(0,len(lines_of_string)):
        if lines_of_string[i] == '':
            break
        body_loc = i
        
    if body_loc == -1:
        b = lines_of_string[0::]     
    else:
        b = lines_of_string[0:body_loc+1]
        
    first_line = b[0].split(' ')
    flag = 0
    
    for i in range(1,len(b)):
        temp = b[i].split(': ')
        if len(temp) == 2:
            continue
        flag = 1
        break
    
    version = first_line[-1].split('/')[-1]
    HTTP_versions = ['1.0', '1.1']
    if flag == 1 or len(first_line) != 3 or HTTP_versions.count(version) == 0:
        request_time = str(datetime.datetime.now())
        msg = 'HTTP/1.0 400 Bad Request\n'                                                              +\
              'Connetion: close\n'                                                                      +\
              'Content-Length: '+ '\n'                                                                  +\
              'Content-Type: text/html\n'                                                               +\
              'Date: '+ request_time + '\n\n'                                                           +\
              '<html><body><h1>BADREQUEST!</h1></body></html>'
        msg = string_with_calculated_length(msg)
        
        JSON_LOG(addr, lines_of_string[0].split(' ')[0], '400 Bad Request', request_time)
        JSON_REQUEST_STAT(a_string.split('\n')[0].split(' ')[0])    
        JSON_RESPONSE_STAT('400')
        
        return ('-1','-1', msg, '-1')
    
    service_type = ['GET','HEAD','DELETE','POST','PUT']
    if  service_type.count(first_line[0]) == 0:
        print(first_line[0])
        request_time = str(datetime.datetime.now())        
        msg = 'HTTP/1.0 501 Not Implemented\n'                                                          +\
              'Connetion: close\n'                                                                      +\
              'Content-Length: ' + '\n'                                                                 +\
              'Content-Type: text/html\n'                                                               +\
              'Date: ' + request_time  + '\n\n'                                                         +\
              '<html><body><h1>NOTIMPLEMENTED!</h1></body></html>'
        msg = string_with_calculated_length(msg)
       
        JSON_LOG(addr, lines_of_string[0].split(' ')[0], '501 Not Implemented', request_time)
        JSON_REQUEST_STAT('Improper')
        JSON_RESPONSE_STAT('501')
                
        return ('-1','-1', msg, '-1')
        
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
        
        JSON_LOG(addr, lines_of_string[0].split(' ')[0], '405 Method Not Allowed', request_time)
        JSON_REQUEST_STAT(lines_of_string[0].split(' ')[0])
        JSON_RESPONSE_STAT('405')
       
        return ('-1','-1', msg, '-1')
    
    if first_line[0] == 'GET':
        request_time = str(datetime.datetime.now())        
        if os.path.isfile(first_line[1]):
            type_of_file = os.path.splitext(first_line[1])[1][1::]
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
            
            JSON_LOG(addr, lines_of_string[0].split(' ')[0], '200 OK', request_time)
            JSON_FILE_TYPE_STAT(type_of_file)
            JSON_REQUEST_STAT("GET")
            JSON_RESPONSE_STAT('200')
            
            return (first_line[1], length_of_file, msg, 'GET')
        
        else:
            request_time = str(datetime.datetime.now())            
            msg = 'HTTP/1.0 301 Moved Permanently\n'                                                   +\
                  'Connetion: close\n'                                                                 +\
                  'Content-Length: '+ '\n'                                                             +\
                  'Content-Type: text/html\n'                                                          +\
                  'Date: ' + request_time + '\n\n'                                                     +\
                  '<html><body><h1>MOVEDPERMANENTLY!</h1></body></html>'              
            msg = string_with_calculated_length(msg)
            
            JSON_LOG(addr, lines_of_string[0].split(' ')[0], '301 Moved Permanently', request_time)
            JSON_REQUEST_STAT("GET")
            JSON_RESPONSE_STAT('301')
            
            return ('-1','-1', msg, '-1')
    
    if first_line[0] == 'POST' and  len(lines_of_string) == body_loc+1:
        type_of_file = lines_of_string[body_loc-1].split(': ')[1].split('/')[1]
        size_of_file = a_string.split('\n')[-3].split(': ')[1]
        msg = 'HTTP/1.0 200 OK' + '\n'                                         +\
              'Connetion: close\nContent-Length: ' + str(len(a_string)) + '\n' +\
              'Content-Type: text/html' + '\n'                                 +\
              'Date: ' + str(datetime.datetime.now()) + '\n\n'                 +\
              '<html><body><h1>POST!</h1></body></html>'
        
        JSON_REQUEST_STAT("POST")
        JSON_RESPONSE_STAT('200')

        return ('Server\\'+first_line[1]+'.'+ type_of_file, size_of_file, msg, 'POST')
    
    
    if True:#else:
        request_time = str(datetime.datetime.now())        
        msg = 'HTTP/1.0 403 Forbidden\n'                                                               +\
              'Connetion: close\n'                                                                     +\
              'Content-Length: '+ '\n'                                                                 +\
              'Content-Type: text/html\n'                                                              +\
              'Date: ' + request_time + '\n\n'                                                         +\
              '<html><body><h1>FORBIDDEN!</h1></body></html>'
        msg = string_with_calculated_length(msg)
        
        JSON_LOG(addr, lines_of_string[0].split(' ')[0], '403 Forbidden', request_time)
        JSON_REQUEST_STAT('POST')
        JSON_RESPONSE_STAT('403')
        
        return ('-1', '-1 ', msg, '-1')           
    return 0


def JSON_LOG(addr, Method, status_message, date_time):
    try:
        if Method != '' or Method != None:
            jsonFile = open("JSON_LOG.json", "r")
            data = json.load(jsonFile)
            jsonFile.close()
            
            connection_i = str(int(list(data.keys())[-1].split(' ')[-1]) + 1)            
            data.update({'connection ' + connection_i : [str(addr), Method, status_message, date_time]})
            
            jsonFile = open("JSON_LOG.json", "w")
            jsonFile.write(json.dumps(data))
            jsonFile.close()    
    except:    
            jsonFile = open("JSON_LOG.json", "w")
            data = {'connection 1' : [str(addr), Method, status_message, date_time]}
            jsonFile.write(json.dumps(data))
            jsonFile.close()
    return 0   
            
def JSON_FILE_TYPE_STAT(type_of_file):
    try:
        jsonFile = open("JSON_FILE_TYPE_STAT.json",'r')
        data = json.load(jsonFile)
        jsonFile.close()
        
        data[type_of_file] += 1
        
        jsonFile = open("JSON_FILE_TYPE_STAT.json", "w")
        jsonFile.write(json.dumps(data))
        jsonFile.close()      
    except:
        jsonFile = open("JSON_FILE_TYPE_STAT.json", "w")
        data = {'image/jpg': 0, 'text/txt': 0, 'image/png': 0, 'text/html': 0}
        data[type_of_file] += 1
        jsonFile.write(json.dumps(data))
        jsonFile.close()
                
    return

def JSON_REQUEST_STAT(Method):
    try:
        jsonFile = open("JSON_REQUEST_STAT.json",'r')
        data = json.load(jsonFile)
        jsonFile.close()
        try:
            data[Method] += 1
        except:
            data['Improper'] += 1
        jsonFile = open("JSON_REQUEST_STAT.json", "w")
        jsonFile.write(json.dumps(data))
        jsonFile.close()
    except:
        jsonFile = open("JSON_REQUEST_STAT.json", "w")
        data = {'GET': 0, 'PUT': 0, 'POST': 0, 'DELETE': 0, 'HEAD': 0, 'Improper': 0}
        try:
            data[Method] += 1
            jsonFile.write(json.dumps(data))
            jsonFile.close()
        except:    
            data['Improper'] += 1
            jsonFile.write(json.dumps(data))
            jsonFile.close()
    return

def JSON_RESPONSE_STAT(Number):
    try:
        jsonFile = open("JSON_RESPONSE_STAT.json",'r')
        data = json.load(jsonFile)
        jsonFile.close()
        
        data[Number] += 1
        
        jsonFile = open("JSON_RESPONSE_STAT.json", "w")
        jsonFile.write(json.dumps(data))
        jsonFile.close()      
    except:
        jsonFile = open("JSON_RESPONSE_STAT.json", "w")
        data = {'400': 0, '501': 0, '405': 0, '200': 0, '301': 0, '403': 0}

        data[Number] += 1

        jsonFile.write(json.dumps(data))
        jsonFile.close()
    return

def JSON_TO_STRING(address):
    response = ''
    jsonFile = open(address,'r')
    data = json.load(jsonFile)
    jsonFile.close()
    for i in list(data.keys()):
        response += i + ' : ' + str(data[i]) + '\n'
    return response#[0:-1]


PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
print(SERVER)

ADDR = (SERVER, PORT)
FORMAT = 'utf-8'


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)


def handle_client(conn, addr):
    print(f"New Connection: {addr} connected!\n")
    
    connected = True
    while connected:

        msg = conn.recv(2048).decode(FORMAT)
        #time.sleep(6)
        if not msg:
            connected = False
            continue
            
        print(f'{addr} :\n{msg}\n')
        type_of_msg = stat_HTTP_disconnect(msg.split('\r')[0])
    
        if type_of_msg == 'stat':
            response = stat_msg(msg.split('\r')[0])
            conn.send(response.encode(FORMAT))
        
        if type_of_msg == 'HTTP':   
            (URL, size_of_file, response, Method) = HTTP_msg(msg, addr)
            
            if Method == '-1':            
                conn.send(response.encode(FORMAT))
            
            if URL != '-1' and Method == 'GET':
                conn.send(response.encode(FORMAT))                
                msg = conn.recv(2048).decode(FORMAT)
                if msg == 'Ready to receive':
                    time.sleep(1)
                    f = open(URL,'rb')
                    L = f.read(int(size_of_file))
                    conn.send(L)
                    print('data sent.\n')
                    
            if URL != '-1' and Method == 'POST':
                conn.send('Ready to receive'.encode(FORMAT))
                f = open(URL, 'wb')
                L = conn.recv(int(size_of_file))
                f.write(L)
                f.close()
                conn.send(response.encode(FORMAT))
                print('data received.\n')
        if type_of_msg == 'disconnect':
            conn.send('Thanks for connecting!!\n'.encode(FORMAT))
            break
            
    conn.close()            

def start():
    server.listen()
    print(f'Server is Listening on {SERVER}')
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target = handle_client, args = (conn, addr))
        thread.start()
        print(f'Active Connections: {threading.activeCount()-1}\n')

print('server is starting!')
start ()        
