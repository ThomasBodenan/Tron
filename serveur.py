import socket
import threading
import time
import sys
import queue
import pickle
import numpy as np

SERVER_PORT = 1234

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('0.0.0.0', SERVER_PORT))
server_socket.listen(2)

game_over = False
game_started = False
couleur_attribue = False
collision = False

client_connections = {}
mouvements = queue.Queue()

# Ajouter des positions initiales pour les joueurs
positions = np.zeros((500,500))

Clients_couleur = ['R', 'Y']

def ecouter_client(client_socket, client_id):
    global collision
    while not collision:
        try:
            start_char = client_socket.recv(1)
            start_char2 = start_char.decode('utf-8')
            
            if not start_char:
                break

            if start_char2 == 'I':
                received_data = client_socket.recv(3)
                data1 = received_data.decode('utf-8')
                data = data1.split(',')
                x = int(data[0])
                y = int(data[1])
                if positions[x][y] == 0:
                    positions[x][y] = 1
                else:
                    collision = True

            elif start_char2 == 'J':
                received_data = client_socket.recv(4)
                data1 = received_data.decode('utf-8')
                data = data1.split(',')
                x = int(data[0])
                y = int(data[1])
                if positions[x][y] == 0:
                    positions[x][y] = 1
                else:
                    collision = True

            elif start_char2 == 'K':
                received_data = client_socket.recv(5)
                data1 = received_data.decode('utf-8')
                data = data1.split(',')
                x = int(data[0])
                y = int(data[1])
                if positions[x][y] == 0:
                    positions[x][y] = 1
                else:
                    collision = True

            elif start_char2 == 'W':
                received_data = client_socket.recv(6)
                data1 = received_data.decode('utf-8')
                data = data1.split(',')
                x = int(data[0])
                y = int(data[1])
                if positions[x][y] == 0:
                    positions[x][y] = 1
                else:
                    collision = True

            elif start_char2 == 'P':
                received_data = client_socket.recv(7)
                data1 = received_data.decode('utf-8')
                data = data1.split(',')
                x = int(data[0])
                y = int(data[1])
                if positions[x][y] == 0:
                    positions[x][y] = 1
                else:
                    collision = True

            elif start_char2 == 'H' :
                command = client_socket.recv(1)
                command2 = command.decode('utf-8')
                if command2 in "ZSLD":
                    mouvements.put((command2, client_id))

        except Exception as e:
            print(f"E {client_id}: {str(e)}")
            client_socket.close()
            del client_connections[client_id]


def envoyer_client(client_socket, client_id):
    global collision
    while not collision:
        if not mouvements.empty():
            (move, id) = mouvements.get()
            mouv = str(move)
            move_bytes = (mouv + "M").encode('utf-8')
            move_bytes2 = (mouv + "O").encode('utf-8')
                        
            if id == client_id:
                client_socket.send(move_bytes)
                other_client_id = 1 - client_id
                other_client_socket = client_connections[other_client_id]
                other_client_socket.send(move_bytes2)
            else:
                other_client_id = 1 - client_id
                other_client_socket = client_connections[other_client_id]
                other_client_socket.send(move_bytes)
                client_socket.send(move_bytes2)


while len(client_connections) < 2:
    client_socket, client_address = server_socket.accept()
    client_id = len(client_connections)
    client_connections[client_id] = client_socket
    print(f"Client {client_id} connecté depuis {client_address}")
    client_socket.send("W".encode('utf-8'))
time.sleep(1)
print("C'est bon, tous les joueurs sont connectés !")
for client_socket in client_connections.values():
    client_socket.send("G".encode('utf-8'))
game_started = True  # Définissez game_started sur True après que les deux clients sont connectés
time.sleep(1)
i = 0
for client_socket in client_connections.values():
    client_socket.send(Clients_couleur[i].encode('utf-8'))
    i += 1

for client_id, client_socket in client_connections.items():
    thread2 = threading.Thread(target=envoyer_client, args=(client_socket, client_id))
    thread2.start()
    thread = threading.Thread(target=ecouter_client, args=(client_socket, client_id))
    thread.start()

duree_partie = 0
duree_initial = time.time()

while not game_over:
    if collision == True :
        print("Collision détectée")
        thread.join()
        thread2.join()
        game_over = True