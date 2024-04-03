# How to use PaintCrop v1.0

After opening the program, the main window will appear.
![scr_1.png](resources%2Freadme%2Fscr_1.png)

On the left side, there is two main subframes. **Image preview** is where the user can see 
how input pictures were processed (they will look exactly the same after export).

**Tileset preview** allows user to insert processed frames right into PaintCrop.
This will be explained below.

## Loading images to process
First of all, the user needs to select images to work with. This is done by clicking the "..." 
button near "Path to one or multiple images" label.
Your system explorer will open, allowing you to select one or more images to process.

After doing that, you'll see them loaded into the **Image preview** frame.
Adjust them with "Painting tiles quantity" spinboxes to the desired size (it should correspond 
to the images size in the game). You can use mouse wheel for that.

After such manipulations, you'll receive something like this
![scr_2.png](resources%2Freadme%2Fscr_2.png)

*You can additionally add frames, but beware that this is a demo feature.* 
*Your frame should correspond to the resulting size of the image, otherwise it will be* 
*resized to fit*

If you're OK with the result already, and you want to replace pictures manually, 
for example, using Photoshop, press "Export Image(s) as .PNG", select folder and get 
your processed images for your needs.

Also, you can edit your tileset right in this program. For that, press "..." near the
"Tileset path (optional)" label and load your tileset in *.png* format.

After that, click on any image in the "Image preview" frame, it should be painted red.
Then use your left mouse button to paste this image right onto the tileset. Right mouse 
button will remove this image from the tileset.
![scr_3.png](resources%2Freadme%2Fscr_3.png)
When you will be satisfied with the result, press "Export tileset as .png" and you are good to go.
This file can easily be injected into the game like any resource pack.