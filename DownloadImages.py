# importing libraries
import os
import argparse
from time import sleep
import requests
from PIL import Image

#Download a image directly from a url to that image
def Download(link: str, output_path: str = 'image.jpg') -> bool:
    #Open a file at output path
    with open(output_path, 'wb') as handle:
	#Create a request for the image 
        response = requests.get(link, stream=True)
	#If request failed
        if not response.ok:
            print("ERROR: Could not download image")
            print(response)
            return False
	#Write the image to the file
        for block in response.iter_content(1024):
            if not block:
                break
            handle.write(block)
    #Return True since image was downloaded correctly
    return True

#Resize any image to a specific width and height
def ResizeImage(image_path: str, width: int = 516, height: int = 516) -> None:
    try:
		#Open Image Path as a PIL object
		image = Image.open(image_path)
		#Resize Image
		resized_image = image.resize((int(width), int(height)))
		#Overwrite Original Image
		resized_image.save(image_path)
	except:
		print("Failed to resize given image")

#Resize any image to a specific width and height
def CropImage(image_path: str, startx: int = 0, starty: int = 0 width: int = 516, height: int = 516) -> None:
    try:
		#Open Image Path as a PIL object
		image = Image.open(image_path)
		#Resize Image
		resized_image = image.crop((int(startx), int(starty), int(width), int(height)))
		#Overwrite Original Image
		resized_image.save(image_path)
	except:
		print("Failed to resize given image")

#Main Function
def main():
	#CLI creation
    parser = argparse.ArgumentParser(description='Download Images from URLS automatically')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--file', '-f', metavar='<file path>', help='Path of the file containing the urls')
    group.add_argument('--url', '-u', metavar='<url>', help='URL of the image to download')
    parser.add_argument('--output', '-o', metavar='<output path>', help='Path to the output location')
    parser.add_argument('--res', '-r', metavar='<widthxheight>', help='Resolution of the image to download')
	parser.add_argument('--type', '-t', metavar='<file type>', help='File type of output image ex: "jpg"')
    args = parser.parse_args()
	
	#Create valid inputs
    output_path = args.output or "images/"
    if not os.path.exists(output_path):
        os.makedirs(output_path)

	if args.res:
		width = args.res.split('x')[0]
		height = args.res.split('x')[1]
	
	file_type = args.type or "jpg"
	file_type = "." + file_type
	
	#If Given File Path Proccess all the URL's in that file
    if args.file:
        # Process file
        downloadedImages = []
        with open(args.file) as f:
            urls = f.readlines()
            for i in range(len(urls)):
                urls[i] = urls[i].strip()
                print("Downloading image from url: " + urls[i])
                if Download(urls[i], output_path + str(i) + file_type):
                    downloadedImages.append(output_path + str(i) + file_type)  # Add to list of downloaded images 
		
		
        # Resize images
		if args.res:
			for image in downloadedImages:
				print("Resizing image: " + image)
				ResizeImage(image_path=image, width=width, height=height)
				
	#Download Single Image From URL
    elif args.url:
        # Process URL
        print("Downloading image from url: " + args.url)
        Download(args.url, output_path + "1" + file_type)
		if args.res:
        	ResizeImage(output_path + "1" + file_type, width=width, height=height)
	else:
		#! Should never get here
		raise Exception("Invalid: Must Choose MULTIPLE or SINGULAR")



if __name__ == '__main__':
	main()















