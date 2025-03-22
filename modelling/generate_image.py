import numpy as np
import cv2

def generate_binary_images(size=100, save_path="/home/hippolytedreyfus/Documents/images2model/images/"):
    image1 = np.zeros((size, size), dtype=np.uint8)
    image2 = np.zeros((size, size), dtype=np.uint8)
    
    # Dessiner une croix sur image1
    image1[size//4:3*size//4, size//2 - 5:size//2 + 5] = 1
    image1[size//2 - 5:size//2 + 5, size//4:3*size//4] = 1
    
    # Dessiner une diagonale sur image2
    for i in range(size):
        if 10 < i < size - 10:
            image2[i, i] = 1
            image2[i, size - i - 1] = 1
    
    # Enregistrer les images
    cv2.imwrite(save_path + "image1.png", image1 * 255)
    cv2.imwrite(save_path + "image2.png", image2 * 255)
    
def generate_complex_binary_images(size=100, save_path="/home/hippolytedreyfus/Documents/images2model/images/"):
    image1 = np.zeros((size, size), dtype=np.uint8)
    image2 = np.zeros((size, size), dtype=np.uint8)
    
    # Image 1 : Labyrinthe (chemin sinueux)
    for i in range(10, size-10, 10):
        if i % 20 == 0:
            image1[i, 10:size-10] = 1  # Ligne horizontale
        else:
            image1[10:size-10, i] = 1  # Ligne verticale
    
    # Image 2 : Spirale logarithmique
    center = (size // 2, size // 2)
    a, b = 5, 0.2  # Paramètres de la spirale
    theta = np.linspace(0, 4 * np.pi, num=500)  # Angle
    r = a * np.exp(b * theta)  # Rayon
    x = (center[0] + r * np.cos(theta)).astype(int)
    y = (center[1] + r * np.sin(theta)).astype(int)
    
    valid_idx = (x >= 0) & (x < size) & (y >= 0) & (y < size)
    image2[x[valid_idx], y[valid_idx]] = 1

    # Enregistrer les images
    cv2.imwrite(save_path + "image1_maze.png", image1 * 255)
    cv2.imwrite(save_path + "image2_spiral.png", image2 * 255)



generate_complex_binary_images()
