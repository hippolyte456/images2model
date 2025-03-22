import numpy as np
import cv2
from scipy.spatial.transform import Rotation as R
import pdb
import pyvista as pv



def load_binary_image(image_path):
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    return (img > 128).astype(np.uint8)  # Convert to binary mask


#on prend la premiere image et une distance de vision 
#et on renvoie l'espace autorisé pour que l'observateur voit l'image
def define_first_allowed_space(image1, distance1):
    h, w = image1.shape
    voxel_grid = np.zeros((h, w, w), dtype=np.uint8)  # 3D voxel space
    for y in range(h):
        for x in range(w):
            if image1[y, x] == 1:
                z_index = min(int(distance1 * (w // 100)), w - 1)
                voxel_grid[y, x, z_index] = 1
    return voxel_grid


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


voxel_grid = define_first_allowed_space(image1, 50)


plot_3d(voxel_grid)
