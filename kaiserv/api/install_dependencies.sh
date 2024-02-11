#!/bin/bash

# Vérifier si les dépendances Python sont installées
if ! command -v pip3 &> /dev/null; then
    echo "Installer pip3..."
    sudo apt-get update
    sudo apt-get install -y python3-pip
fi

# Vérifier si Flask est installé
if ! python3 -c "import flask" &> /dev/null; then
    echo "Installer Flask..."
    pip3 install Flask
fi

# Vérifier si psycopg2-binary est installé
if ! python3 -c "import psycopg2" &> /dev/null; then
    echo "Installer psycopg2-binary..."
    pip3 install psycopg2-binary
fi

# Vérifier si bcrypt est installé
if ! python3 -c "import bcrypt" &> /dev/null; then
    echo "Installer bcrypt..."
    pip3 install bcrypt
fi

# Vérifier si le conteneur de la base de données existe
if [ ! "$(docker ps -q -f name=kaiserv_db)" ]; then
    # Si le conteneur n'existe pas, le créer
    docker run --name kaiserv_db -e POSTGRES_USER=kaiserv_user -e POSTGRES_PASSWORD=kaiserv_mdp -p 5432:5432 -d postgres
fi

# Attendre 10 secondes pour laisser le temps à la base de données de démarrer si elle vient d'être créée
sleep 10

# Exécuter le script de lancement de l'API
python3 api.py

