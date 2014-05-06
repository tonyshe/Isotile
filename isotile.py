from PIL import Image
import numpy

def iso_img_gen(color_grid,height_grid,name_str,tile_im,mid_im,bot_im, bg_color = [255, 150, 180]):
	height, width, ___ = color_grid.shape
	#out_im_height = 18*(height+width) + numpy.amax(height_grid)	#sets the height of the finished image. i like to manually change this for animations
	out_im_height = 10*(height+width) + 150
	out_im_width = (width+height+2)*15
	out_im_array = numpy.zeros([out_im_height,out_im_width,3])
	for i in range(int(out_im_height)):
		for j in range(int(out_im_width)):
			out_im_array[i][j] = bg_color

	out_im = Image.fromarray(numpy.uint8(out_im_array))
	for pixel in out_im_array[:][:]:
		pixel = bg_color
	for i in range(height):
		for j in range(width):
			new_tile = color_changer_im(tile_im,color_grid[i][j])	#color change to the RGBA value provided in color_grid
			mid_tile = color_changer_im(mid_im,color_grid[i][j])
			out_im.paste(new_tile, (int(15*(height - i + j)),int(out_im_height-8*(height-i + width-j)-height_grid[i][j]-8)),new_tile)	#overlay w/ transparency
			for k in range(1,int(height_grid[i][j])):	#draws the height of the block
				out_im.paste(mid_tile, (int(15*(height - i + j)),int(out_im_height-8*(height-i + width-j)-height_grid[i][j]+k)),mid_tile)
			out_im.paste(bot_im, (int(15*(height - i + j)),int(out_im_height-8*(height-i + width-j)-height_grid[i][j]+k+1)),bot_im)	#draws the bottom line of the block
	out_im.save(name_str)	#saves the image. make sure name_str contains the filetype extension

def color_changer_im(tile_im, rgba_color):
	alpha_im_data = []
	alpha_image = tile_im.convert("RGBA")	#image.overlay() is possible with an alpha channel
	alpha_im_data = alpha_image.getdata()
	shade = 50	#subtract this value from RGB values. Double on the darkest side
	color_tuple = (int(rgba_color[0]),int(rgba_color[1]),int(rgba_color[2]),int(rgba_color[3]))
	color_tuple_left = (int(rgba_color[0])-shade,int(rgba_color[1])-shade,int(rgba_color[2])-shade,int(rgba_color[3]))
	color_tuple_right = (int(rgba_color[0])-2*shade,int(rgba_color[1])-2*shade,int(rgba_color[2])-2*shade,int(rgba_color[3]))
	new_im = []
	for pixel in alpha_im_data:
		#make sure your image doesn't have "colored" fully-transparent tiles.
		if pixel[0] == 255 and pixel[1] == 0 and pixel[2] == 0:    #check if the pixel is red
			new_im.append(color_tuple)   #replace color
		elif pixel[0] == 0 and pixel[1] == 255 and pixel[2] == 0:    #check if the pixel is green
			new_im.append(color_tuple_left)   #replace color
		elif pixel[0] == 0 and pixel[1] == 0 and pixel[2] == 255:    #check if the pixel is blue
			new_im.append(color_tuple_right)   #replace color
		else:
			new_im.append(pixel)	#otherwise, don't change the tile
	alpha_image.putdata(new_im)
	return alpha_image

def main(tile_im,mid_im,bot_im):
	#write your scripts here. iso_img_gen takes a N x M x 4 numpy array of RGBA values, an N x M array of pixel heights, and a filename string
	color_grid = numpy.zeros([25,25,4])
	height,width, __ = color_grid.shape
	for i in range(height):
		for j in range(width):
			for k in range(3):
				color_grid[i][j][k] = 210
			color_grid[i][j][3] = 255
	
	#sample height map. This is a sine wave
	height_grid = numpy.zeros([25,25])
	for i in range(25):
		for j in range(25):
			height_grid[i][j] = 70 + 50.0 * numpy.sin(2.0*(3.14159/30.0)*(1/2-(abs(i-12)**2 + abs(j-12)**2)**0.5))
	name_str = "wave" + ".png"
	iso_img_gen(color_grid,height_grid,name_str,tile_im,mid_im,bot_im)
	
if __name__ == '__main__':
	#tile image data
	tile_im = Image.open("image_assets/tile_top.png")
	mid_im = Image.open("image_assets/middle.png")
	bot_im = Image.open("image_assets/bottom.png")
	main(tile_im,mid_im,bot_im)