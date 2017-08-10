from PIL import Image, ImageDraw, ImageFont, ImageChops
import textwrap

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
	## TODO fix hardcode
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

def main():
	W = H = 1080
	im = Image.open("in/bkg.jpg").resize((W,H))
	im = apply_tint(im, (200,200,200))
	draw = ImageDraw.Draw(im)

	cap = "Whatever you do, do it for yourself."
	cap_font = ImageFont.truetype("utils/BebasNeue.otf",115)
	place_caption(im, cap, cap_font)

	trademark = "Lifting.Motivations"
	tm_font = ImageFont.truetype("utils/BebasNeue.otf",62)
	place_trademark(im, trademark, tm_font)

	logo = Image.open("utils/logo.png").resize((65,65))
	place_logo(im, logo)

	im.save('out/out.png')

main()