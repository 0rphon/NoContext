import socket
from sys import argv
from time import sleep

HOST = 'REMOVED FOR GITHUB'         # The server's hostname
PORT = 0#REMOVED FOR GITHUB         # The port used by the server
key="REMOVED FOR GITHUB"

 

def send_image(img_path):
    try:
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  #create socket obj
        server.connect((HOST, PORT))                                #connect to host/port
        server.sendall(key.encode())                                #send key
        resp = server.recv(1024).decode()                           #get validation response
        if resp == "null":                                          #if response valid
            with open(img_path,"rb") as img:                        #with image as img
                img_type = img_path[img_path.rindex('.'):]          #get img type
                server.sendall(img_type.encode())                   #send img type
                send_img = img.read()                               #read img data
                server.sendall(send_img)                            #send img data
                return "Image Sent"                                 #return success 
        else: return "Invalid Key"                                  #if key invalid return fail
        server.close()                                              #close connection
    except ConnectionRefusedError: return "Server Down"             #if connection refused return fail
    except TimeoutError: return "Server Down"


def main():
    img_path=argv[1]                    #get image path
    result = send_image(img_path)       #send img
    print(result)                       #print result
    sleep(2)

if __name__=="__main__":
    main()