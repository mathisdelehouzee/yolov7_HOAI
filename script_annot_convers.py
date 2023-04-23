#créer un nouveau fichier yolo_annotation.csv à partir du fichier BD_HANDSONAI/Test/annotation.csv où on supprime les 32 premiers caractères de chaque ligne

import csv
import os

# Définir la fonction pour extraire le numéro de fichier à partir d'une ligne du CSV
def get_file_number(csv_line):
    return csv_line.split('gen_')[1].split('.')[0]

# Ouvrir le fichier CSV
with open('datasets/Val/val.txt', 'r') as csv_file:
    # Lire les lignes du fichier CSV
    csv_lines = csv_file.readlines()

    # Créer un dictionnaire pour stocker les annotations par fichier
    annotations_by_file = {}

    # Parcourir toutes les lignes du fichier CSV
    for line in csv_lines:
        # Extraire les informations d'annotation de la ligne
        filename, bbox = line.strip().split(" ")
        x1, y1, x2, y2, numclass = bbox.split(',')
        x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
        numclass = int(numclass)

        # Calculer les coordonnées de la boîte englobante
        xcenter = (x1 + ((x2 - x1) / 2))/800
        ycenter = (y1 + ((y2 - y1) / 2))/800
        width = (x2 - x1)/800
        height = (y2 - y1)/800

        # Extraire le numéro de fichier à partir du nom de fichier
        file_number = get_file_number(filename)

        # Vérifier si le fichier existe déjà dans le dictionnaire
        if file_number in annotations_by_file:
            # Ajouter l'annotation à la liste existante
            annotations_by_file[file_number].append((numclass, xcenter, ycenter, width, height))
        else:
            # Créer une nouvelle liste d'annotations pour le fichier
            annotations_by_file[file_number] = [(numclass, xcenter, ycenter, width, height)]

    # Parcourir toutes les entrées du dictionnaire et écrire les fichiers texte correspondants
    for file_number, annotations in annotations_by_file.items():
        # Créer le nom de fichier pour le fichier texte correspondant
        txt_filename = f"gen_{file_number}.txt"

        # Ouvrir le fichier texte en mode écriture
        with open("datasets/HOAI/labels/val/"+ txt_filename, 'w') as txt_file:
            # Parcourir toutes les annotations du fichier et écrire les lignes correspondantes dans le fichier texte
            for annotation in annotations:
                numclass, xcenter, ycenter, width, height = annotation
                txt_file.write(f"{numclass} {xcenter} {ycenter} {width} {height}\n")


