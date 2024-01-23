import cv2
import numpy as np

def removeBackgroundFromImageWithSolidBG(image):
    # Convert the image to grayscale
    grayScaleImage = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Convert the grayscale image to binary image
    # 120 is the threshold value which is used to classify the pixel values
    # If pixel value is below 120, it is considered as black, else it is considered as white
    # 255 is the max value/o0uu
    _, thresholdImage = cv2.threshold(grayScaleImage, 245, 255, cv2.THRESH_BINARY)
    cv2.imshow("Threshold Image", thresholdImage)
    cv2.waitKey(0)
    # Find the contours
    contours, hierarchy = cv2.findContours(thresholdImage, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    # Create a mask with the largest contour
    mask = np.zeros(image.shape, np.uint8)
    # cv2.drawContours(mask, [max(contours, key=cv2.contourArea)], -1, (255, 255, 255), -1)

    # Create a image with the foreground pixels set to zero
    imageWithBGRemoved = cv2.bitwise_not(image, mask)
    cv2.imshow("Image with Background Removed", imageWithBGRemoved)
    cv2.waitKey(0)
    return imageWithBGRemoved

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
new_color_img = replace_transparent_with_color(bg, new_color=(255, 0, 255, 255))
cv2.imwrite("test_bg_removed.png", new_color_img)
# image = cv2.imread(image_path)
# image = removeBackgroundFromImageWithSolidBG(image)
# cv2.imwrite("test_bg_removed.jpg", image)