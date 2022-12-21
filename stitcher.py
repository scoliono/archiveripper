from PIL import Image, UnidentifiedImageError
import os
from natsort import natsorted

def stitch(DIRECTORY, id):
    jpg_files = os.listdir(DIRECTORY)
    jpg_files = natsorted(jpg_files)
    images = []
    for f in jpg_files:
        if f.endswith(".jpg"):
            try:
                images.append(Image.open(DIRECTORY + "/" + f))
            except UnidentifiedImageError:
                print("Error: " + f + " is not a valid image")
                continue
    
    # Reduce the size of the images so the pdf is smaller in size
    for i in range(len(images)):
        images[i] = images[i].resize((int(images[i].size[0] / 2), int(images[i].size[1] / 2)))

    pdf_path = "./" + id + ".pdf"

    images[0].save(
        pdf_path, "PDF" ,resolution=100.0, save_all=True, append_images=images[1:]
    )

    print('Done stitching images to pdf!')

if __name__ == '__main__':
    directory = input("Enter the directory of the images: ")
    id = input("Enter the id of the book: ")
    stitch(directory, id)