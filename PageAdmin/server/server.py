import socket
from threading import Thread
import datetime
from random import randint, choice
import os
from subprocess import call
from time import sleep
import facebook
from datetime import date



HOST = '0.0.0.0'                        # Standard loopback interface address (localhost)
PORT = 0#REMOVED FOR GITHUB             # Port to listen on (non-privileged ports are > 1023)
time_til_next_post = 0
connection_log = list()                 #list of connections
server_key = "REMOVED FOR GITHUB"
token = "REMOVED FOR GITHUB"
#y/m/d
token_expiration = date(2020, 6, 6)
dns_expiration = date(2020, 5, 7)


#checks if proper folders exist
def initialize():
    if os.path.isdir("queue")==False:                               #checks if queue file exists
            os.mkdir("queue")



#recieve data until client disconnects
def recv_img(client):
    data = list()
    while True:
        data.append(client.recv(2048))
        if not data[-1]:
            return b''.join(data)



#validates user and recieves image
def recieve_image(client):
    key = client.recv(1024).decode()                                #gets validation key
    if key == server_key:                                           #if key valid
        client.sendall(b"null")                                     #send validation response
        img_type = client.recv(1024).decode()                       #recieve file type
        client_img = recv_img(client)                               
        img_name = "queue/"+str(randint(0,999999))+img_type         #generate img name
        with open(img_name, "wb") as img:                           #write img to queue folder
            img.write(client_img)
    else:                                                           #if key invalid
        response = "The time is: "+str(datetime.datetime.now())     #generate fake time message
        client.sendall(response.encode())                           #send fake time message



#handles client connections
def accept_client_imgs():
    global connection_log
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:    #creates socket obj
        s.bind((HOST, PORT))                                        #binds socket to host/port
        s.listen(5)                                                 #listens for incoming connections
        while True:
            client, addr = s.accept()                               #waits for connection
            with open("iplog.txt","a") as iplog:
                iplog.write(addr[0]+"\n")
            connection_log.append(addr[0])                          #adds ip to list
            t=Thread(target=recieve_image, args=(client,))          #creates recieve_img thread obj with client
            t.start()                                               #calls recieve_img thread



#updates cmd
def update_screen():
    call("cls",shell=True)                                          #CHANGE TO CLEAR FOR LINUX
    print("Token Expires in " + str((token_expiration-date.today()).days) + " Days")
    print("DDNS Expires in " + str((dns_expiration-date.today()).days) + " Days")
    print("Time Until Next Post: "+str(time_til_next_post//60)+":{:02d}".format(time_til_next_post%60))
    print("Images in Queue:", len(os.listdir("queue")))
    print('Connections:', len(connection_log))
    for ip in connection_log[::-1][:10]: print("    "+ip)



def handle_posting():
    global time_til_next_post
    graph = facebook.GraphAPI(token)
    while True:
        queue = os.listdir("queue")
        if len(queue)>0:
            img = "queue/"+choice(queue)
            with open(img,"rb") as meme:                     #UNCOMMENT TO POST
                graph.put_photo(image=meme,)                 #UNCOMMENT TO POST
            os.remove(img)                                   #UNCOMMENT TO POST
        for x in range(1800,-1,-1):
            sleep(1)
            time_til_next_post = x





def main():
    initialize()                                    #checks folders
    t = Thread(target=accept_client_imgs)           #creates accept_client_imgs thread
    t.start()                                       #starts accept_client_img thread
    t = Thread(target=handle_posting)
    t.start()
    while True: 
        update_screen()
        sleep(0.2)


if __name__=="__main__":
    main()


"""
server:
thread 1: accept images, download them, and updates globals queue len and connection log
thread 2: counts down timer (sleep one second in loop?) and posts
main: updates screen with timer, queue len, and connection log
"""