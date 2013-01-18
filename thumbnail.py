#!/usr/bin/python

from PIL import Image
from operator import itemgetter
import sys
import math

def create_image(xsteps, ysteps, steps_x, steps_y, im, im2):
    for y in ysteps:
        for x in xsteps:
            a = x
            b = y
            #print (a, b)
            dest_image_dict = {}
            major_color_index = 0
            #print ((steps+a) , im.size[0] , (steps+b) , im.size[1])
            if ((steps_x+a) < im.size[0] and (steps_y+b) < im.size[1]):
                for i in xrange(steps_x):
                    for j in xrange(steps_y):
                        #print (i, j, a, b)
                        pix = im.getpixel((i+a,j+b))
                        if pix in dest_image_dict:
                            dest_image_dict[pix] += 1
                        else:
                            dest_image_dict[pix] = 1

            for j,k in sorted(dest_image_dict.items(), key=itemgetter(1), reverse=True)[:1]:
                major_color_index = j
                #print (j, k)

            if((a/steps_x) < im2.size[0] and (b/steps_y) < im2.size[1]):
                #print (a/steps_x, b/steps_y)
                im2.putpixel((int(a/steps_x),int(b/steps_y)),major_color_index)

    im2.save("i.gif")
    #print dest_image_dict

    his = im2.histogram()
    values = {}
    for i in range(256):
        values[i] = his[i]

    for j,k in sorted(values.items(), key=itemgetter(1), reverse=True)[:3]:
        print ("******New image major colors*******")
        print j,k

if __name__ == '__main__':
    image = sys.argv[1]
    conx = sys.argv[2]
    cony = sys.argv[3]

    im = Image.open(image)
    im = im.convert("P")

    im2_size = (int(conx), int(cony))
    im2 = Image.new("P", im2_size, 255)

    his = im.histogram()

    print ("original image size: ", im.size)

    values = {}

    print "\n******20 Major colors in original image*****\n"
    for i in range(256):
        values[i] = his[i]
    for j,k in sorted(values.items(), key=itemgetter(1), reverse=True)[:20]:
        print j,k
    print "\n******End original image colors******\n"

    #earlier assumed images to have len.pixel == width.pixel.
    #steps = int(math.sqrt((im.size[0]*im.size[1])/(int(conx)*int(cony))))
    steps_x = im.size[0]/int(conx)
    steps_y = im.size[1]/int(cony)

    print ("Step size for x (aka length): ", steps_x)
    print ("Step size for y (aka width): ", steps_y)

    xsteps = [x*steps_x for x in xrange((im.size[0]/steps_x)+1)]
    ysteps = [y*steps_y for y in xrange((im.size[1]/steps_y)+1)]

    print "Breaking the original image in steps_x and steps_y"
    print xsteps
    print ysteps
    print "\n"

    create_image(xsteps, ysteps, steps_x, steps_y, im, im2)
