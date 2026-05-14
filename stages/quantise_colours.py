import numpy as np

from config import ALPHA_THRESHOLD


def assign_labels(opaque_pixels, centroids):
    """Finds the centroid closest to each pixel"""
    # opaque_pixels.shape is (num_pixels, 3). centroids.shape is (k, 3). To take norm, the final shape should be (num_pixels, k, 3), one pixel for each k
    opaque_pixels_3d = opaque_pixels[:, np.newaxis]     # new shape (num_pixels, 1, 3)
    centroids_3d = centroids[np.newaxis]                # new shape (1,          k, 3)

    vector_distance = opaque_pixels_3d - centroids_3d   # Shape (num_pixels, k, 3), each value is pixels vector distance to centroid k
    euclid_distances = np.linalg.norm(vector_distance, axis=2)    # Shape (num_pixels, k), each value is euclidean distance of each pixel to centroid k

    closest_centroid_labels = np.argmin(euclid_distances, axis=1)  # Shape (num_pixels), each value is the close centroid for corresponding pixel index

    return closest_centroid_labels


def quantise_colours(pixels, num_colours, max_iterations=100):
    # Opaque mask to neglect transparent pixels
    opaque_mask = pixels[:, :, 3] >= ALPHA_THRESHOLD
    opaque_pixels = pixels[opaque_mask, :3].astype(np.float64)  # Returns flattened array

    unique_colours = np.unique(opaque_pixels, axis=0)
    if len(unique_colours) <= num_colours:
        return pixels
        
    # Initialise centroids
    indices = np.random.choice(len(opaque_pixels), size=num_colours, replace=False)
    centroids = opaque_pixels[indices].copy().astype(np.float64)  # Numpy fancy indexing

    for iteration in range(max_iterations):
        closest_centroid_labels = assign_labels(opaque_pixels, centroids)

        ## Find new centroids based on current clusters
        new_centroids = []
        for k in range(num_colours):
            pixels_assigned_to_k = opaque_pixels[closest_centroid_labels == k]
            if len(pixels_assigned_to_k) > 0:
                new_centroids.append(pixels_assigned_to_k.mean(axis=0))
            else:
                new_centroids.append(centroids[k])  # If the new centroid has no assigned pixels, it uses the old centroid

        new_centroids = np.array(new_centroids)
        
        # If old and new centroids are similar, there is convergence
        if np.allclose(centroids, new_centroids):
            break

        centroids = new_centroids

    # Finding labels with converged centroids
    closest_centroid_labels = assign_labels(opaque_pixels, centroids)
    quantised_rgb = centroids[closest_centroid_labels].round().astype(np.uint8)     # Numpy fancy indexing

    quantised_pixels = pixels.copy()
    quantised_pixels[opaque_mask, :3] = quantised_rgb   # Maps the quantised pixels back into the opaque pixels

    return quantised_pixels
