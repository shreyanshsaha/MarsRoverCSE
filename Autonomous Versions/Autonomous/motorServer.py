import socket
import sys
import select
from motor import Motor

BUFFER=10

host=''
port=12345
server=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.setblocking(0)
socket_list=[]

server.bind((host,port))
server.listen(5)
print('Server initiated')
socket_list.append(server)

roverMotor=Motor('/dev/ttyACM0')


while socket_list:
    data=None
    readable,_,_=select.select(socket_list,[],[],0)
    for client in readable:
        if client is server:
            connection,client_address=client.accept()
            socket_list.append(connection)
            print(client_address,'connected')
            # connection.send('You are connected now' .encode('ascii'))
        else:
            data=client.recv(BUFFER)
            if data:
                d=data.decode('ascii')
                print("DATA:", d)
                if (d=='F'):
                    roverMotor.moveMotor('forward')
                elif(d=='R'):
                    roverMotor.moveMotor('right')
                elif(d=='L'):
                    roverMotor.moveMotor('left')
                elif(d=='B'):
                    roverMotor.moveMotor('backward')
                elif(d=='S'):
                    roverMotor.moveMotor('stop')
            elif not data:
                print('Disconnected')
                socket_list.remove(client)        
                        

                # for s in socket_list:
                #     if (s!=server and s!=socket):
                #         s.send(data)
