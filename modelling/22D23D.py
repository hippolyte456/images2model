import numpy as np
import cv2
import trimesh
from scipy.spatial import ConvexHull
import pdb

def make_allowed_space(image1, image2, coord1, coord2, object_center):
    '''définit un sous espace qui est l'ensemble des points autorisés à remplir, 
    cet espace '''
    #pré-selection de la sphere de centre object_center incluant coord1 et coord2 
    # (pour exclure "l'espace externe" à la scène) ???
    
    return subspace


def minimal_subspace(maximal_subspace, method = 'continuous'):
    '''à partir de l'ensemble des points de l'espace autorisé, proposition d'un objet 3D
    permettant de créer les deux formes complètes'''
    return object3D




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
