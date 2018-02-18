from PIL import Image, ImageDraw, ImageFont, ImageChops
import textwrap
import os

# gives the background image a grayscale to allow easier reading of quote
def apply_tint(im, tint_color):
	tinted_im = ImageChops.multiply(im, Image.new('RGB', im.size, tint_color))
	return tinted_im

# places the trademark logo at the bottom of the image (hardcoded placement)
def place_logo(bkg, logo):
	bkg.paste(logo, ((540-65/2), (1010-65)), logo)
	return bkg

# places the trademark logo at the bottom of the image (hardcoded placement)
def place_trademark(im, trademark, font):
	draw = ImageDraw.Draw(im)
	bbox =  im.getbbox()
	W = bbox[2]
	H = bbox[3]
	draw.text(((W-800/2)/2, 1010), trademark, font=font)
	return im

# places the quote in the centre of the image
def place_quote(im, quote, font):
	draw = ImageDraw.Draw(im)
	w, h = draw.textsize(quote, font=font)
	bbox =  im.getbbox()
	W = bbox[2]; H = bbox[3]

	# determine the number of lines needed to fit the quote on the image
	lines = textwrap.wrap(quote, width=24)
	n_lines = len(lines)
	pad = -10
 
 	# place the lines of the quotes one on top of the other
	current_h = H/2 - (n_lines*h/2)
	for line in lines:
		w, h = draw.textsize(line, font=font)
		draw.text(((W - w) / 2, current_h), line, font=font)
		current_h += h + pad

# determine is the given path is an image
def is_img(path):
	ext = path[-4:]
	if (ext == ".jpg") or (ext == ".png") or (ext == "jpeg"):
		return True
	return False

# gets the paths of the images to be used
def get_im_paths(files):
	pic_paths = []
	for file in files:
		if is_img(file):
			pic_paths.append(file)
	return pic_paths

# reads the quotes from the quotes.txt file 
def get_quotes(file):
	with open(file) as f:
		content = f.readlines()
	return [x.strip() for x in content] 

# creates and saves an image
def build_image(im_path, quote, im_count = '', logoify = True):
	W = H = 1080
	im = Image.open(im_path).resize((W,H))
	im = apply_tint(im, (200,200,200))
	draw = ImageDraw.Draw(im)

	cap_font = ImageFont.truetype("utils/BebasNeue.otf",115)
	place_quote(im, quote, cap_font)

	# if the 'add trademark' option is selected then add the logo and trademark
	if (logoify):
		trademark = "Lifting.Motivations"
		tm_font = ImageFont.truetype("utils/BebasNeue.otf",62)
		place_trademark(im, trademark, tm_font)
		logo = Image.open("utils/logo.png").resize((65,65))
		place_logo(im, logo)

	im.save('out/' + str(im_count) + "_" + str(quote[0:10]) + '.png')
	print "Output image saved as: " + 'out/' + str(im_count) + "_" + str(quote[0:10]) + '.png'


def main():
	dir_paths = os.listdir("../overlayer/in/raw")
	im_paths = get_im_paths(dir_paths)
	quotes = get_quotes("../overlayer/in/quotes.txt")

	combos = (raw_input("Generate all combinations? (y/n): ") == 'y')
	logoify = (raw_input("Include trademark/logo? (y/n): ") == 'y')

	if combos:
		im_count = 0
		for im_path in im_paths:
			for quote in quotes:
				print "Overlaying " + str(im_path) + "..."
				build_image('in/raw/' + im_path, quote, im_count, logoify)
			im_count = im_count + 1
	else:	
		for i, im_path in enumerate(im_paths):
			print "Overlaying " + str(im_path) + "..."
			build_image('in/raw/' + im_path, quotes[i], '', logoify)

main()