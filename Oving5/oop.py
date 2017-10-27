import os
path = "C:/Users/wgkva/NTNU/OneDrive - NTNU/Datateknologi/2. klasse/TDT4113 - Programmeringsprosjekt/TDT4113/Oving5/images"
os.chdir(path)

from PIL import Image, ImageEnhance, ImageOps, ImageFilter

class Davinci:

    def __init__(self, path1, path2, path3, path4, path5, path6):
        self.path1 = path1
        self.path2 = path2
        self.path3 = path3
        self.path4 = path4
        self.path5 = path5
        self.path6 = path6

        self.image1 = Image.open(path1)
        self.image2 = Image.open(path2)
        self.image3 = Image.open(path3)
        self.image4 = Image.open(path4)
        self.image5 = Image.open(path5)
        self.image6 = Image.open(path6)

        self.listofimages = []

    def blur(self):
        blured = self.image1.filter(ImageFilter.GaussianBlur(radius=10))
        self.listofimages.append(blured)

    def rotate(self, degrees):
        rotated = self.image2.rotate(degrees)
        self.listofimages.append(rotated)

    def change_exposure(self, amount):
        exposured = self.image3.point(lambda x: x * amount)
        self.listofimages.append(exposured)

    def change_contrast(self, amount):
        contrasted = ImageEnhance.Contrast(self.image4).enhance(amount)
        self.listofimages.append(contrasted)

    def make_it_grey(self):
        gray = self.image5.convert('LA')
        self.listofimages.append(gray)

    def invert_colors(self):
        inverted = ImageOps.invert(self.image6)
        self.listofimages.append(inverted)



    def create_collage(self, width = 900, height=600):
        cols, rows = 3, 2

        thumbnail_width = width//cols
        thumbnail_height = height//rows
        size = thumbnail_width, thumbnail_height

        collage = Image.new('RGB', (width, height))
        images = []
        for im in self.listofimages:
            im.thumbnail(size)
            images.append(im)
        i = 0
        x = 0
        y = 0
        for col in range(cols):
            for row in range(rows):
                collage.paste(images[i], (x,y))
                i += 1
                y += thumbnail_height
            x += thumbnail_width
            y = 0

        collage.save('collage.jpeg')
        collage = Image.open('collage.jpeg')
        collage.show()

def main():
    imo1 = 'library.jpeg'
    imo2 = 'kdfinger.jpeg'
    imo3 = 'fisheggs.jpeg'
    imo4= 'brain.jpeg'
    imo5 = 'campus.jpeg'
    imo6 = 'northernlights.jpeg'

    artist = Davinci(imo1,imo2,imo3,imo4,imo5,imo6)

    artist.blur()
    artist.rotate(90)
    artist.change_exposure(0.5)
    artist.change_contrast(2)
    artist.invert_colors()
    artist.make_it_grey()
    artist.create_collage(1800,1200)

main()