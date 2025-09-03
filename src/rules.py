from PIL import Image

# 5 rules 
# - format: is it a PNG, JPEG --> reject if not this format 
# - minimum image size for GIF : is it a small GIF --> reject if it exceeds certain dimension
# - minimum size for image: min size is a square for an image --> anything less is rejected
# - ratio size: is the ratio size of the image too small or too big --> requires further review if image is not inbetween the ratio. Image could be cut off or too small for advert or outdoor advertisement.
# - contrast/brightness of image - images that are too dark or low in contrast will be flagged up as review. 

def format_checker(image: Image.Image) -> tuple[str, list[str]]:
    allowedFormats = ["PNG", "JPEG"]
    reasons= []
    if image.format not in allowedFormats:
        reasons.append(f"This format is unsupported: {image.format}. Only PNG and JPED supported")
        return "REJECTED", reasons

    return "APPROVED", reasons

def gif_size_checker(image: Image.Image, fileSizeBytes: int) -> tuple[str, list[str]]:
    reasons: list[str] = []

    if image.format == "GIF":
        maxWidth= 150  
        maxHeight = 150
        maxBytes = 150_000
        if image.width > maxWidth or image.height > maxHeight:
            reasons.append(f"GIF dimensions is too big: {image.width}x{image.height}")
        if fileSizeBytes > maxBytes:
            reasons.append(f"GIF file size too big: {fileSizeBytes} bytes")

        if reasons:
            return "REJECTED", reasons

    return "APPROVED", reasons

def minimum_image_size(image: Image.Image) -> tuple[str, list[str]]:
    minWidth = 300
    minHeight = 250
    reasons= []
    if image.width < minWidth or image.height < minHeight:
        reasons.append(f"This image is too small: {image.width}x{image.height}")
        return "REJECTED", reasons

    return "APPROVED", reasons

def check_ratio_size(image: Image.Image) -> tuple[str, list[str]]:
    minRatio = 0.7
    maxRatio = 2.5
    reasons= []
    ratio = image.width/image.height
    if ratio < minRatio:
        reasons.append(f"The ratio of the image ({ratio:.2f}) is below the minimum allowed (0.7)")
        return "REQUIRES_REVIEW", reasons   
    elif ratio > maxRatio:
        reasons.append(f"The ratio of the image ({ratio:.2f}) exceeds the maximum allowed (2.5)")
        return "REQUIRES_REVIEW", reasons
    
    return "APPROVED", reasons

def check_legality_and_contrast(image: Image.Image) -> tuple[str, list[str]]:
    reasons = []
    grayscale = image.convert("L")
    pixels = list(grayscale.getdata())
    
    minPixel = min(pixels)
    maxPixel = max(pixels)
    contrast = maxPixel - minPixel

    meanBrightness = sum(pixels) / len(pixels)
    if meanBrightness < 40:
        reasons.append(f"Image is very dark (mean brightness: {meanBrightness:.1f})")
    
    if contrast < 30:  # adjust threshold based on testing
        reasons.append(f"Image has low contrast ({contrast:.1f})")

    if reasons:
        return "REQUIRES_REVIEW", reasons

    return "APPROVED", reasons
