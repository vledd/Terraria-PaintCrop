# import warnings
# warnings.filterwarnings("ignore", category=DeprecationWarning)

from gui_main import Ui_MainScreen
# from gui_second import Ui_SecondScreen

from PyQt6 import QtCore as qtc
from PyQt6 import QtGui as qtg
from PyQt6 import QtWidgets as qtw

from PIL import Image, ImageDraw
from PIL.ImageQt import ImageQt

import pcrop_helpers as pcrop
import os


# class SettingsScreenWindow(qtw.QMainWindow):
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.ui = Ui_SecondScreen()
#         self.ui.setupUi(self)


class MainScreenWindow(qtw.QMainWindow):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.frame = None
        self.tileset_pth = None
        self.images_pth = None

        self.preview_tileset_layer0: Image = None
        self.preview_tileset_layer1: Image = None

        self.preview_image: Image = None
        self.selected_image_preview: Image = None
        self.selected_image_preview_temp: Image = None
        self.tiles_qty: list[int, int] = [1, 1]

        self.ui = Ui_MainScreen()
        self.ui.setupUi(self)

        self.ui.img_path_btn.clicked.connect(self.get_image_path)
        self.ui.tile_path_btn.clicked.connect(self.get_tileset_path)
        self.ui.frame_path_btn.clicked.connect(self.get_frame_path)
        self.ui.export_single_png_btn.clicked.connect(self.process_save_to_folder)
        self.ui.export_tileset_btn.clicked.connect(self.tileset_save)

        self.ui.tile_qty_xspin.valueChanged.connect(self.update_x_tiles_qty)
        self.ui.tile_qty_yspin.valueChanged.connect(self.update_y_tiles_qty)

        self.ui.tileset_pixmap_lbl.mousePressEvent = self.tileset_pixmap_clicked
        self.ui.img_preview_pixmap_lbl.mouseDoubleClickEvent = self.img_preview_pixmap_clicked

    def update_x_tiles_qty(self, event):
        self.tiles_qty[0] = int(event)
        if self.images_pth is not None:
            self.process_preview()

    def update_y_tiles_qty(self, event):
        self.tiles_qty[1] = int(event)
        if self.images_pth is not None:
            self.process_preview()

    def get_image_path(self):
        self.images_pth = qtw.QFileDialog.getOpenFileNames(self, "Select Files", filter="Image files (*.jpg *.png)")
        if len(self.images_pth[0]) == 0:
            self.ui.img_path_line.setText("No valid file provided!")
            self.ui.img_preview_pixmap_lbl.setEnabled(False)
            self.images_pth = None
            self.selected_image_preview = None
            self.selected_image_preview_temp = None
            self.ui.export_single_png_btn.setEnabled(False)
        else:
            self.ui.img_path_line.setText(str(self.images_pth[0]))
            self.ui.img_preview_pixmap_lbl.setEnabled(True)
            self.ui.export_single_png_btn.setEnabled(True)
            self.process_preview()

    def get_tileset_path(self):
        self.tileset_pth = qtw.QFileDialog.getOpenFileName(self, "Select Files", filter="Tileset (*.png)")
        if len(self.tileset_pth[0]) == 0:
            self.ui.tile_path_line.setText("No valid tileset provided!")
            self.ui.export_tileset_btn.setEnabled(False)
            self.ui.tileset_pixmap_lbl.setEnabled(False)
        else:
            self.ui.tile_path_line.setText(str(self.tileset_pth[0]))
            self.ui.export_tileset_btn.setEnabled(True)
            self.ui.tileset_pixmap_lbl.setEnabled(True)
            self.preview_tileset_layer0 = Image.new("RGBA", Image.open(self.tileset_pth[0]).size)
            tileset_img = ImageQt(Image.open(self.tileset_pth[0]))
            self.ui.tileset_pixmap_lbl.setPixmap(qtg.QPixmap.fromImage(tileset_img))

    def get_frame_path(self):
        self.frame = qtw.QFileDialog.getOpenFileName(self, "Select Files", filter="Frame (*.png)")
        if len(self.frame[0]) == 0:
            self.ui.frame_path_line.setText("No valid frame provided!")
            self.ui.add_frame_chk.setEnabled(False)
            self.ui.add_frame_chk.setChecked(False)
            self.ui.frame_thick_spin.setEnabled(False)
        else:
            self.ui.frame_path_line.setText(str(self.frame[0]))
            self.ui.add_frame_chk.setEnabled(True)
            self.ui.frame_thick_spin.setEnabled(True)

    def process_images(self):
        frame_thick = self.ui.frame_thick_spin.value()
        if self.ui.add_frame_chk.isChecked():
            src_frame = Image.open(self.frame[0])
        else:
            src_frame = None

        src_img_list: list = []

        if len(self.images_pth[0]) == 1:
            src_img = Image.open(str(self.images_pth[0][0]))

            src_img_list.append(pcrop.process_image_single(src_img,
                                                           (self.tiles_qty[0], self.tiles_qty[1]),
                                                           src_frame,
                                                           frame_thick))
        else:
            for i in range(0, len(self.images_pth[0])):
                img_local = Image.open(self.images_pth[0][i])
                # Todo frames
                src_img_list.append(pcrop.process_image_single(img_local, (self.tiles_qty[0], self.tiles_qty[1]),
                                                               src_frame,
                                                               frame_thick))
                img_local.close()

        return src_img_list

    def process_preview(self):
        processed_img = ImageQt(pcrop.create_preview_multiple_images(self.process_images()))
        self.ui.img_preview_pixmap_lbl.setPixmap(qtg.QPixmap.fromImage(processed_img))
        self.preview_image = pcrop.create_preview_multiple_images(self.process_images())


    def tileset_save(self):
        if self.tileset_pth is None:
            return

        tileset_local: Image = Image.open(self.tileset_pth[0])
        tileset_local.paste(self.preview_tileset_layer0, (0, 0), mask=self.preview_tileset_layer0)
        save_path = qtw.QFileDialog.getSaveFileName(self,
                                                           "Select directory where to save tileset",
                                                           filter="Tileset (*.png)")

        if save_path[0] == "":
            qtw.QMessageBox.warning(self, "Export warning", "Please select a valid folder!")
        else:
            tileset_local.save(save_path[0])
            qtw.QMessageBox.information(self, "Export status", "Tileset exported OK!")

    def process_save_to_folder(self):
        save_folder_path = qtw.QFileDialog.getExistingDirectory(self, "Select directory where to save")

        if save_folder_path == "":
            qtw.QMessageBox.warning(self, "Export warning", "Please select a valid folder!")
        else:
            processed_img_list = self.process_images()
            for i in range(0, len(processed_img_list)):
                processed_img_list[i].save(f"{save_folder_path}/export_{i}.png")
            qtw.QMessageBox.information(self, "Export status", "Image(s) exported OK!")

    def tileset_pixmap_clicked(self, event):
        # TODO finish feature
        if self.selected_image_preview is None:
            return

        tileset_local: Image = Image.open(self.tileset_pth[0])

        selection_no: int = pcrop.get_image_no_by_coords(tileset_local,
                                                         (self.tiles_qty[0], self.tiles_qty[1]),
                                                         (event.pos().x(), event.pos().y()),
                                                         pcrop.TilesetTilesOrder.LEFT2RIGHT)

        if event.button() == qtg.QMouseEvent.button(event).LeftButton:
            self.preview_tileset_layer0 = (
                pcrop.process_and_replace_image_in_tileset_by_no(self.preview_tileset_layer0,
                                                                 selection_no,
                                                                 self.selected_image_preview,
                                                                 (self.tiles_qty[0], self.tiles_qty[1]),
                                                                 pcrop.TilesetTilesOrder.LEFT2RIGHT,
                                                                 None, 0))  # Todo add frame

        elif event.button() == qtg.QMouseEvent.button(event).RightButton:
            eraser_img = Image.new("RGBA",
                                   (self.tiles_qty[0] * pcrop.TILE_SIZE_OFFSET_PX,
                                    self.tiles_qty[1] * pcrop.TILE_SIZE_OFFSET_PX),
                                   (0, 0, 0, 0))

            self.preview_tileset_layer0 = (
                pcrop.process_and_replace_image_in_tileset_by_no(self.preview_tileset_layer0,
                                                                 selection_no,
                                                                 eraser_img,
                                                                 (self.tiles_qty[0], self.tiles_qty[1]),
                                                                 pcrop.TilesetTilesOrder.LEFT2RIGHT,
                                                                 None, 0))

        temp_tilseset_preview: Image = tileset_local
        temp_tilseset_preview.paste(self.preview_tileset_layer0, (0, 0), mask=self.preview_tileset_layer0)
        temp_tilseset_preview_qt = ImageQt(temp_tilseset_preview)
        self.ui.tileset_pixmap_lbl.setPixmap(qtg.QPixmap.fromImage(temp_tilseset_preview_qt))

    def img_preview_pixmap_clicked(self, event):
        selection_no: int = pcrop.get_image_no_by_coords(self.preview_image,
                                                         (self.tiles_qty[0], self.tiles_qty[1]),
                                                         (event.pos().x(), event.pos().y()),
                                                         pcrop.TilesetTilesOrder.LEFT2RIGHT)
        self.selected_image_preview = self.process_images()[selection_no]

        self.selected_image_preview_temp = Image.new("RGBA",
                                                     (self.tiles_qty[0] * pcrop.TILE_SIZE_OFFSET_PX - 2,
                                                      self.tiles_qty[1] * pcrop.TILE_SIZE_OFFSET_PX - 2),
                                                     (255, 0, 0, 120))

        preview_img_with_selection = self.preview_image.copy()
        preview_img_with_selection.paste(self.selected_image_preview_temp,
                                         (selection_no * pcrop.TILE_SIZE_OFFSET_PX * self.tiles_qty[0], 0),
                                         mask=self.selected_image_preview_temp)

        preview_img_with_selection_qt = ImageQt(preview_img_with_selection)
        self.ui.img_preview_pixmap_lbl.setPixmap(qtg.QPixmap.fromImage(preview_img_with_selection_qt))

    # def show_second(self):
    #     self.window2 = SettingsScreenWindow()
    #     self.window2.show()


# if __name__ == "main.py":
app = qtw.QApplication([])
app.setStyle("Fusion")
widget = MainScreenWindow()
widget.setWindowTitle("Terraria PaintCrap v0.1")
# palette = qtg.QPalette()
# palette.setColor(qtg.QPalette.ColorRole.Window, qtg.QColor(53, 53, 53))
# app.setPalette(palette)
widget.show()
app.exec()
