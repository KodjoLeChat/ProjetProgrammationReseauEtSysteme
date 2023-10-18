# kaiserV

## Installation du package pillow indispensable
## Installation du package pygame indispensable
## Installation du package heapq  indispensable
## Installation du package pickle indispensable
## Installation du package numpy  indispensable

Si l'un de ces packages n'est malheursement pas fournis avec votre python vous pouvez les installer de la manières suivantes
Pour ce faire vous avez **deux** façon de faire, en considérant que vous posséder pip avec votre python.

1. `py -m pip install pillow`
2. `python3 -m pip install pillow`

## Lancement du programme
Selon l'OS vous pourrez faire:
- py controleur.py
- python3 controleur.py

## Modification de la carte
Vous pouvez modifier votre carte dans le répertoire assets/map
Cependant, veillez à ce qu'elle conserve map1.bmp. Vous pouvez utilisez le code couleur suivant pour modifier votre carte:
- herbe (0,255,0)
- arbre (0,180,0)
- eau   (0,0,255)
- route (105,105,105)

## Modification de la taille des tuiles
Si vous voulez faire n'importe quoi vous pouvez modifier la valeur dans settings.txt
Tant que cela reste un entier positif