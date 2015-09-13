import PIL
import Image,ImageDraw,ImageFilter
import random
def setColor():
     return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
w=1000
h = 1000
i=100
im= Image.new("RGB",(w,h),(255,255,255))
#im=Image.open("c:/image.jpg")
l,w=im.size
draw = ImageDraw.Draw(im)
interval = [x*100 for x in range (0,10) if x*100<1001]
for x in interval:
	for y in interval:
		color = setColor()
		for sub_x in range(i):
			for sub_y in range(i):
				draw.point((x+sub_x, y+sub_y), fill=color)
		
        

im.save("image.jpg","jpeg")
