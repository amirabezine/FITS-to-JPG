import numpy as np
from astropy.io import fits
from PIL import Image , ImageFilter

def normalize(array, scaling='log', factor=1000):
    """Normalize the image array to [0, 255]"""
    if scaling == 'log':
        # Apply a logarithmic scaling
        scaled_array = np.log10(1 + factor * array)
        array_min, array_max = np.min(scaled_array), np.max(scaled_array)
        return ((scaled_array - array_min) / (array_max - array_min) * 255).astype(np.uint8)
    else:
        # Apply a linear scaling
        array_min, array_max = np.min(array), np.max(array)
        return ((array - array_min) / (array_max - array_min) * 255).astype(np.uint8)

def combine_channels(r, g, z):
    """Combine the three channels into a single RGB image"""
    return np.stack([r, g, z], axis=-1)

def main():
    # Read the individual FITS files
    with fits.open('img_r.fits') as hdulist:
        img_r = hdulist[0].data
    with fits.open('img_g.fits') as hdulist:
        img_g = hdulist[0].data
    with fits.open('img_z.fits') as hdulist:
        img_z = hdulist[0].data

    # Normalize each channel to [0, 255]
    img_r_normalized = normalize(img_r * 1.2)
    img_g_normalized = normalize(img_g * 1.2)
    img_z_normalized = normalize(img_z * 1.2)

    # Combine the channels to form an RGB image
    rgb_image = combine_channels(img_r_normalized, img_g_normalized, img_z_normalized)

    # Create a PIL Image object and save as JPEG
    output_image = Image.fromarray(rgb_image)
    output_image.save('output.jpg')

       # Create a PIL Image object and save as JPEG
    output_image = Image.fromarray(rgb_image)
    
    # Apply an unsharp mask filter for sharpening
    unsharp_mask = ImageFilter.UnsharpMask(radius=2, percent=150, threshold=3)
    sharpened_image = output_image.filter(unsharp_mask)
    
    # Save the sharpened image
    sharpened_image.save('output_sharpened.jpg')


if __name__ == '__main__':
    main()
