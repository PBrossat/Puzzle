import cv2
import numpy as np
import matplotlib.pyplot as plt
import re
from collections import Counter
import math


imageCouleurRGB = cv2.imread('exemple_puzzle1.jpeg')

imageCouleurHSV = cv2.cvtColor(imageCouleurRGB, cv2.COLOR_BGR2HSV)
imageGreyScale = cv2.cvtColor(imageCouleurRGB, cv2.COLOR_BGR2GRAY)
imageCouleurLAB = cv2.cvtColor(imageCouleurRGB, cv2.COLOR_BGR2LAB)
imageCouleurHSVGauss = cv2.GaussianBlur(imageCouleurHSV, (5, 5), 0)
imageCouleurLABGauss = cv2.GaussianBlur(imageCouleurLAB, (5, 5), 0)

# ---------------------------------------Resize de l'image--------------------------------------------


def resizeImage(image, gauche, droite, haut, bas):
    image = image[haut:-bas, gauche:-droite]
    return image


def bordBlanc(imageNiveauDeGris):
    for i in range(imageNiveauDeGris.shape[0]):
        for j in range(2):
            imageNiveauDeGris[i][j] = 255

    for i in range(imageNiveauDeGris.shape[0]):
        for j in range(imageNiveauDeGris.shape[1]-1, imageNiveauDeGris.shape[1]):
            imageNiveauDeGris[i][j] = 255

    for i in range(2):
        for j in range(imageNiveauDeGris.shape[1]):
            imageNiveauDeGris[i][j] = 255

    for i in range(imageNiveauDeGris.shape[0]-1, imageNiveauDeGris.shape[0]):
        for j in range(imageNiveauDeGris.shape[1]):
            imageNiveauDeGris[i][j] = 255

    return imageNiveauDeGris


imageCouleurLABGauss = resizeImage(imageCouleurLABGauss, 5, 120, 10, 10)

# ---------------------------------------Définition des variables--------------------------------------------
longueurImage = imageCouleurLABGauss.shape[1]
largeurImage = imageCouleurLABGauss.shape[0]


# ---------------------------------------Définition des fonctions--------------------------------------------

# fonction permettant de définir la couleur la plus utilisée dans une zone interressante de l'image


def plageDeCouleurZoneInterressante(image, haut, bas, gauche, droite):
    tabCouleurZoneInterressante = []
    for i in range(int(haut), int(bas)):
        for j in range(int(gauche), int(droite)):
            tabCouleurZoneInterressante.append(image[i][j])

    # Compter le nombre de fois que chaque couleur apparaît
    compteur = {}
    for couleur in tabCouleurZoneInterressante:
        couleur_str = str(couleur)
        if couleur_str in compteur:
            compteur[couleur_str] += 1
        else:
            compteur[couleur_str] = 1

    # Trier les couleurs par ordre décroissant de fréquence
    couleurs_triees = sorted(
        compteur.items(), key=lambda x: x[1], reverse=True)
    # Afficher la couleur la plus fréquente
    couleur_plus_frequente = couleurs_triees[0][0]
    # Chaîne de caraceres à liste
    couleur_plus_frequente = couleur_plus_frequente.replace('[', '')
    couleur_plus_frequente = couleur_plus_frequente.replace(']', '')
    couleur_plus_frequente = couleur_plus_frequente.split()
    couleur_plus_frequente = [int(i) for i in couleur_plus_frequente]
    print("la couleur dominante de la zone est : ")
    print(couleur_plus_frequente)
    return couleur_plus_frequente


# fonction permettant de transformer une image couleur en image noir et blanc en fonction de la couleur dominante de l'image
def HSVtoBW(image, CouleurDominanteLAB, erreur):
    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            # si le pixel est dans la plage de couleur de la zone interressante + ou - erreur
            if (image[i][j][0] >= (CouleurDominanteLAB[0]-erreur) and image[i][j][0] <= (CouleurDominanteLAB[0]+erreur) and image[i][j][1] > (CouleurDominanteLAB[1]-erreur) and image[i][j][1] < (CouleurDominanteLAB[1]+erreur) and image[i][j][2] > (CouleurDominanteLAB[2]-erreur) and image[i][j][2] < (CouleurDominanteLAB[2]+erreur)):
                # on remplace le pixel par un pixel blanc
                image[i][j] = [255, 255, 255]
            else:
                # on remplace le pixel par un pixel noir
                image[i][j] = [0, 0, 0]


# ---------------------------------------Contour de la forme--------------------------------------------

def contourFormeLigne(image, ligne):
    tabCouleurPixel = []
    # remplir le tableau des couleurs des pixels de la ligne passée en paramètre
    for i in range(image.shape[1]):
        tabCouleurPixel.append(image[ligne][i])

    # parcours du tableau des couleurs des pixels (de 1 à la longueur du tableau)
    for i in range(0, len(tabCouleurPixel)-1):
        # si le pixel est d'une couleur différente au pixel précédent
        if (tabCouleurPixel[i][0] != tabCouleurPixel[i+1][0]):
            # le pixel de l'image correspondant à un contour devient rouge
            image[ligne][i] = [0, 0, 255]


def contourFormeColonne(image, colonne):
    tabCouleurPixel = []
    # remplir le tableau des couleurs des pixels de la colonne passée en paramètre
    for i in range(image.shape[0]):
        tabCouleurPixel.append(image[i][colonne])

    # parcours du tableau des couleurs des pixels (de 1 à la longueur du tableau)
    for i in range(0, len(tabCouleurPixel)-1):
        # si le pixel est d'une couleur différente au pixel précédent
        if (tabCouleurPixel[i][0] != tabCouleurPixel[i+1][0]):
            # le pixel de l'image correspondant à un contour devient cyan
            image[i][colonne] = [255, 255, 0]


# ---------------------------------------Isolement d'une pièce du puzzle--------------------------------------------
def isolementPiecePuzzle(image):
    # Inverser les couleurs de l'image
    inv_image = cv2.bitwise_not(image)
    # conversion en niveaux de gris
    gray = cv2.cvtColor(inv_image, cv2.COLOR_BGR2GRAY)
    # Détection des composantes connexes
    num_labels, labels = cv2.connectedComponents(gray)

    # generer une couleur differente pour chaque composante connexe
    colors = np.random.randint(0, 256, size=(num_labels, 3), dtype=np.uint8)

    # Colorier chaque composante connexe avec une couleur différente
    colored = np.zeros_like(image)
    for label in range(1, num_labels):
        mask = labels == label
        colored[mask] = colors[label]
    return colored


def trouverContour(image, imageCouleur):
    # Trouver les contours
    contours, _ = cv2.findContours(
        image, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)

    sommePerimetreContours = 0
    for contour in contours:
        # somme de la longueur des contours
        sommePerimetreContours += len(contour)

    # calcul de la moyenne de la longueur des contours
    moyennePerimetreContour = sommePerimetreContours/len(contours)

    # Supprimer les contours indésirables (min 500 max moyenne+1000)
    contours_filtres = []
    for contour in contours:
        if (len(contour) >= 500 and len(contour) <= (moyennePerimetreContour+1000)):
            contours_filtres.append(contour)

    # Afficher les contours en vert
    imageContour = cv2.drawContours(
        imageCouleur, contours_filtres, -1, (0, 255, 0), 2)

    return imageContour, contours_filtres


def recuperationPiecePuzzle(imageContour, listeImageContour, index):
    x, y, w, h = cv2.boundingRect(listeImageContour[index])
    piecePuzzle = imageContour[y:y+h, x:x+w]
    return piecePuzzle


# ---------------------------------------Appel des fonctions--------------------------------------------
erreur = 15

# Définition de la couleur dominante de l'image imageCouleurHSVGauss
CouleurDominante = plageDeCouleurZoneInterressante(
    imageCouleurLABGauss, 0, largeurImage, 0, longueurImage)

# Transformation de l'image couleur en image noir et blanc
HSVtoBW(imageCouleurLABGauss, CouleurDominante, erreur)

# kernel
kernel = np.ones((3, 3), np.uint8)
imageBlackWhiteLABGauss = cv2.morphologyEx(
    imageCouleurLABGauss, cv2.MORPH_OPEN, kernel)  # noir et blanc en RGB


imageBlackWhiteLABGauss_grey = cv2.cvtColor(
    imageBlackWhiteLABGauss, cv2.COLOR_BGR2GRAY)  # vrai noir et blanc en niveaux de gris

cv2.imshow("Image Noir et Blanc", imageBlackWhiteLABGauss_grey)


# isolement d'une pièce du puzzle
imageCouleurLABGaussPieceColoree = isolementPiecePuzzle(imageCouleurLABGauss)
cv2.imshow("Image Pieces Coloree", imageCouleurLABGaussPieceColoree)


# coloration des bords de l'image en blanc
imageBlackWhiteLABGauss_grey_white_border = bordBlanc(
    imageBlackWhiteLABGauss_grey)

# contour des formes de l'image
imageContour = trouverContour(
    imageBlackWhiteLABGauss_grey_white_border, imageCouleurLABGauss)
cv2.imshow("Image Contour", imageContour[0])


# affichage des trois premières pièces indépendamments
for i in range(3):
    piecePuzzle = recuperationPiecePuzzle(
        imageBlackWhiteLABGauss_grey_white_border, imageContour[1], i)
    cv2.imshow("Piece Puzzle"+str(i), piecePuzzle)


cv2.waitKey(0)
cv2.destroyAllWindows()


# Meilleur config :
# imageCouleurLABGauss, erreur = 15 , kernel : (3,3), parcours sur L , A et B (indice 0,1,2)
