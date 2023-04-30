# Projet d'Analyse d'image

## Ce qui a été fait

### Fonctionnalités réalisées

- Identification des différentes pièces de puzzle, grâce aux deux fonctions suivantes :
  1- plageDeCouleurZoneInterressante(image, haut, bas, gauche, droite)
  2- HSVtoBW(image, CouleurDominanteLAB, erreur)

La première fonction permet de détecter la couleur dominante d'une zone précise d'une image. Ici, l'image utilisée est au format LAB à laquelle on a appliqué un "Gaussian Blur". Dans l'appel de cette fonction, la zone intéressante est l'image entière. Celle-ci permet alors de détecter que la couleur dominante de l'image est l'orange (affichage du code couleur de celle-ci dans le terminal).

La deuxième fonction permet de transformer une image en couleur (ici LAB) en une image en Noir et Blanc. Pour cela, elle parcourt l'image et détecte la couleur du pixel, si celle-ci fait partie de la plage :
[couleurDominanteLAB-erreur, couleurDominanteLAB+erreur] alors le pixel devient blanc, sinon noir.

La combinaison de ces deux fonctions permet de transformer une image en couleur en une image en noir et blanc tout en séparant le premier plan du deuxième.

Pour tester ces deux fonctions, j'ai utilisé plusieurs images :
![Image Puzzle](exemple_puzzle1.jpeg)

![Image Jouets](Images/exemple_jouets.jpeg)

![Image Feuille](Images/exemple_feuilles.jpeg)

- Coloration de chaque pièce indépendamment des autres grâce à la fonction suivante:
  - isolementPiecePuzzle(image)

Cette fonction prend en paramètre une image en noir et blanc, et "colorise" chaque composante connexe de l'image avec une couleur différente. J'ai choisi de colorier chaque pièce de puzzle avec des couleurs choisies au hasard pour un souci d'esthétisme. Evidemment, on peut changer cette partie de la fonction pour colorier les composantes connexes de l'image en niveaux de gris différent.

### Bonus réalisé

- Bonus 1 : création de vignettes représentants les pièces de puzzle grâce aux deux fonctions :
  1- trouverContour(image, imageCouleur)
  2- recuperationPiecePuzzle(imageContour, listeImageContour, index)

La première fonction permet de renvoyer : une image avec les contours des pièces de puzzle coloriés en vert ainsi qu'une liste de contours que l'on appelle contours_filtres contenant tous les contours désirables. C'est-à-dire que cette liste ne contient ni les trop petits contours (les petits points sur l'image), ni les trop gros (notamment celui qui fait tout le tour de l'image).

La deuxième fonction renvoie l'image unique contenant la pièce de puzzle d'indexe : index.

### Fonctions créées personnellement

Fonctions permettant de trouver les contours des pièces de puzzle
1- contourFormeColonne(image, colonne)
2- contourFormeLigne(image, ligne)

Celles-ci parcourent respectivement l'image en hauteur et en largeur et détectent un changement de couleur de l'image puis colorient le pixel frontière en une couleur définie dans le corps de la fonction.
J'ai créé ces deux fonctions avant de découvrir la fonction findContours(...) de la librairie cv2 qui me permet de faire la même chose et de renvoyer la liste des contours par la même occasion.
Je n'utilise pas ces fonctions dans mes appels, mais je trouve pertinent le fait de vous les présenter.

Fonctions permettant de redimensionner l'image
1- resizeImage(image, gauche, droite, haut, bas)
2- bordBlanc(imageNiveauDeGris)

La première fonction permet de redimensionner l'image grâce aux paramètres de celle-ci.
Cette fonction est utilisée pour enlever la partie droite de l'image puzzle1.jpeg car celle-ci est inutile.
La deuxième fonction permet de colorier les pixels du contour de l'image en blanc pour le bon fonctionnement de la fonction trouverContour(image, imageCouleur).

### Ce que peut être amélioré

Le temps de chargement du script peut-être amélioré, en effet, celui-ci est assez long (environ une dizaine de secondes) car il y a beaucoup de parcours d'image à faire.
Nous avons décidé de proposer ce script, car nous avons, le plus possible, créé nos propres fonctions.
Nous n'avons utilisé que les fonctions de la librairie cv2 pour les parties plus complexes (comme findContours notamment).

## Retour sur le TP

Brossat Pierrick :

J'ai trouvé ce TP/projet très intéressant, celui-ci est original et permet de mettre en application les choses que l'on a vu durant les TPs d'analyse en python du début du semestre.
Le projet m'a permis de manipuler les fonctions de la librairie cv2 et de comprendre comment marche le traitement d'une image en général.

## Compilation du code

Pour compiler le code : ouvrez un terminal à la racine de l'archive et tapez la commande suivante :

```bash
python puzzle.py
```
