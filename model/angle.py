import cv2 as cv
import numpy as np
import math

def compute_middle_point(point1, point2):
    x = (point1[0] + point2[0]) / 2
    y = (point1[1] + point2[1]) / 2
    return np.array([x, y])

def compute_line_angle(point1, point2):
    dx = point2[0] - point1[0]
    dy = point2[1] - point1[1]
    angle = np.arctan2(dy, dx) * 180 / math.pi
    return angle

def compute_angle(screen):
    # Convert PIL image to OpenCV-compatible format (NumPy array)
    opencv_image = cv.cvtColor(np.array(screen), cv.COLOR_RGB2BGR)

    # Convert the OpenCV image to grayscale
    gray_image = cv.cvtColor(opencv_image, cv.COLOR_BGR2GRAY)

    # Denoise with threshold
    arrow = cv.threshold(gray_image, 150, 255, 0)
    _, binary_image = arrow

    # Find contours in the binary image
    contours, _ = cv.findContours(binary_image, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

    if not contours:
        # couldn't find arrow
        return None

    # Find the largest contour
    largest_contour = max(contours, key=cv.contourArea)

    # Create a mask for the largest contour
    mask = cv.drawContours(np.zeros_like(binary_image), [largest_contour], 0, (255), thickness=cv.FILLED)

    # Denoise with mask
    extracted_image = cv.bitwise_and(gray_image, gray_image, mask=mask)

    # Model as triangle
    triangle = cv.minEnclosingTriangle(largest_contour)

    # Get the vertices of the triangle
    pt1, pt2, pt3 = triangle[1]
    pt1 = pt1[0]
    pt2 = pt2[0]
    pt3 = pt3[0]

    side_lengths = [np.linalg.norm(pt2 - pt3), np.linalg.norm(pt1 - pt3), np.linalg.norm(pt1 - pt2)]
    acute_index = side_lengths.index(min(side_lengths))

    points = [pt1,pt2,pt3]
    vertex_point = points.pop(acute_index)
    base_point1, base_point2 = points

    base_point = compute_middle_point(base_point1, base_point2)

    angle = compute_line_angle(base_point, vertex_point)
    # opencv flips y axis for some reason
    angle = angle * -1
    return angle

