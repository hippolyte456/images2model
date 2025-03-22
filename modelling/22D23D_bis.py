import numpy as np
import cv2
from scipy.spatial.transform import Rotation as R
import pdb
import pyvista as pv



def load_binary_image(image_path):
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    return (img > 128).astype(np.uint8)  # Convert to binary mask


def reconstruct_3d(image1, image2, angle):
    h, w = image1.shape
    voxel_grid = np.zeros((h, w, w), dtype=np.uint8)  # 3D voxel space
    
    angle_rad = np.radians(angle)
    rotation_matrix = R.from_euler('y', angle_rad, degrees=False).as_matrix()
    
    for y in range(h):
        for x in range(w):
            if image1[y, x] == 1:
                voxel_grid[y, x, :] = 1  # Extrusion along z
            if image2[y, x] == 1:
                rotated_x, rotated_z = np.dot(rotation_matrix[:2, :2], np.array([x - w//2, w//2]))
                rotated_x = int(rotated_x + w//2)
                rotated_z = int(rotated_z + w//2)
                if 0 <= rotated_x < w and 0 <= rotated_z < w:
                    voxel_grid[y, rotated_x, rotated_z] = 1
    
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


voxel_grid = reconstruct_3d(image1, image2, angle)


plot_3d(voxel_grid)
