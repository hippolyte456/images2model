import cv2
import numpy as np
import pyvista as pv
from scipy.spatial.transform import Rotation as R


##### GET THE FILTER
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


def compute_projection(image, observer):
    h, w = image.shape
    x, y = np.meshgrid(np.arange(w), np.arange(h))
    z = np.zeros_like(x)
    
    points = np.c_[x.ravel(), y.ravel(), z.ravel()]
    mask = image.ravel() > 0  # Sélectionner uniquement les pixels blancs
    valid_points = points[mask]
    
    projected_points = []
    for (x, y, _) in valid_points:
        projected_points.append([x, y, 0])
    
    return valid_points, np.array(projected_points)


def display_projection(valid_points, projected_points, observer, plotter):
    cloud = pv.PolyData(valid_points)
    plotter.add_mesh(cloud, color='black', point_size=5)
    plotter.add_points(observer, color='red', point_size=20, label='Observer')
    
    for (x, y, _) in valid_points:
        line = pv.Line(observer, [x, y, 0])
        plotter.add_mesh(line, color='black')
    
    poly = pv.PolyData(projected_points)
    plotter.add_mesh(poly.delaunay_2d(), color='gray', opacity=0.5)


def display_3D_space():
    plotter = pv.Plotter()
    
    # for image, distance in zip(images, distances):
    #     observer = get_observer_point(image, distance)
    #     valid_points, projected_points = compute_projection(image, observer)
    #     display_projection(valid_points, projected_points, observer, plotter)
        
    #     new_observer = observer + np.array([0, 0, -distance_offset])
    #     valid_points, projected_points = compute_projection(image, new_observer)
    #     display_projection(valid_points, projected_points, new_observer, plotter)
    
    plotter.show()




if __name__ == "__main__":
        
    # espace 3D à definir 

    #IMAGE1
    # load image
    # binarize image
    # get observer point
    # compute projection

    #IMAGE2
    # load image
    # binarize image
    # get observer point
    # compute projection

    # display 3D space


    image_path1 = "/home/hippolytedreyfus/Documents/images2model/images/cross.png"
    image_path2 = "/home/hippolytedreyfus/Documents/images2model/images/circle.png"
    
    image1 = load_image(image_path1)
    image2 = load_image(image_path2)
    binary_image1 = binarize_image(image1)
    binary_image2 = binarize_image(image2)
    
    display_3D_space([binary_image1, binary_image2], [100, 100], distance_offset=50)

    
