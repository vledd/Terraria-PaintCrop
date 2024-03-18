from PIL import Image
from constants import *


def process_image_single(src_img: Image, x_tiles_qty: int, y_tiles_qty: int,
                         frame_img: Image = None, frame_size_px: int = 0) -> Image:
    """
    Function to convert + resize single image to the terraria-friendly tiled image.
    You'll need to insert it manually in the place needed
    :param src_img: Input image to process
    :param y_tiles_qty: Amount of Y tiles (Image Width)
    :param x_tiles_qty: Amount of X tiles (Image Height)
    :param frame_img: Transparent image of a frame
    :param frame_size_px:
    :return: Processed image
    """

    # Resize the source (input) image to the desired size
    img_resized = src_img.resize((TILE_SIZE_PX * x_tiles_qty - (frame_size_px * 2),
                                 TILE_SIZE_PX * y_tiles_qty - (frame_size_px * 2)),
                                 Image.Resampling.BILINEAR,
                                 None,
                                 3.0)

    # Resize frame input image to the size according to the tiles qty
    frame_img_resized = frame_img.resize((TILE_SIZE_PX * x_tiles_qty,
                                         TILE_SIZE_PX * y_tiles_qty),
                                         Image.Resampling.BILINEAR,
                                         None,
                                         3.0)

    # Image used to merge source image and the frame
    img_merged = Image.new("RGBA",
                           (TILE_SIZE_PX * x_tiles_qty, TILE_SIZE_PX * y_tiles_qty),
                           (255, 255, 255, 0))
    img_merged.paste(img_resized, (frame_size_px, frame_size_px))
    img_merged.paste(frame_img_resized, (0, 0), mask=frame_img_resized)

    # Create a new image (without additional borders since this is a single image function)
    img_out = Image.new("RGBA",
                        ((TILE_SIZE_OFFSET_PX * x_tiles_qty) - 2, (TILE_SIZE_OFFSET_PX * y_tiles_qty) - 2),
                        (255, 255, 255, 0))

    # Copy and paste tiles with 2 transparent pixels offset
    for i in range(0, y_tiles_qty):
        for j in range(0, x_tiles_qty):
            pos_x = TILE_SIZE_PX * i
            pos_y = TILE_SIZE_PX * j
            img_cropped = img_merged.crop((pos_y, pos_x, pos_y + TILE_SIZE_PX, pos_x + TILE_SIZE_PX))
            img_cropped.copy()
            img_out.paste(img_cropped, (pos_y + (2 * j), pos_x + (2 * i)))

    return img_out


# To be refactored, for testing please uncomment
# src = Image.open("resources/pic/pic1.jpg")
# frame = Image.open("resources/frames/frame1.png")
# process_image_single(src, 2, 3, frame_img=frame, frame_size_px=2)
