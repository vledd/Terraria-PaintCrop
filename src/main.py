from PIL import Image
from constants import *


def process_image_single(src_img: Image, x_tiles_qty: int, y_tiles_qty: int,
                         frame_img: Image = None, frame_size_px: int = 0) -> Image:
    """
    Function to convert + resize single image to the terraria-friendly tiled image.
    You'll need to insert it manually in the place needed
    :param src_img: Input image to process
    :param x_tiles_qty: Amount of X tiles (Image Width)
    :param y_tiles_qty: Amount of Y tiles (Image Height)
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


def count_images_qty(src_tileset: Image,
                     img_tile_xy_qty: tuple[int, int]) -> tuple[int, int]:
    """

    :param src_tileset: image file with all the tiles
    :param img_tile_xy_qty: width and height of one image (object) [in tiles]
    :return: amount of pictures (x * y tiles) in the X and Y axis
    """

    x_size, y_size = src_tileset.size  # Get image size in px
    x_tiles_qty: int = int(x_size / 18 / img_tile_xy_qty[0])
    y_tiles_qty: int = int(y_size / 18 / img_tile_xy_qty[1])

    return x_tiles_qty, y_tiles_qty


def get_image_coords_px_by_tile_coords(tileset: Image,
                                       img_tile_coords: tuple[int, int],
                                       img_tile_xy_qty: tuple[int, int]) -> int or tuple[int, int]:

    max_image_qty: tuple[int, int] = count_images_qty(tileset, img_tile_xy_qty)
    if img_tile_coords[0] not in range(0, max_image_qty[0]) or\
            img_tile_coords[1] not in range(0, max_image_qty[1]):
        return -1

    x_coord_px: int = img_tile_coords[0] * (TILE_SIZE_PX * img_tile_xy_qty[0] + (2 * img_tile_xy_qty[0]))
    y_coord_px: int = img_tile_coords[1] * (TILE_SIZE_PX * img_tile_xy_qty[1] + (2 * img_tile_xy_qty[1]))

    return x_coord_px, y_coord_px


def get_image_coords_px_by_no(tileset: Image,
                              image_no: int,
                              img_tile_xy_qty: tuple[int, int],
                              tiles_order: TilesetTilesOrder) -> int or tuple[int, int]:
    """

    :param tileset:
    :param image_no: STARTS FROM ZERO be careful
    :param img_tile_xy_qty:
    :param tiles_order: TODO maybe auto-detect according to the image aspect ratio
    :return:
    """

    max_image_no: int = count_images_qty(tileset, img_tile_xy_qty)[0] * count_images_qty(tileset, img_tile_xy_qty)[1]

    # TODO we can add additional argument such as "content aware".
    # TODO If true, do not include blank images as a possible values to address.

    if image_no > max_image_no:
        return -1

    # TODO for sure it could be done using some simple formula, need to refactor one time
    no_counter: int = 0
    image_position: list = [0, 0]

    if tiles_order == TilesetTilesOrder.LEFT2RIGHT:
        i_iter: int = 1
        j_iter: int = 0
    else:
        i_iter: int = 0
        j_iter: int = 1

    for i in range(0, count_images_qty(tileset, img_tile_xy_qty)[i_iter]):
        for j in range(0, count_images_qty(tileset, img_tile_xy_qty)[j_iter]):
            if no_counter == image_no:
                image_position[i_iter] = i
                image_position[j_iter] = j
                break
            else:
                no_counter += 1
        else:
            continue
        break

    # print(image_position)

    x_coord = image_position[0] * (TILE_SIZE_PX * img_tile_xy_qty[0] + (2 * img_tile_xy_qty[0]))
    y_coord = image_position[1] * (TILE_SIZE_PX * img_tile_xy_qty[1] + (2 * img_tile_xy_qty[1]))

    return x_coord, y_coord


def is_selected_zone_empty(tileset: Image,
                           xy_coords: tuple[int, int],
                           dimensions: tuple[int, int]) -> bool:
    """
    Helper function to check whether the desired area of image is empty (transparent)
    :param tileset: Image to check
    :param xy_coords: Coordinates to check [px]
    :param dimensions: Dimensions of zone [px]
    :return:
    """

    for i in range(xy_coords[0], dimensions[0] + xy_coords[0]):
        for j in range(xy_coords[1], dimensions[1] + xy_coords[1]):
            if tileset.getpixel((i, j))[3] != 0:
                return False
            else:
                pass

    return True


# tiles = Image.open("./Tiles_240.png")
# print(is_selected_zone_empty(tiles, (280, 1900), (32, 16),))
# print(count_images_qty(tiles, (3, 3)))
# get_image_coords_px_by_no(tiles, 1, (3, 3), TilesetTilesOrder.LEFT2RIGHT)
# print(get_image_coords_px_by_tile_coords(tiles, (2, 1), (3, 3)))

# To be refactored, for testing please uncomment
# src = Image.open("resources/pic/pic1.jpg")
# frame = Image.open("resources/frames/frame1.png")
# process_image_single(src, 2, 3, frame_img=frame, frame_size_px=2).show()
