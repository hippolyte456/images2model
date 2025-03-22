import cv2
import numpy as np
import pyvista as pv
from scipy.spatial.transform import Rotation as R

def load_image(image_path):
    # Charger l'image en niveaux de gris
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    return img

def binarize_image(img, threshold=128):
    # Appliquer la binarisation
    _, binary_img = cv2.threshold(img, threshold, 255, cv2.THRESH_BINARY)
    return binary_img

def get_observer_point(image, distance):
    h, w = image.shape
    observer = np.array([w / 2, h / 2, -distance])
    return observer

def display_image_3d(image, observer, title="Image 3D"):
    h, w = image.shape
    x, y = np.meshgrid(np.arange(w), np.arange(h))
    z = np.zeros_like(x)
    
    points = np.c_[x.ravel(), y.ravel(), z.ravel()]
    mask = image.ravel() > 0  # Sélectionner uniquement les pixels blancs
    valid_points = points[mask]
    
    cloud = pv.PolyData(valid_points)
    
    plotter = pv.Plotter()
    plotter.add_mesh(cloud, color='black', point_size=5)
    plotter.add_points(observer, color='red', point_size=20, label='Observer')
    
    # Tracer les droites de projection pour tous les points binarisés
    projected_points = []
    for (x, y, _) in valid_points:
        line = pv.Line(observer, [x, y, 0])
        plotter.add_mesh(line, color='black')
        projected_points.append([x, y, 0])
    
    # Remplir le volume intérieur en gris
    projected_points = np.array(projected_points)
    poly = pv.PolyData(projected_points)
    plotter.add_mesh(poly.delaunay_2d(), color='gray', opacity=0.5)
    
    plotter.show(title=title)

# Exemple d'utilisation
image_path =  "/home/hippolytedreyfus/Documents/images2model/images/cross.png"
image = load_image(image_path)
binary_image = binarize_image(image)
observer_point = get_observer_point(binary_image, distance=100)

display_image_3d(binary_image, observer_point, "Image en 3D")
