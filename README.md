
## Formalisme V1

L'objectif du projet est de trouver une fonction qui, 
(INPUT)  étant donné 2 images 2D (en noir et blanc...) 
 et 2 points de l'espace 3D, dont doivent être vu respectivement ces deux images.

 OUTPUT : renvoie la (ou les) structure(s) 3D possible qui permettent d'observer ces deux images selon les points définit.


 --> puis a faire rentrer dnas une imprimante 3D


## Formalisme V2
On cherche à inverser le processus de projection d'une forme 3D sur deux plans de l'espace.

On part de deux images (2D) en noir et blanc (de même taille / nombre de pixels).
On considère que ces deux images sont le résultat de la projection d'une forme 3D selon deux points de vue différents. (L'angle entre les deux points de vue correspond à une rotation dans l'espace 3D d'une image par rapport à l'autre autour de leur axe vertical passant par le centre des images.)
On cherche une forme 3D (ou l'ensemble des formes 3D) qui soit compatibles avec ces deux projections.
Dans ces images 2D, un pixel blanc indique la projection de l'objet et un pixel noir indique l'absence de l'objet.

Les inputs sont donc :
Les deux images en noir et blanc.
L'angle entre les deux points de vue.

L'output attendu est :
Un modèle 3D ou l'ensemble des points de l'espace qu'il faut "remplir" pour obtenir les deux images par projections.

https://www.thingiverse.com/ 