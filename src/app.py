# import warnings
# warnings.filterwarnings("ignore", category=DeprecationWarning)
import time

from gui_main import Ui_MainScreen
from gui_about import Ui_AboutForm
from gui_splash import Ui_Splash

from PyQt6 import QtCore as qtc
from PyQt6 import QtGui as qtg
from PyQt6 import QtWidgets as qtw

from PIL import Image, ImageDraw
from PIL.ImageQt import ImageQt

import webbrowser
import pcrop_helpers as pcrop
import os
import sys


class SplashScreen(qtw.QSplashScreen):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ui = Ui_Splash()
        self.ui.setupUi(self)
        self.move(640, 260)
        self.ui.label.setPixmap(qtg.QPixmap.fromImage(logo_pixmap_qt))

        qtc.QTimer.singleShot(3000, self.close)


class AboutWindow(qtw.QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ui = Ui_AboutForm()
        self.ui.setupUi(self)

        self.setFixedSize(640, 485)
        self.setWindowTitle("About us")
        self.ui.logo.setPixmap(qtg.QPixmap.fromImage(logo_pixmap_qt))


class MainScreenWindow(qtw.QMainWindow):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.window2 = AboutWindow()

        self.frame = None
        self.tileset_pth = None
        self.images_pth = None

        self.preview_tileset_layer0: Image = None
        self.preview_tileset_layer1: Image = None

        self.preview_image: Image = None
        self.selected_image_preview: Image = None
        self.selected_image_preview_temp: Image = None
        self.tiles_qty: list[int, int] = [1, 1]
        self.tiles_order: pcrop.TilesetTilesOrder = pcrop.TilesetTilesOrder.LEFT2RIGHT

        self.ui = Ui_MainScreen()
        self.ui.setupUi(self)


        self.ui.img_path_btn.clicked.connect(self.get_image_path)
        self.ui.tile_path_btn.clicked.connect(self.get_tileset_path)
        self.ui.frame_path_btn.clicked.connect(self.get_frame_path)
        self.ui.export_single_png_btn.clicked.connect(self.process_save_to_folder)
        self.ui.export_tileset_btn.clicked.connect(self.tileset_save)

        self.ui.tile_qty_xspin.valueChanged.connect(self.update_x_tiles_qty)
        self.ui.tile_qty_yspin.valueChanged.connect(self.update_y_tiles_qty)
        self.ui.add_frame_chk.clicked.connect(self.update_frame)
        self.ui.frame_thick_spin.valueChanged.connect(self.update_frame)

        self.ui.tileset_pixmap_lbl.mousePressEvent = self.tileset_pixmap_clicked
        self.ui.img_preview_pixmap_lbl.mousePressEvent = self.img_preview_pixmap_clicked

        self.ui.menuFile.triggered.connect(self.menu_file_exit)
        self.ui.menuHelp.triggered.connect(self.menu_help_clicked)

    @staticmethod
    def menu_file_exit(self):
        app.closeAllWindows()
        app.exit(0)

    def menu_help_clicked(self, event):
        if event.text() == "About":
            self.show_about()
        else:
            webbrowser.open("https://github.com/vledd/Terraria-PaintCrop")

    def update_x_tiles_qty(self, event):
        self.tiles_qty[0] = int(event)
        self.selected_image_preview = None
        if self.images_pth is not None:
            self.process_preview()

    def update_y_tiles_qty(self, event):
        self.tiles_qty[1] = int(event)
        self.selected_image_preview = None
        if self.images_pth is not None:
            self.process_preview()

    def update_frame(self, event):
        if self.preview_image is None:
            return
        else:
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

            tileset_img = Image.open(self.tileset_pth[0])
            tileset_img_qt = ImageQt(tileset_img)

            self.preview_tileset_layer0 = Image.new("RGBA", Image.open(self.tileset_pth[0]).size)
            self.preview_tileset_layer0.paste(tileset_img, (0, 0))

            if tileset_img.size[0] >= tileset_img.size[1]:
                self.tiles_order = pcrop.TilesetTilesOrder.LEFT2RIGHT
            else:
                self.tiles_order = pcrop.TilesetTilesOrder.UP2DOWN

            self.ui.tileset_pixmap_lbl.setPixmap(qtg.QPixmap.fromImage(tileset_img_qt))

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
            tileset_local.save(save_path[0], dpi=(96, 96))
            qtw.QMessageBox.information(self, "Export status", "Tileset exported OK!")

    def process_save_to_folder(self):
        save_folder_path = qtw.QFileDialog.getExistingDirectory(self, "Select directory where to save")

        if save_folder_path == "":
            qtw.QMessageBox.warning(self, "Export warning", "Please select a valid folder!")
        else:
            processed_img_list = self.process_images()
            for i in range(0, len(processed_img_list)):
                processed_img_list[i].save(f"{save_folder_path}/export_{i}.png", dpi=(96, 96))
            qtw.QMessageBox.information(self, "Export status", "Image(s) exported OK!")

    def tileset_pixmap_clicked(self, event):
        # TODO finish feature
        if self.selected_image_preview is None:
            return

        tileset_local: Image = Image.open(self.tileset_pth[0])

        selection_no: int = pcrop.get_image_no_by_coords(tileset_local,
                                                         (self.tiles_qty[0], self.tiles_qty[1]),
                                                         (event.pos().x(), event.pos().y()),
                                                         self.tiles_order)

        eraser_img = Image.new("RGBA",
                               (self.tiles_qty[0] * pcrop.TILE_SIZE_OFFSET_PX,
                                self.tiles_qty[1] * pcrop.TILE_SIZE_OFFSET_PX),
                               (0, 0, 0, 0))

        # print(selection_no)
        if event.button() == qtg.QMouseEvent.button(event).LeftButton:
            self.preview_tileset_layer0 = (
                pcrop.process_and_replace_image_in_tileset_by_no(self.preview_tileset_layer0,
                                                                 selection_no,
                                                                 eraser_img,
                                                                 (self.tiles_qty[0], self.tiles_qty[1]),
                                                                 self.tiles_order,
                                                                 None, 0))

            self.preview_tileset_layer0 = (
                pcrop.process_and_replace_image_in_tileset_by_no(self.preview_tileset_layer0,
                                                                 selection_no,
                                                                 self.selected_image_preview,
                                                                 (self.tiles_qty[0], self.tiles_qty[1]),
                                                                 self.tiles_order,
                                                                 None, 0))  # Todo add frame

        elif event.button() == qtg.QMouseEvent.button(event).RightButton:
            restored_image = pcrop.extract_image_from_tileset_by_no(tileset_local,
                                                                    selection_no,
                                                                    (self.tiles_qty[0], self.tiles_qty[1]),
                                                                    self.tiles_order)

            self.preview_tileset_layer0 = (
                pcrop.process_and_replace_image_in_tileset_by_no(self.preview_tileset_layer0,
                                                                 selection_no,
                                                                 eraser_img,
                                                                 (self.tiles_qty[0], self.tiles_qty[1]),
                                                                 self.tiles_order,
                                                                 None, 0))

            self.preview_tileset_layer0 = (
                pcrop.process_and_replace_image_in_tileset_by_no(self.preview_tileset_layer0,
                                                                 selection_no,
                                                                 restored_image,
                                                                 (self.tiles_qty[0], self.tiles_qty[1]),
                                                                 self.tiles_order,
                                                                 None, 0))

        temp_tilseset_preview_qt = ImageQt(self.preview_tileset_layer0)
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

    def show_about(self):
        self.window2.show()


if getattr(sys, 'frozen', False):
    logo_pixmap_qt = ImageQt(Image.open(pcrop.resource_path("resources_internal/splash_1.jpg")))
else:
    logo_pixmap_qt = ImageQt(Image.open("../resources_internal/splash_1.jpg"))


# if __name__ == "main.py":
app = qtw.QApplication([])
app.setStyle("Fusion")
widget = MainScreenWindow()
widget.setWindowTitle("Terraria PaintCrop v1.0")
# palette = qtg.QPalette()
# palette.setColor(qtg.QPalette.ColorRole.Window, qtg.QColor(53, 53, 53))
# app.setPalette(palette)
widget.show()

widget2 = SplashScreen()
widget2.show()

app.exec()
