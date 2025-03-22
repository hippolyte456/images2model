import numpy as np
import cv2
import matplotlib.pyplot as plt

def load_binary_image(image_path):
    """ Charge une image binaire (blanc = opaque, noir = transparent) """
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)  # Charge en niveaux de gris
    _, binary = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)  # Convertir en binaire (0 ou 255)
    return binary

def get_opaque_pixels(binary_img, scale=1.0):
    """ Extrait les pixels blancs (opaques) et les convertit en coordonnées 3D dans le plan y=0 """
    h, w = binary_img.shape
    x_coords, z_coords = np.where(binary_img == 255)  # Indices des pixels blancs
    x_coords = (x_coords - h / 2) * scale  # Mise à l’échelle centrée
    z_coords = (z_coords - w / 2) * scale
    return np.column_stack((x_coords, np.zeros_like(x_coords), z_coords))  # y=0

def is_point_visible(point, observer, opaque_pixels):
    """ Vérifie si un point est visible ou bloqué par un filtre """
    for p in opaque_pixels:
        vec_obs_to_p = p - observer
        vec_obs_to_test = point - observer
        cross_product = np.cross(vec_obs_to_p, vec_obs_to_test)
        if np.linalg.norm(cross_product) < 1e-3:  # Si les points sont alignés
            if np.dot(vec_obs_to_p, vec_obs_to_test) > 0:  # Vérifie si le point est derrière
                return False  # Le point est caché
    return True  # Le point est visible

# Paramètres
image_path = "/home/hippolytedreyfus/Documents/images2model/images/cross.png"  # Image binaire à charger
observer = np.array([0, 2, 0])  # Observateur placé à (x=0, y=2, z=0)
distance_test = 5  # Distance max de projection

# Chargement de l'image et extraction des pixels opaques
binary_img = load_binary_image(image_path)
opaque_pixels = get_opaque_pixels(binary_img, scale=0.1)

# Générer une grille de points de test
test_points = []
for x in np.linspace(-2, 2, 20):
    for z in np.linspace(-2, 2, 20):
        for y in np.linspace(-1, 3, 5):  # Volume test devant et derrière
            test_points.append([x, y, z])

test_points = np.array(test_points)

# Vérification de la visibilité
visible_points = [p for p in test_points if is_point_visible(p, observer, opaque_pixels)]
hidden_points = [p for p in test_points if not is_point_visible(p, observer, opaque_pixels)]

# Affichage
fig = plt.figure(figsize=(10, 6))
ax = fig.add_subplot(111, projection='3d')

# Afficher le filtre
ax.scatter(opaque_pixels[:, 0], opaque_pixels[:, 1], opaque_pixels[:, 2], color='black', label="Filtre (opaque)")

# Afficher les points visibles et cachés
if visible_points:
    visible_points = np.array(visible_points)
    ax.scatter(visible_points[:, 0], visible_points[:, 1], visible_points[:, 2], color='green', label="Visibles")
if hidden_points:
    hidden_points = np.array(hidden_points)
    ax.scatter(hidden_points[:, 0], hidden_points[:, 1], hidden_points[:, 2], color='red', label="Cachés")

# Afficher l'observateur
ax.scatter(observer[0], observer[1], observer[2], color='blue', marker='o', s=100, label="Observateur")

ax.set_xlabel("X")
ax.set_ylabel("Y")
ax.set_zlabel("Z")
ax.legend()
plt.show()
