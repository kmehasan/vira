import cv2
import numpy as np

def remove_background(image_path, smoothing_radius=1):
    # Read the image
    img = cv2.imread(image_path)

    # Convert the image to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Threshold the image to create a binary mask
    _, mask = cv2.threshold(gray, 245, 255, cv2.THRESH_BINARY)
    # Apply GaussianBlur to the mask for smoothing
    mask = cv2.GaussianBlur(mask, (smoothing_radius, smoothing_radius), 0)

    # Invert the mask
    inverted_mask = cv2.bitwise_not(mask)

    # Apply the inverted mask to the original image
    result = cv2.bitwise_and(img, img, mask=inverted_mask)

    # Add an alpha channel to the original image
    img_with_alpha = cv2.cvtColor(img, cv2.COLOR_BGR2BGRA)

    # Apply the inverted mask to the alpha channel
    img_with_alpha[:, :, 3] = inverted_mask

    return img_with_alpha
def replace_transparent_with_color(img, new_color=(255, 0, 0, 255), feathering_radius=7):
    # Read the image with an alpha channel
    # img = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)
# Extract the alpha channel
    alpha_channel = img[:, :, 3]
# Create a mask for non-transparent regions
    non_transparent_mask = alpha_channel > 0

    # Create a feathering mask
    feathering_mask = cv2.GaussianBlur(non_transparent_mask.astype(np.float32), (feathering_radius, feathering_radius), 0)

    # Normalize the feathering mask
    feathering_mask /= feathering_mask.max()

    # Create a new image with the desired color
    new_image = np.ones_like(img) * new_color  # Set alpha value to 0 (fully transparent)

    # Replace non-transparent regions with the desired color, applying feathering
    new_image[non_transparent_mask] = img[non_transparent_mask]
    new_image[:, :, 3] = (1 - feathering_mask) * new_image[:, :, 3] + feathering_mask * img[:, :, 3]
    return new_image

image_path = "test.jpg"
bg = remove_background(image_path)
cv2.imwrite("test_bg_removed.png", bg)
new_color_img = replace_transparent_with_color(bg, new_color=(227,219,171, 255))
cv2.imwrite("test_bg_changed.png", new_color_img)
# image = cv2.imread(image_path)
# image = removeBackgroundFromImageWithSolidBG(image)
# cv2.imwrite("test_bg_removed.jpg", image)