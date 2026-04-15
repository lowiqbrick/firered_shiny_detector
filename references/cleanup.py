import os
import cv2
import numpy as np

if __name__ == "__main__":
    # get paths
    current_directory = os.getcwd() + "/"
    subfolder = "references/"
    reference_folder = current_directory + subfolder

    processed_images = []

    deleted_images = 0

    for filename in os.listdir(reference_folder):
        filepath = reference_folder + filename

        # ignore this file
        if filename == "cleanup.py":
            continue

        # read image data
        # shape: (1080, 1920, 3); height, width, color channels)
        image = cv2.imread(filepath)
        assert image is not None

        # image already seen?
        if any([np.array_equal(image, image_test) for image_test in processed_images]):
            os.remove(filepath)
            deleted_images += 1
            continue

        # add image to list if not yet seen
        processed_images.append(image)

    # print("deleted " + str(deleted_images) + " images")
