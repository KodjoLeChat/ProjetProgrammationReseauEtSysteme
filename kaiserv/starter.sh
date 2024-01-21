#!/bin/bash

# Chemin relatif vers le transmetteur
chemin_relatif_vers_le_fichier_transmitter="com/transmitter.c"

# Chemin relatif vers le fichier Python qui lance le jeu
chemin_vers_le_fichier_du_lancement_du_jeu="controleur.py"

# Se déplacer dans le répertoire racine du jeu, ici c'est kaiserv
cd "$(dirname "$0")"

# Chemin complet du fichier compilé du transmetteur
chemin_sortie=$(dirname "$0")/com/transmitter

gcc $chemin_relatif_vers_le_fichier_transmitter -o $chemin_sortie

if [ $? -eq 0 ]; then
    echo "Compilation réussie. Lancement du jeu Python et du transmetteur."

    # script pour lancer le programme Python en arrière-plan
    python3 $chemin_vers_le_fichier_du_lancement_du_jeu &

    # Attendre 5 secondes
    sleep 5

    # script pour le transmetteur en arrière-plan
    ./com/transmitter &
else
    echo "Erreur lors de la compilation du fichier transmitter."
fi