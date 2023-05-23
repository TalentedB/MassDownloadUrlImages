# importing libraries
import os
import argparse
from time import sleep
import requests
from PIL import Image


def Download(link: str, output_path: str = 'image.jpg') -> bool:

    with open(output_path, 'wb') as handle:
        response = requests.get(link, stream=True)
        if not response.ok:
            print("ERROR: Could not download image")
            print(response)
            return False

        for block in response.iter_content(1024):
            if not block:
                break

            handle.write(block)
    return True


def ResizeImage(image_path: str, width: int = 516, height: int = 516):
    image = Image.open(image_path)
    resized_image = image.resize((int(width), int(height)))
    resized_image.save(image_path)


def main():
    parser = argparse.ArgumentParser(description='Download Images from URLS automatically')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--file', '-f', metavar='<file path>', help='Path of the file containing the urls')
    group.add_argument('--url', '-u', metavar='<url>', help='URL of the image to download')
    parser.add_argument('--output', '-o', metavar='<output path>', help='Path to the output location')
    parser.add_argument('--res', '-r', metavar='<widthxheight>', help='Resolution of the image to download')
    args = parser.parse_args()

    output_path = args.output or "images/"
    if not os.path.exists(output_path):
        os.makedirs(output_path)
    try:
        width = args.res.split('x')[0] or 516
        height = args.res.split('x')[1] or 516
    except:
        width = 516
        height = 516


    if args.file:
        # Process file
        downloadedImages = []
        with open(args.file) as f:
            urls = f.readlines()
            for i in range(len(urls)):
                urls[i] = urls[i].strip()
                print("Downloading image from url: " + urls[i])
                if Download(urls[i], output_path + str(i) + ".jpg"):
                    downloadedImages.append(output_path + str(i) + ".jpg")  # Add to list of downloaded images 

        # Resize images
        #  TODO: Add resizing functionality
        for image in downloadedImages:
            print("Resizing image: " + image)
            ResizeImage(image_path=image, width=width, height=height)

    elif args.url:
        # Process URL
        print("Downloading image from url: " + args.url)
        Download(args.url, output_path + "1.jpg")
        ResizeImage("testimage.jpg", width=width, height=height)



if __name__ == '__main__':
	main()















