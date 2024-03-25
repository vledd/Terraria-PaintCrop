# import warnings
# warnings.filterwarnings("ignore", category=DeprecationWarning)

from gui_main import Ui_MainScreen
# from gui_second import Ui_SecondScreen

from PyQt6 import QtCore as qtc
from PyQt6 import QtGui as qtg
from PyQt6 import QtWidgets as qtw

from PIL import Image
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
        self.tileset = None
        self.files = None
        self.tiles_qty: list[int, int] = [1, 1]

        self.ui = Ui_MainScreen()
        self.ui.setupUi(self)

        self.ui.img_path_btn.clicked.connect(self.get_image_path)
        self.ui.tile_path_btn.clicked.connect(self.get_tileset_path)
        self.ui.frame_path_btn.clicked.connect(self.get_frame_path)
        self.ui.export_process_images.clicked.connect(self.process_preview)
        self.ui.export_single_png_btn.clicked.connect(self.process_save_to_folder)

        self.ui.tile_qty_xspin.valueChanged.connect(self.update_x_tiles_qty)
        self.ui.tile_qty_yspin.valueChanged.connect(self.update_y_tiles_qty)

        self.ui.tileset_pixmap_lbl.mouseDoubleClickEvent = self.tileset_pixmap_clicked

    def update_x_tiles_qty(self, event):
        self.tiles_qty[0] = int(event)

    def update_y_tiles_qty(self, event):
        self.tiles_qty[1] = int(event)

    def get_image_path(self):
        self.files = qtw.QFileDialog.getOpenFileNames(self, "Select Files", filter="Image files (*.jpg *.png)")
        if len(self.files[0]) == 0:
            self.ui.img_path_line.setText("No valid file provided!")
            for button in self.ui.buttonGroup.buttons():
                button.setEnabled(False)
        else:
            self.ui.img_path_line.setText(str(self.files[0]))
            for button in self.ui.buttonGroup.buttons():
                button.setEnabled(True)

    def get_tileset_path(self):
        self.tileset = qtw.QFileDialog.getOpenFileName(self, "Select Files", filter="Tileset (*.png)")
        if len(self.tileset[0]) == 0:
            self.ui.tile_path_line.setText("No valid tileset provided!")
        else:
            self.ui.tile_path_line.setText(str(self.tileset[0]))
            tileset_img = ImageQt(Image.open(self.tileset[0]))
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

        if len(self.files[0]) == 1:
            src_img = Image.open(str(self.files[0][0]))

            src_img_list.append(pcrop.process_image_single(src_img,
                                                           (self.tiles_qty[0], self.tiles_qty[1]),
                                                           src_frame,
                                                           frame_thick))
        else:
            for i in range(0, len(self.files[0])):
                img_local = Image.open(self.files[0][i])
                # Todo frames
                src_img_list.append(pcrop.process_image_single(img_local, (self.tiles_qty[0], self.tiles_qty[1]),
                                                               src_frame,
                                                               frame_thick))
                img_local.close()

        return src_img_list

    def process_preview(self):
        processed_img = ImageQt(pcrop.create_preview_multiple_images(self.process_images()))
        self.ui.img_preview_lbl.setPixmap(qtg.QPixmap.fromImage(processed_img))

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
        tileset_local = Image.open(self.tileset[0])
        pcrop.get_image_no_by_coords(tileset_local,
                                     (self.tiles_qty[0], self.tiles_qty[1]),
                                     (event.pos().x(), event.pos().y()),
                                     pcrop.TilesetTilesOrder.LEFT2RIGHT)


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
