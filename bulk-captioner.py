from PIL import Image, ImageDraw, ImageFont, ImageChops
import textwrap
import os

def apply_tint(im, tint_color):
	tinted_im = ImageChops.multiply(im, Image.new('RGB', im.size, tint_color))
	return tinted_im


def place_logo(bkg, logo):
	bkg.paste(logo, ((540-65/2), (1010-65)), logo)
	return bkg


def place_trademark(im, trademark, font):
	draw = ImageDraw.Draw(im)
	bbox =  im.getbbox()
	W = bbox[2]
	H = bbox[3]
	draw.text(((W-800/2)/2, 1010), trademark, font=font)
	return im


def place_caption(im, cap, font):
	draw = ImageDraw.Draw(im)
	w, h = draw.textsize(cap, font=font)
	bbox =  im.getbbox()
	W = bbox[2]
	H = bbox[3]

	lines = textwrap.wrap(cap, width=24)
	n_lines = len(lines)
	pad = -10
 
	current_h = H/2 - (n_lines*h/2)
	for line in lines:
		w, h = draw.textsize(line, font=font)
		draw.text(((W - w) / 2, current_h), line, font=font)
		current_h += h + pad


def is_img(path):
	ext = path[-4:]
	if (ext == ".jpg") or (ext == ".png") or (ext == "jpeg"):
		return True
	return False


def get_im_paths(files):
	pic_paths = []
	for file in files:
		if is_img(file):
			pic_paths.append(file)
	return pic_paths


def get_captions(file):
	with open(file) as f:
		content = f.readlines()
	return [x.strip() for x in content] 


def caption_image(im_path, cap, im_count = '', logoify = True):
	W = H = 1080
	im = Image.open(im_path).resize((W,H))
	im = apply_tint(im, (200,200,200))
	draw = ImageDraw.Draw(im)

	cap_font = ImageFont.truetype("utils/BebasNeue.otf",115)
	place_caption(im, cap, cap_font)

	if (logoify):
		trademark = "Lifting.Motivations"
		tm_font = ImageFont.truetype("utils/BebasNeue.otf",62)
		place_trademark(im, trademark, tm_font)
		logo = Image.open("utils/logo.png").resize((65,65))
		place_logo(im, logo)

	im.save('out/' + str(im_count) + "_" + str(cap[0:10]) + '.png')
	print "Output image saved as: " + 'out/' + str(im_count) + "_" + str(cap[0:10]) + '.png'


def main():
	dir_paths = os.listdir("../captioners/in/bkg")
	im_paths = get_im_paths(dir_paths)
	caps = get_captions("../captioners/in/cap.txt")

	permute = (raw_input("Generate all permutations? (y/n): ") == 'y')
	logoify = (raw_input("Include trademark/logo? (y/n): ") == 'y')

	if permute:
		im_count = 0
		for im_path in im_paths:
			for cap in caps:
				print "Captioning " + str(im_path) + "..."
				caption_image('in/bkg/' + im_path, cap, im_count, logoify)
			im_count = im_count + 1
	else:	
		for i, im_path in enumerate(im_paths):
			print "Captioning " + str(im_path) + "..."
			caption_image('in/bkg/' + im_path, caps[i], '', logoify)

main()