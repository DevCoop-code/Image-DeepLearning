from PIL import Image
import numpy as np

# Change the image data to use Average Hash
def average_hash(fname, size = 16):
    #open the image data
    img = Image.open(fname)
    #Convert to grayscale
    img = img.convert('L')
    #Resize
    img = img.resize((size, size), Image.ANTIALIAS)
    #Get the pixel data
    pixel_data = img.getdata()
    #Convert to numpy array
    pixels = np.array(pixel_data)
    #Convert to 2-dimen array
    pixels = pixels.reshape((size, size))
    #Get the Average
    avg = pixels.mean()
    #If the data is bigger than avg, the value is 1. opposite is 0
    diff = 1 * (pixels > avg)
    return diff

# Convert to Binary Hash
def np2hash(ahash):
    bhash = []
    for nl in ahash.tolist():
        s1 = [str(i) for i in nl]
        s2 = "".join(s1)
        #convert the binary data to integer data
        i = int(s2, 2)
        bhash.append("%04x" % i)
    return "".join(bhash)

#Print the Average Hash
ahash = average_hash('ssamba_hong.jpg')
print(ahash)
print(np2hash(ahash))