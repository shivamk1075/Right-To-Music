import numpy as np
from PIL import Image

# ConvertSpectrogramToImage converts a spectrogram to a heat map image
def SpectrogramToImage(spectrogram, output_path):
    num_windows = len(spectrogram)
    num_freq_bins = len(spectrogram[0])

    # Create an empty grayscale image
    img = Image.new('L', (num_freq_bins, num_windows))

    # Scale the values in the spectrogram to the range [0, 255]
    max_magnitude = 0.0
    for i in range(num_windows):
        for j in range(num_freq_bins):
            magnitude = abs(spectrogram[i][j])
            if magnitude > max_magnitude:
                max_magnitude = magnitude

    # Convert spectrogram values to pixel intensities
    pixels = []
    for i in range(num_windows):
        row = []
        for j in range(num_freq_bins):
            magnitude = abs(spectrogram[i][j])
            intensity = int(np.floor(255 * (magnitude / max_magnitude)))
            row.append(intensity)
        pixels.append(row)

    # Set the pixels to the image
    img.putdata([item for sublist in pixels for item in sublist])

    # Save the image to the specified path
    img.save(output_path)


