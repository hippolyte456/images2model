import numpy as np
import trimesh

# Définition de l'observateur
observer = np.array([0, 0, 5])  # Position (x, y, z)

# Création d'un filtre (un plan vertical)
filter_mesh = trimesh.creation.box(extents=[4, 0.1, 4])  # Un plan fin simulé comme une boîte
filter_mesh.apply_translation([0, 0, 2])  # Déplacer le filtre devant l'observateur

# Générer des points aléatoires dans l’espace
num_points = 100
space_points = np.random.uniform(-3, 3, size=(num_points, 3))
space_points[:, 2] = np.random.uniform(0, 6, num_points)  # Z entre 0 et 6

# Vérification de la visibilité
ray_origins = np.tile(observer, (num_points, 1))  # L'observateur envoie des rayons vers chaque point
ray_directions = space_points - ray_origins  # Vecteurs directionnels

# Tester les intersections avec le filtre
intersections, index_ray, _ = filter_mesh.ray.intersects_location(ray_origins, ray_directions, multiple_hits=False)

# Déterminer quels points sont cachés
hidden_points = set(index_ray)  # Index des points qui ont été bloqués

# Séparer les points visibles et cachés
visible_points = [p for i, p in enumerate(space_points) if i not in hidden_points]
hidden_points = [p for i, p in enumerate(space_points) if i in hidden_points]

# Affichage des résultats
print(f"Nombre de points testés : {num_points}")
print(f"Nombre de points visibles : {len(visible_points)}")
print(f"Nombre de points cachés : {len(hidden_points)}")

# Visualisation avec trimesh
scene = trimesh.Scene()
scene.add_geometry(filter_mesh)

# Ajouter les points visibles (en vert) et cachés (en rouge)
scene.add_geometry(trimesh.points.PointCloud(np.array(visible_points), colors=[0, 255, 0]))  # Vert
scene.add_geometry(trimesh.points.PointCloud(np.array(hidden_points), colors=[255, 0, 0]))  # Rouge

scene.show()
