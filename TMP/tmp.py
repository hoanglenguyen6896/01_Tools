#!python

# # Importing Image class from PIL module
# from PIL import Image

# # Opens a image in RGB mode
# im = Image.open("E:/Learning/00_Git/01_Tools/TMP/1.jpg")

# # Setting the points for cropped image
# left = 0
# top = 0
# right = 500
# bottom = 200

# # Cropped image of above dimension
# # (It will not change original image)
# im1 = im.crop((left, top, right, bottom))

# # Shows the image in image viewer
# im1.show()

# h = 800
# h_cfg = 788

def ccc(h, h_cfg):
    t = int((h - h_cfg)/2)
    b = int((h + h_cfg)/2)
    print('---------------')
    print(t, b, b - t)

    if abs(t - b) != h_cfg:
        print(1)
        b = h_cfg - t

    print(t, b, b - t)
    print('---------------')

for i in range(600, 800):
    ccc(800, i)