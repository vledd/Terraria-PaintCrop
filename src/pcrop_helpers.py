import glob
import os
import sys

from PIL import Image
from constants import *


# TODO we can refactor it using named tuples, would be much better

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


def process_image_single(src_img: Image,
                         img_tile_xy_qty: tuple[int, int],
                         frame_img: Image = None,
                         frame_size_px: int = 0) -> Image:
    """
    Function to convert + resize single image to the terraria-friendly tiled image.
    You'll need to insert it manually in the place needed
    :param src_img: Input image to process
    :param img_tile_xy_qty: Amount of X and Y tiles (Image Width and Height)
    :param frame_img: Transparent image of a frame
    :param frame_size_px:
    :return: Processed image
    """

    # Resize the source (input) image to the desired size
    img_resized = src_img.resize((TILE_SIZE_PX * img_tile_xy_qty[0] - (frame_size_px * 2),
                                 TILE_SIZE_PX * img_tile_xy_qty[1] - (frame_size_px * 2)),
                                 Image.Resampling.BILINEAR,
                                 None,
                                 3.0)

    # Image used to merge source image and the frame
    img_merged = Image.new("RGBA",
                           (TILE_SIZE_PX * img_tile_xy_qty[0], TILE_SIZE_PX * img_tile_xy_qty[1]),
                           (255, 255, 255, 0))
    img_merged.paste(img_resized, (frame_size_px, frame_size_px))

    if frame_img is not None:
        # Resize frame input image to the size according to the tiles qty
        frame_img_resized = frame_img.resize((TILE_SIZE_PX * img_tile_xy_qty[0],
                                              TILE_SIZE_PX * img_tile_xy_qty[1]),
                                             Image.Resampling.BILINEAR,
                                             None,
                                             3.0)
        img_merged.paste(frame_img_resized, (0, 0), mask=frame_img_resized)

    # Create a new image (without additional borders since this is a single image function)
    img_out = Image.new("RGBA",
                        ((TILE_SIZE_OFFSET_PX * img_tile_xy_qty[0]) - 2,
                         (TILE_SIZE_OFFSET_PX * img_tile_xy_qty[1]) - 2),
                        (255, 255, 255, 0))

    # Copy and paste tiles with 2 transparent pixels offset
    for i in range(0, img_tile_xy_qty[1]):
        for j in range(0, img_tile_xy_qty[0]):
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
    """
    This function gets image upper-left coordinates by the relative coordinates of the image in tileset
    :param tileset: Tileset which contains the image
    :param img_tile_coords: Coordinates of the image in tileset (relative, not in pixels, but in images)
    :param img_tile_xy_qty: Amount of tiles in image
    :return: tuple with x and y coordinates
    """

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
    This function returns the upper-left coordinates of an image in tileset by its number
    :param tileset: Tileset containing image
    :param image_no: STARTS FROM ZERO be careful
    :param img_tile_xy_qty: Amount of tiles in image
    :param tiles_order: How to count number of images (left to right or up to down)
    :return: tuple with image coordinates [px]
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
    :return: is the image is empty (transparent)
    """

    for i in range(xy_coords[0], dimensions[0] + xy_coords[0]):
        for j in range(xy_coords[1], dimensions[1] + xy_coords[1]):
            if tileset.getpixel((i, j))[3] != 0:
                return False
            else:
                pass

    return True


def process_and_replace_image_in_tileset_by_no(tileset: Image,
                                               image_no: int,
                                               src_image: Image,
                                               img_tile_xy_qty: tuple[int, int],
                                               tiles_order: TilesetTilesOrder,
                                               frame_img: Image = None,
                                               frame_size_px: int = 0) -> Image:
    """
    This function creates a processed (split and crop) image and pastes it in the tileset.
    :param tileset:
    :param image_no:
    :param src_image:
    :param img_tile_xy_qty:
    :param tiles_order:
    :param frame_img:
    :param frame_size_px:
    :return:
    """

    # Acquire a processed image first. FIXME it was edited, please double check
    # img_to_replace = process_image_single(src_image, img_tile_xy_qty, frame_img, frame_size_px)
    # Paste it where desired
    tileset.paste(src_image,
                  get_image_coords_px_by_no(tileset,
                                            image_no,
                                            img_tile_xy_qty,
                                            tiles_order))

    return tileset


def batch_process_replace_images_in_tileset_by_no(src_path: str,
                                                  tileset: Image,
                                                  images_no: list,
                                                  img_tile_xy_qty: tuple[int, int],
                                                  tiles_order: TilesetTilesOrder,
                                                  frame_img: Image = None,
                                                  frame_size_px: int = 0) -> Image:
    """
    Unused for now. Probably needs refactoring from scratch.
    :param src_path:
    :param tileset:
    :param images_no:
    :param img_tile_xy_qty:
    :param tiles_order:
    :param frame_img:
    :param frame_size_px:
    :return:
    """

    entries_list = sorted(glob.glob(os.path.join(src_path, "*.jpg")) + glob.glob(os.path.join(src_path, "*.png")))

    # FIXME check for sizes missmatch (not enough photos etc.)
    for i in range(0, len(images_no)):
        src_image = Image.open(entries_list[i])
        tileset = process_and_replace_image_in_tileset_by_no(tileset,
                                                             images_no[i],
                                                             src_image,
                                                             img_tile_xy_qty,
                                                             tiles_order,
                                                             frame_img,
                                                             frame_size_px)
        src_image.close()

    return tileset


def create_preview_multiple_images(images_list: list[Image]) -> Image:
    preview_x_size: int = 0
    preview_y_size: int = images_list[0].size[1] + 2

    for img in images_list:
        preview_x_size += img.size[0] + 2  # Just spacing

    preview_img = Image.new("RGBA",
                            (preview_x_size, preview_y_size),
                            (255, 255, 255, 0))

    current_x_pos: int = 0

    for i in range(0, len(images_list)):
        preview_img.paste(images_list[i], (current_x_pos, 0))
        current_x_pos += images_list[i].size[0] + 2

    return preview_img


def get_image_no_by_coords(tileset: Image,
                           img_tile_xy_qty: tuple[int, int],
                           coords: tuple[int, int],
                           tiles_order: TilesetTilesOrder) -> int:
    """
    Function to retrieve image number by the coordinates on the tileset [px]
    :param tileset:
    :param img_tile_xy_qty:
    :param coords:
    :param tiles_order:
    :return:
    """

    images_qty: tuple[int, int] = count_images_qty(tileset, img_tile_xy_qty)
    image_no: int = 0

    if tiles_order == TilesetTilesOrder.LEFT2RIGHT:
        i_iter: int = 1
        j_iter: int = 0
    else:
        i_iter: int = 0
        j_iter: int = 1

    for i in range(0, images_qty[i_iter]):
        for j in range(0, images_qty[j_iter]):
            # TODO Dirty hack. Please edit later
            x_pos: int = (i if j_iter == 1 else j) * TILE_SIZE_OFFSET_PX * img_tile_xy_qty[0]
            y_pos: int = (j if i_iter == 0 else i) * TILE_SIZE_OFFSET_PX * img_tile_xy_qty[1]
            # print(x_pos, end=" ")
            # print(y_pos)
            if x_pos <= coords[0] < x_pos + TILE_SIZE_OFFSET_PX * img_tile_xy_qty[0] and \
                    y_pos <= coords[1] < y_pos + TILE_SIZE_OFFSET_PX * img_tile_xy_qty[1]:
                # print("Found")
                break
            else:
                image_no += 1
        else:
            continue
        break
    # print(image_no)
    return image_no


def extract_image_from_tileset_by_no(tileset: Image,
                                     image_no: int,
                                     img_tile_xy_qty: tuple[int, int],
                                     tiles_order: TilesetTilesOrder) -> Image:
    """
    Returns a cropped image from the tileset
    :param tileset: Tileset containing the image
    :param image_no: Image number
    :param img_tile_xy_qty: Amount of tiles in the image
    :param tiles_order:
    :return: Extracted region (as PIL Image)
    """
    x_coord, y_coord = get_image_coords_px_by_no(tileset,
                                                 image_no,
                                                 img_tile_xy_qty,
                                                 tiles_order)
    x_box = x_coord + (img_tile_xy_qty[0] * TILE_SIZE_OFFSET_PX)
    y_box = y_coord + (img_tile_xy_qty[1] * TILE_SIZE_OFFSET_PX)

    region_cropped = tileset.crop((x_coord, y_coord, x_box, y_box))

    return region_cropped
