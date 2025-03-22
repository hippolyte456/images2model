import numpy as np
import cv2
import trimesh
from scipy.spatial import ConvexHull
import pdb

def silhouette_to_3d(image_path, angle):
    """
    Convertit une silhouette 2D en un ensemble de points 3D projetés selon un angle donné.

    Paramètres :
    ------------
    image_path : str
        Chemin de l'image en noir et blanc (forme blanche sur fond noir).
    angle : float
        Angle de rotation en radians autour de l'axe Y.

    Retourne :
    ----------
    np.ndarray
        Tableau (N, 3) des points 3D projetés.

    """
    # Charger l'image en noir et blanc
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    _, binary = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY_INV)

    # Trouver les contours des formes
    contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Créer les points du cône en 3D
    points_3d = []
    for cnt in contours:
        for pt in cnt:
            x, y = pt[0]
            # Convertir en coordonnées 3D en fonction de l'angle
            X = x * np.cos(angle)
            Y = y
            Z = x * np.sin(angle)
            points_3d.append([X, Y, Z])

    return np.array(points_3d)



image1_path = "/home/hippolytedreyfus/Documents/images2model/images/image_circle.png"
image2_path = "/home/hippolytedreyfus/Documents/images2model/images/image_square.png"

# Charger deux images et créer les deux ensembles de points 3D
points1 = silhouette_to_3d(image1_path, np.radians(0))
points2 = silhouette_to_3d(image2_path, np.radians(45))

pdb.set_trace()
# Fusionner les points et calculer l'enveloppe convexe
all_points = np.vstack([points1, points2])
hull = ConvexHull(all_points)

# Convertir en maillage Trimesh et exporter en STL
mesh = trimesh.Trimesh(vertices=all_points[hull.vertices], faces=hull.simplices)
mesh.export("output.stl")
