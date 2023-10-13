import socket
import threading
import pygame
import sys
from pygame.locals import *
import queue
import time
# import ctypes

# ctypes.windll.user32.SetProcessDPIAware()

# Initialisation de Pygame
pygame.init()
reference_resolution = (500, 500)
# Obtenir la résolution réelle de l'écran
screen_info = pygame.display.Info()
screen_width, screen_height = screen_info.current_w, screen_info.current_h

# Calculer le facteur d'échelle pour la largeur et la hauteur
scale_x = screen_width / reference_resolution[0]
scale_y = screen_height / reference_resolution[1]
largeur_fenetre, hauteur_fenetre = reference_resolution

# Créer une fenêtre de jeu redimensionnée
ecran = pygame.display.set_mode(reference_resolution)
pygame.display.set_caption('Tron')

message_queue = queue.Queue()

# Couleurs
NOIR = (0, 0, 0)
ROUGE = (255, 0, 0)

# Position et dimensions du rectangle
rectangle1_x = largeur_fenetre
rectangle1_y = hauteur_fenetre // 2
rectangle_largeur = 10
rectangle_hauteur = 10
rectangle2_x = 0
rectangle2_y = hauteur_fenetre // 2

# Vitesse de déplacement
vitesse = 0.05
couleur_joueur = ""

game_started = False
couleur_attribue = False


# Limites de la fenêtre
limite_gauche = 0
limite_droite = largeur_fenetre - rectangle_largeur
limite_haut = 0
limite_bas = hauteur_fenetre - rectangle_hauteur

# Surface pour stocker le carré
surface_tracage = pygame.Surface((largeur_fenetre, hauteur_fenetre))
surface_tracage.fill(NOIR)

game_on = True
start_time = pygame.time.get_ticks()

# Direction initiale
direction1_x = -1
direction1_y = 0
direction2_x = 1
direction2_y = 0

SERVER_IP = '172.21.72.213'

SERVER_PORT = 1234

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((SERVER_IP, SERVER_PORT))

def receive_messages(socket):
    global direction1_x, direction1_y, direction2_x, direction2_y, game_started, couleur_attribue,game_on

    while True:
        message = socket.recv(2).decode('utf-8')
        if not message:
            break
        message_queue.put((message, time.time()))  # Enregistrez le temps de réception

        if message == "ZO":
            direction2_x = 0
            direction2_y = -1
        elif message == "SO":
            direction2_x = 0
            direction2_y = 1
        elif message == "LO":
            direction2_x = -1
            direction2_y = 0
        elif message == "DO":
            direction2_x = 1
            direction2_y = 0
        elif message == "ZM":
            direction1_x = 0
            direction1_y = -1
        elif message == "SM":
            direction1_x = 0
            direction1_y = 1
        elif message == "LM":
            direction1_x = -1
            direction1_y = 0
        elif message == "DM":
            direction1_x = 1
            direction1_y = 0

message_thread = threading.Thread(target=receive_messages, args=(client_socket,))
message_thread.start()

while not game_started:
    for event in pygame.event.get():
        if event.type == QUIT:
            client_socket.send("HQ".encode('utf-8'))
            pygame.quit()
            sys.exit()

    if not message_queue.empty():
        message = message_queue.get()

        if message[0] == "G":
            game_started = True
            print("La partie commence!")

while not couleur_attribue:

    if not message_queue.empty():
        message = message_queue.get()

        if message[0] == "R" or message[0] == "Y":
            couleur_attribue = True
            couleur_joueur = message[0]
            print("Votre couleur est la couleur " + couleur_joueur)


if couleur_joueur == "R":
    rectangle1_x = largeur_fenetre - 10
    rectangle1_y = hauteur_fenetre // 2 - 10
    direction1_x = -1
    rectangle2_x = 10
    rectangle2_y = hauteur_fenetre // 2 - 10
    direction2_x = 1

elif couleur_joueur == "Y":
    rectangle1_x = 10
    rectangle1_y = hauteur_fenetre // 2 - 10
    direction1_x = 1
    rectangle2_x = largeur_fenetre - 10
    rectangle2_y = hauteur_fenetre // 2 - 10
    direction2_x = -1

touche_z = False
touche_s = False
touche_d = False
touche_q = False
temps0 = time.time()


while game_on:
    for event in pygame.event.get():
        if event.type == QUIT:
            client_socket.send("HQ".encode('utf-8'))
            pygame.quit()
            sys.exit()

    temps1 = time.time()
    if temps1 - temps0 > 0.025 :
        a = str(int(rectangle1_x)) + ',' + str(int(rectangle1_y))
        if len(a) == 3 :
            b = 'I' + a
            client_socket.send(b.encode('utf-8'))
            temps0 = temps1
        elif len(a) == 4 :
            b = 'J' + a
            client_socket.send(b.encode('utf-8'))
            temps0 = temps1
        elif len(a) == 5 :
            b = 'K' + a
            client_socket.send(b.encode('utf-8'))
            temps0 = temps1
        elif len(a) == 6 :
            b = 'W' + a
            client_socket.send(b.encode('utf-8'))
            temps0 = temps1
        elif len(a) == 7 :
            b = 'P' + a
            client_socket.send(b.encode('utf-8'))
            temps0 = temps1

    rectangle1_x += vitesse * direction1_x
    rectangle1_y += vitesse * direction1_y
    rectangle2_x += vitesse * direction2_x
    rectangle2_y += vitesse * direction2_y

    if rectangle1_x < limite_gauche:
        rectangle1_x = limite_gauche
    elif rectangle1_x > limite_droite:
        rectangle1_x = limite_droite

    if rectangle1_y < limite_haut:
        rectangle1_y = limite_haut
    elif rectangle1_y > limite_bas:
        rectangle1_y = limite_bas

    if rectangle2_x < limite_gauche:
        rectangle2_x = limite_gauche
    elif rectangle2_x > limite_droite:
        rectangle2_x = limite_droite

    if rectangle2_y < limite_haut:
        rectangle2_y = limite_haut
    elif rectangle2_y > limite_bas:
        rectangle2_y = limite_bas

    couleur1 = (0, 0, 0)
    couleur2 = (0, 0, 0)

    if couleur_joueur == "R":
        couleur1 = (255, 0, 0)
        couleur2 = (255, 255, 0)

    elif couleur_joueur == "Y":
        couleur1 = (255, 255, 0)
        couleur2 = (255, 0, 0)

    pygame.draw.rect(surface_tracage, couleur1, (rectangle1_x, rectangle1_y, rectangle_largeur, rectangle_hauteur))
    pygame.draw.rect(surface_tracage, couleur2, (rectangle2_x, rectangle2_y, rectangle_largeur, rectangle_hauteur))

    ecran.fill(NOIR)

    ecran.blit(surface_tracage, (0, 0))

    pygame.display.update()

    touches = pygame.key.get_pressed()

    if touches[K_z] and not touche_z:
        # direction1_x = 0
        # direction1_y = -1
        client_socket.send("HZ".encode('utf-8'))
        touche_z = True

    if not touches[K_z] :
        touche_z = False

    if touches[K_s] and not touche_s:
        # direction1_x = 0
        # direction1_y = 1
        client_socket.send("HS".encode('utf-8'))
        touche_s = True

    if not touches[K_s]:
        touche_s = False

    if touches[K_q] and not touche_q:
        # direction1_x = -1
        # direction1_y = 0
        client_socket.send("HL".encode('utf-8'))
        touche_q = True

    if not touches[K_q]:
        touche_q = False

    if touches[K_d] and not touche_d:
        # direction1_x = 1
        # direction1_y = 0
        client_socket.send("HD".encode('utf-8'))
        touche_d = True

    if not touches[K_d] :
        touche_d = False