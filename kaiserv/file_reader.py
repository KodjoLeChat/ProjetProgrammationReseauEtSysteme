from PIL import Image
import random

# recupere la taille d'une tuile dans un fichier
def set_tile_size(file_name):
    with open(file_name) as file_read:
        for i, line in enumerate(file_read):
            if line.__contains__("TILE_SIZE"):
                return int(line.split("=")[1])

# permet de recuperer les codes rgb de chaques pixel
def reader_bmp_map(map_number, controleur):
    file = Image.open('./assets/map/map{}.bmp'.format(map_number))
    width, height = file.width, file.height
    names_files = []
    for num_lig in range(width):
        names_files.append([])
        for num_col in range(height):
            names_files[num_lig].append(get_name_sprite(file.getpixel((num_lig, num_col))))

    controleur.grid_width  = width
    controleur.grid_height = height
    return names_files

# traite les codes rgb
def get_name_sprite(rgb_code):
    match rgb_code:
        case ((0,255,0)):
            return "herbe_{}".format(random.randint(110,119))
        case((0,180,0)):
            return "arbre_{}".format(random.randint(40,61))
        case ((0,0,255)):
            return "eau"
        case ((105,105,105)):
            return "route"

    print("Code RGB {} inconnu, poursuite du chargement")
    return None
