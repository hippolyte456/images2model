import numpy as np
import cv2
from scipy.spatial.transform import Rotation as R
import pdb
import pyvista as pv



def load_binary_image(image_path):
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    return (img > 128).astype(np.uint8)  # Convert to binary mask


def make_allowed_space(image1, image2, distance1, distance2, angle):
    h, w = image1.shape
    voxel_grid = np.zeros((h, w, w), dtype=np.uint8)  # 3D voxel space
    
    angle_rad = np.radians(angle)
    rotation_matrix = R.from_euler('y', angle_rad, degrees=False).as_matrix()
    
    for y in range(h):
        for x in range(w):
            if image1[y, x] == 1:
                z_index = min(int(distance1 * (w // 100)), w - 1)
                voxel_grid[y, x, z_index] = 1
            if image2[y, x] == 1:
                rotated_x, rotated_z = np.dot(rotation_matrix[:2, :2], np.array([x - w//2, w//2]))
                rotated_x = int(rotated_x + w//2)
                rotated_z = min(int(distance2 * (w // 100)), w - 1)
                if 0 <= rotated_x < w:
                    voxel_grid[y, rotated_x, rotated_z] = 1
    
    return voxel_grid

# def make_allowed_space(image1, image2, distance1, distance2, angle):
#     """
#     Définit un sous-espace contenant l'ensemble des points autorisés à remplir,
#     en fonction des deux images projetées, des distances aux images et de l'angle entre elles.
    
#     :param image1: Première image binaire (vue 1).
#     :param image2: Deuxième image binaire (vue 2).
#     :param distance1: Distance de la caméra 1 à son plan image.
#     :param distance2: Distance de la caméra 2 à son plan image.
#     :param angle: Angle entre les deux caméras en degrés.
#     :return: Un volume 3D indiquant les points remplissables.
#     """
#     h, w = image1.shape
#     voxel_grid = np.zeros((h, w, w), dtype=np.uint8)  # Espace 3D initialisé
    
#     # Transformation de la deuxième vue dans le même repère que la première
#     angle_rad = np.radians(angle)
#     rotation_matrix = R.from_euler('y', angle_rad, degrees=False).as_matrix()
    
#     for y in range(h):
#         for x in range(w):
#             # Si le pixel appartient à image1, on remplit la ligne de profondeur selon distance1
#             if image1[y, x] == 1:
#                 voxel_grid[y, x, int(distance1 * (w // 2))] = 1
            
#             # Si le pixel appartient à image2, on le projette avec l'angle
#             if image2[y, x] == 1:
#                 rotated_x, rotated_z = np.dot(rotation_matrix[:2, :2], np.array([x - w//2, distance2]))
#                 rotated_x = int(rotated_x + w//2)
#                 rotated_z = int(rotated_z + w//2)
                
#                 if 0 <= rotated_x < w and 0 <= rotated_z < w:
#                     voxel_grid[y, rotated_x, rotated_z] = 1
    
#     # Intersection des espaces autorisés
#     return voxel_grid

# def make_allowed_space(image1, image2, distance1, distance22, angle):
#     '''définit un sous espace qui est l'ensemble des points autorisés à remplir, 
#     cet espace '''
    #pré-selection de la sphere de centre object_center incluant coord1 et coord2 
    # (pour exclure "l'espace externe" à la scène) ??? 
    # return subspace


def plot_3d(voxel_grid):
    x, y, z = np.where(voxel_grid == 1)
    cloud = pv.PolyData(np.c_[x, y, z])
    plotter = pv.Plotter()
    plotter.add_mesh(cloud, color='black', point_size=5, render_points_as_spheres=True)
    plotter.show()



image1_path = "/home/hippolytedreyfus/Documents/images2model/images/cross.png"
image2_path = "/home/hippolytedreyfus/Documents/images2model/images/circle.png"


# Exemple d'utilisation
image1 = load_binary_image(image1_path)
image2 = load_binary_image(image2_path)
angle = 30  # Angle en degrés


voxel_grid = make_allowed_space(image1, image2 , distance1= 60, distance2= 90, angle=angle)


plot_3d(voxel_grid)
