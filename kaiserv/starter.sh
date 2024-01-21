#!/bin/bash

# Chemin relatif vers le transmetteur
chemin_relatif_vers_le_fichier_transmitter="com/transmitter.c"

# Chemin relatif vers le fichier Python qui lance le jeu
chemin_vers_le_fichier_du_lancement_du_jeu="controleur.py"

# Se déplacer dans le répertoire racine du jeu, ici c'est kaiserv
cd "$(dirname "$0")"

# Chemin complet du fichier de sortie (dans le même répertoire que le fichier source)
chemin_sortie=$(dirname "$0")/com/transmitter

gcc $chemin_relatif_vers_le_fichier_transmitter -o $chemin_sortie

if [ $? -eq 0 ]; then
    echo "Compilation réussie. Lancement du jeu Python et du transmetteur."

    # Lancer le programme Python en arrière-plan
    python3 $chemin_vers_le_fichier_du_lancement_du_jeu &

    # Attendre quelques secondes (ajuster si nécessaire)
    sleep 5

    # Lancer le transmetteur en arrière-plan
    ./com/transmitter &
else
    echo "Erreur lors de la compilation du fichier transmitter."
fi