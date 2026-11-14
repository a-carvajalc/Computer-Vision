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

# TODO: Implement the following functions


def compute_image_distance(focal_length, object_distance):
    """
    Compute image distance using the thin lens equation.
    
    Given the focal length and object distance, calculate where the image forms.
    
    Args:
        focal_length (float): Focal length of the lens in cm
            - Positive: converging (convex) lens
            - Negative: diverging (concave) lens
        object_distance (float): Distance from object to lens in cm (must be > 0)
    
    Returns:
        float: Image distance in cm
            - Positive: real image (on opposite side of lens from object)
            - Negative: virtual image (on same side as object)
    
    Raises:
        ValueError: If object_distance <= 0 or if result is undefined
    
    Formula: 1/s_i = 1/f - 1/s_o
    
    Example:
        >>> compute_image_distance(focal_length=10, object_distance=30)
        15.0  # Real image at 15 cm
        
        >>> compute_image_distance(focal_length=-10, object_distance=20)
        -6.666...  # Virtual image (diverging lens)
    """
    if object_distance <= 0:
        raise ValueError("object_distance must be greater than 0")
    try:
        return 1 / (1 / focal_length - 1 / object_distance)
    except ZeroDivisionError:
        raise ValueError("Resulting image distance is undefined")


def compute_focal_length(object_distance, image_distance):
    """
    Compute focal length from object and image distances.
    
    Args:
        object_distance (float): Distance from object to lens in cm (must be > 0)
        image_distance (float): Distance from lens to image in cm
    
    Returns:
        float: Focal length in cm
            - Positive: converging lens
            - Negative: diverging lens
    
    Raises:
        ValueError: If distances are invalid
    
    Formula: 1/f = 1/s_o + 1/s_i
    
    Example:
        >>> compute_focal_length(object_distance=30, image_distance=15)
        10.0
    """
    if object_distance <= 0:
        raise ValueError("object_distance must be greater than 0")
    try:
        return 1 / (1 / object_distance + 1 / image_distance)
    except ZeroDivisionError:
        raise ValueError("Resulting focal length is undefined")


def compute_object_distance(focal_length, image_distance):
    """
    Compute object distance from focal length and image distance.
    
    Args:
        focal_length (float): Focal length of the lens in cm
        image_distance (float): Distance from lens to image in cm
    
    Returns:
        float: Object distance in cm (will be > 0 for real objects)
    
    Raises:
        ValueError: If distances are invalid
    
    Formula: 1/s_o = 1/f - 1/s_i
    
    Example:
        >>> compute_object_distance(focal_length=10, image_distance=15)
        30.0
    """
    if image_distance == 0:
        raise ValueError("image_distance must be non-zero")
    try:
        return 1 / (1 / focal_length - 1 / image_distance)
    except ZeroDivisionError:
        raise ValueError("Resulting object distance is undefined")


def compute_magnification(object_distance, image_distance):
    """
    Compute magnification of the image.
    
    Magnification describes how much larger or smaller the image is compared to the object,
    and whether it's upright or inverted.
    
    Args:
        object_distance (float): Distance from object to lens in cm (must be > 0)
        image_distance (float): Distance from lens to image in cm
    
    Returns:
        float: Magnification factor
            - Positive: image is upright
            - Negative: image is inverted
            - |m| > 1: image is magnified (larger)
            - |m| < 1: image is reduced (smaller)
            - |m| = 1: image is same size
    
    Formula: m = -s_i / s_o
    
    Example:
        >>> compute_magnification(object_distance=30, image_distance=15)
        -0.5  # Inverted, reduced
        
        >>> compute_magnification(object_distance=15, image_distance=30)
        -2.0  # Inverted, magnified
    """
    if object_distance <= 0:
        raise ValueError("object_distance must be greater than 0")
    try:
        return -image_distance / object_distance
    except ZeroDivisionError:
        raise ValueError("Resulting magnification is undefined")


def lens_type(focal_length):
    """
    Classify lens type based on focal length.
    
    Args:
        focal_length (float): Focal length in cm
    
    Returns:
        str: Either "converging" (f > 0) or "diverging" (f < 0)
    
    Example:
        >>> lens_type(focal_length=10)
        'converging'
        
        >>> lens_type(focal_length=-15)
        'diverging'
    """
    if focal_length > 0:
        return "converging"
    elif focal_length < 0:
        return "diverging"
    else:
        raise ValueError("Focal length cannot be zero")


def image_type(image_distance):
    """
    Classify image type based on image distance.
    
    Args:
        image_distance (float): Distance from lens to image in cm
    
    Returns:
        str: Either "real" (s_i > 0) or "virtual" (s_i < 0) or "at_lens" (s_i = 0)
    
    Example:
        >>> image_type(15)
        'real'
        
        >>> image_type(-6.67)
        'virtual'
    """
    if image_distance > 0:
        return "real"
    elif image_distance < 0:
        return "virtual"
    else:
        return "at_lens"


def image_orientation(magnification):
    """
    Determine image orientation based on magnification.
    
    Args:
        magnification (float): Magnification factor m
    
    Returns:
        str: Either "upright" (m > 0) or "inverted" (m < 0) or "no_image" (m = 0)
    
    Example:
        >>> image_orientation(-0.5)
        'inverted'
        
        >>> image_orientation(0.333)
        'upright'
    """
    if magnification > 0:
        return "upright"
    elif magnification < 0:
        return "inverted"
    else:
        return "no_image"
