# Form implementation generated from reading ui file '.\gui_splash.ui'
#
# Created by: PyQt6 UI code generator 6.4.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_Splash(object):
    def setupUi(self, Splash):
        Splash.setObjectName("Splash")
        Splash.resize(640, 480)
        self.label = QtWidgets.QLabel(parent=Splash)
        self.label.setGeometry(QtCore.QRect(0, 0, 631, 471))
        self.label.setScaledContents(True)
        self.label.setObjectName("label")

        self.retranslateUi(Splash)
        QtCore.QMetaObject.connectSlotsByName(Splash)

    def retranslateUi(self, Splash):
        _translate = QtCore.QCoreApplication.translate
        Splash.setWindowTitle(_translate("Splash", "Form"))
        self.label.setText(_translate("Splash", "TextLabel"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Splash = QtWidgets.QWidget()
    ui = Ui_Splash()
    ui.setupUi(Splash)
    Splash.show()
    sys.exit(app.exec())
