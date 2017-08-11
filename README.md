# captioners
Scripts to add text to images

### captioner.py

applies a black tint and captions a background image

e.g. *with* a logo/trademark

~~~
$ python captioner.py
Enter path of image to caption: in/bkg/bkg9.jpeg
Enter caption: Punching air can be tough
Include logo/trademark? (y/n): y
Output image saved as: out/out.png
~~~
<img src="./figures/fig1.jpg" width="270x" alt="">  <img src="./figures/fig1_capped.png" width="270px" alt="">

input image *bkg9.jpg* and its output *out.png*


e.g. *without* a logo/trademark

~~~
$ python captioner.py
Enter path of image to caption: in/bkg/bkg8.jpg
Enter caption: Look at this empty locker room, i am so inspired.
Include logo/trademark? (y/n): n
Output image saved as: out/out.png
~~~

<img src="./figures/fig2.jpg" width="270x" alt="">  <img src="./figures/fig2_capped.png" width="270px" alt="">

input image *bkg8.jpg* and its output *out.png*

### bulk-captioner.py

captions a number of images
 
__TODO__






