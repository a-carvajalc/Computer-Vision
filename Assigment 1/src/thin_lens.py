"""
Thin Lens Equation Functions

This module implements calculations based on the thin lens equation:
    1/f = 1/s_o + 1/s_i

Where:
- f: focal length (lens property)
- s_o: object distance (from object to lens)
- s_i: image distance (from lens to image)

All distances are in the same units (e.g., cm or mm).
"""

def compute_image_distance(focal_length, object_distance):
    if object_distance <= 0:
        raise ValueError("object_distance must be greater than 0")
    try:
        return 1 / (1 / focal_length - 1 / object_distance)
    except ZeroDivisionError:
        raise ValueError("Resulting image distance is undefined")


def compute_focal_length(object_distance, image_distance):
    if object_distance <= 0:
        raise ValueError("object_distance must be greater than 0")
    try:
        return 1 / (1 / object_distance + 1 / image_distance)
    except ZeroDivisionError:
        raise ValueError("Resulting focal length is undefined")


def compute_object_distance(focal_length, image_distance):
    if image_distance == 0:
        raise ValueError("image_distance must be non-zero")
    try:
        return 1 / (1 / focal_length - 1 / image_distance)
    except ZeroDivisionError:
        raise ValueError("Resulting object distance is undefined")


def compute_magnification(object_distance, image_distance):
    if object_distance <= 0:
        raise ValueError("object_distance must be greater than 0")
    try:
        return -image_distance / object_distance
    except ZeroDivisionError:
        raise ValueError("Resulting magnification is undefined")


def lens_type(focal_length):
    if focal_length > 0:
        return "converging"
    elif focal_length < 0:
        return "diverging"
    else:
        raise ValueError("Focal length cannot be zero")


def image_type(image_distance):
    if image_distance > 0:
        return "real"
    elif image_distance < 0:
        return "virtual"
    else:
        return "at_lens"


def image_orientation(magnification):
    if magnification > 0:
        return "upright"
    elif magnification < 0:
        return "inverted"
    else:
        return "no_image"
