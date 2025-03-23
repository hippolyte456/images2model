import cv2
import numpy as np
import pyvista as pv

def load_image(image_path):
    """Charge l'image en niveaux de gris."""
    return cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

def binarize_image(img, threshold=128):
    """Applique la binarisation sur l'image."""
    _, binary_img = cv2.threshold(img, threshold, 255, cv2.THRESH_BINARY)
    return binary_img

def get_observer_point(image, distance):
    """Calcule le point d'observation en fonction de la taille de l'image et de la distance."""
    h, w = image.shape
    return np.array([w / 2, h / 2, -distance])

def compute_projection(image, observer):
    """Projette les points blancs de l'image sur un plan 3D."""
    h, w = image.shape
    x, y = np.meshgrid(np.arange(w), np.arange(h))
    z = np.zeros_like(x)
    
    points = np.c_[x.ravel(), y.ravel(), z.ravel()]
    mask = image.ravel() > 0  # Sélectionner uniquement les pixels blancs
    valid_points = points[mask]
    
    return valid_points

def add_projection_to_scene(plotter, valid_points, observer):
    """Ajoute les projections et les lignes de projection dans la scène 3D."""
    cloud = pv.PolyData(valid_points)
    plotter.add_mesh(cloud, color='black', point_size=5)
    plotter.add_points(observer, color='red', point_size=20, label='Observer')
    
    for (x, y, _) in valid_points:
        line = pv.Line(observer, [x, y, 0])
        plotter.add_mesh(line, color='black')


def main():
    plotter = pv.Plotter()
    
    # IMAGE 1
    image_path1 = "/home/hippolytedreyfus/Documents/images2model/images/cross.png"
    image1 = load_image(image_path1)
    binary_image1 = binarize_image(image1)
    observer1 = get_observer_point(binary_image1, 100)
    valid_points1 = compute_projection(binary_image1, observer1)
    add_projection_to_scene(plotter, valid_points1, observer1)
    # plotter.show(interactive_update=True)  # Mise à jour interactive de la scène
    
    # IMAGE 2
    image_path2 = "/home/hippolytedreyfus/Documents/images2model/images/cross.png"
    image2 = load_image(image_path2)
    binary_image2 = binarize_image(image2)
    observer2 = get_observer_point(binary_image2, 50)
    valid_points2 = compute_projection(binary_image2, observer2)
    add_projection_to_scene(plotter, valid_points2, observer2)
    
    plotter.show()

if __name__ == "__main__":
    main()
