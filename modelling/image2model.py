import cv2
import numpy as np
import pyvista as pv

class Space3D:
    def __init__(self):
        self.plotter = pv.Plotter()
        self.images = []  # Stores loaded image information
        self.scene_center = None
    
    def add_image(self, image_path, distance):
        """Adds an image to the 3D space with its projection and relative position."""
        image = self.load_image(image_path)
        binary_image = self.binarize_image(image)
        observer = self.compute_observer(binary_image, distance)
        valid_points = self.compute_projection(binary_image)
        
        self.images.append({
            "path": image_path,
            "distance": distance,
            "observer": observer,
            "valid_points": valid_points
        })
        
        self.add_projection_to_scene(valid_points, observer)
        self.update_scene_center()
    
    def load_image(self, image_path):
        """Loads the image in grayscale."""
        return cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    
    def binarize_image(self, img, threshold=128):
        """Applies binarization to the image."""
        _, binary_img = cv2.threshold(img, threshold, 255, cv2.THRESH_BINARY)
        return binary_img
    
    def compute_observer(self, image, distance):
        """Computes the observer's position based on image size and distance."""
        h, w = image.shape
        return np.array([w / 2, h / 2, -distance])
    
    def compute_projection(self, image):
        """Projects the white pixels of the image onto a 3D plane."""
        h, w = image.shape
        x, y = np.meshgrid(np.arange(w), np.arange(h))
        z = np.zeros_like(x)
        
        points = np.c_[x.ravel(), y.ravel(), z.ravel()]
        mask = image.ravel() > 0  # Select only white pixels
        valid_points = points[mask]
        
        return valid_points
    
    def add_projection_to_scene(self, valid_points, observer):
        """Adds projections and projection lines to the 3D scene."""
        cloud = pv.PolyData(valid_points)
        self.plotter.add_mesh(cloud, color='black', point_size=5)
        self.plotter.add_points(observer, color='red', point_size=20, label='Observer')
        
        for (x, y, _) in valid_points:
            line = pv.Line(observer, [x, y, 0])
            self.plotter.add_mesh(line, color='black')
    
    def update_scene_center(self):
        """Computes and updates the scene center based on image projections."""
        if not self.images:
            return
        
        centers = []
        for img_data in self.images:
            observer = img_data["observer"]
            valid_points = img_data["valid_points"]
            if valid_points.size > 0:
                image_center = np.mean(valid_points, axis=0)
                scene_center = (image_center + observer) / 2
                centers.append(scene_center)
        
        if centers:
            self.scene_center = np.mean(centers, axis=0)
            self.plotter.add_points(self.scene_center, color='blue', point_size=20, label='Scene Center')
    
    def show_scene(self):
        """Displays the 3D scene."""
        self.plotter.show()
    
# Usage example
if __name__ == "__main__":
    space_3d = Space3D()
    space_3d.add_image("/home/hippolytedreyfus/Documents/images2model/images/cross.png", distance=100)
    space_3d.add_image("/home/hippolytedreyfus/Documents/images2model/images/spiral.png", distance=50)
    
    space_3d.show_scene()
