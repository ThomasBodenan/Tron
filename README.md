# Tron
# Guide de lancement du jeu Tron

## Règles du jeu :

###### Pour déplacer votre rectangle, il suffit d'appuyer sur les touches "z","q","s","d" du clavier pour changer la direction de votre rectangle. "z" pour se diriger vers le haut, "q" pour se diriger vers la gauche, "s" pour se diriger vers le bas puis "d" pour se diriger vers la droite .Dès lors que votre rectangle touche les parois de la fenêtre ou l'autre joueur et son tracé, il y a collision et vous perdez. Ce jeu est conçu uniquement pour 2 joueurs.

## Comment lancer le jeu

### 1ère étape : Executer serveur.py
###### Entrer la commande : 
```
python3 serveur.py
```
###### Assurez-vous que les 2 joueurs ont accès au code client. Vous devez aussi changer l'adresse IP pour qu'ell puisse correspondre avec l'adresse ip du PC sur lequel vous hébergez le serveur.

### 2ème étape : Executer client.py

###### Entrer la commande : 
```
python3 serveur.py
```

###### Le serveur va alors vous envoyer le message 'W' pour attendre que les joueurs se connectent tous. Ensuite il enverra le message 'G' pour informer que la partie va commencer et on print dans la console client le fait que la partie commence ainsi que la couleur du joueur selon l'ordre d'arrivée. Si la couleur de votre rectangle est affiché comme 'R', cela signifie que la couleur est rouge sinon c'est jaune. 

###### Dès que l'un des joueurs entre en collision avec l'autre rectangle ou son tracé ou les limites de la fenêtre de jeu, la partie s'arrête car il y a eu collision. Le calcul des collisions est effectué toutes les 0.025 secondes.
