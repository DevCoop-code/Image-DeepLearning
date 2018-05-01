from PIL import Image
import numpy as np
import os, re

search_dir = "./images"
cache_dir = "./images/cache_avhash"

if not os.path.exists(cache_dir):
    os.mkdir(cache_dir)
    
#Convert image data to Average Hash
def average_hash(fname, size = 16):
    fname2 = fname[len(search_dir):]
    #Caching the Image
    cache_file = cache_dir + "/" + fname2.replace('/','_') + ".csv"
    #Making Hash
    if not os.path.exists(cache_file):
        img = Image.open(fname)
        img = img.convert('L').resize((size, size), Image.ANTIALIAS)
        pixels = np.array(img.getdata()).reshape((size, size))
        avg = pixels.mean()
        px = 1 * (pixels > avg)
        np.savetxt(cache_file, px, fmt="%.0f", delimiter=",")
    else:
        px = np.loadtxt(cache_file, delimiter=",")
    return px

#Obtain hamming distance
def hamming_dist(a, b):
    #convert to 1-dimension array
    aa = a.reshape(1, -1)
    ab = b.reshape(1, -1)
    dist = (aa != ab).sum()
    return dist

#Apply all of folders
def enum_all_files(path):
    for root, dirs, files in os.walk(path):
        for f in files:
            fname = os.path.join(root, f)
            if re.search(r'\.(jpg|jpeg|png)$', fname):
                yield fname
                
#Search Image
def find_image(fname, rate):
    src = average_hash(fname)
    for fname in enum_all_files(search_dir):
        dst = average_hash(fname)
        diff_r = hamming_dist(src, dst) / 256
        if diff_r < rate:
            yield(diff_r, fname)
            
# Search
srcfile = search_dir + "/sunflower/image_0016.jpg"
html = ""
sim = list(find_image(srcfile, 0.15))
sim = sorted(sim, key=lambda x:x[0])
for r, f in sim:
    print(r, ">", f)
    s = '<div style="float:left;"><h3>[ Difference :' + str(r) + '-' + \
        os.path.basename(f) + ']</h3>' +\
        '<p><a href="' + f + '"><img src ="' + f + '" width=400>' + \
        '</a></p></div>'
    html += s
    
# Print HTML
html = """<html><head><meta charset="utf8"></head>
<body><h3>Origin Image</h3><p>
<img src='{0}' width=400></p>{1}
</body></html>""".format(srcfile, html)
with open("./avhash-search-output.html", "w", encoding="utf-8") as f:
    f.write(html)
print("OK")