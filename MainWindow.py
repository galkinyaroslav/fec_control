# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'MainWindow.ui'
##
## Created by: Qt User Interface Compiler version 6.6.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QComboBox, QFrame, QGridLayout,
    QHBoxLayout, QLabel, QLayout, QLineEdit,
    QMainWindow, QMenuBar, QPushButton, QSizePolicy,
    QSpinBox, QStatusBar, QVBoxLayout, QWidget)

from circle import ColoredCircleWidget

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(800, 643)
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setMinimumSize(QSize(800, 600))
        MainWindow.setMaximumSize(QSize(3840, 2160))
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.centralwidget.setEnabled(True)
        sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy)
        self.centralwidget.setMinimumSize(QSize(800, 600))
        self.gridLayout_3 = QGridLayout(self.centralwidget)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.frame_3 = QFrame(self.centralwidget)
        self.frame_3.setObjectName(u"frame_3")
        sizePolicy1 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Minimum)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.frame_3.sizePolicy().hasHeightForWidth())
        self.frame_3.setSizePolicy(sizePolicy1)
        self.frame_3.setMinimumSize(QSize(200, 0))
        self.frame_3.setFrameShape(QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QFrame.Raised)
        self.verticalLayout_3 = QVBoxLayout(self.frame_3)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setSizeConstraint(QLayout.SetMinimumSize)
        self.base_commands_label = QLabel(self.frame_3)
        self.base_commands_label.setObjectName(u"base_commands_label")
        self.base_commands_label.setEnabled(True)
        sizePolicy2 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.base_commands_label.sizePolicy().hasHeightForWidth())
        self.base_commands_label.setSizePolicy(sizePolicy2)
        self.base_commands_label.setMinimumSize(QSize(120, 20))
        self.base_commands_label.setMaximumSize(QSize(120, 20))
        self.base_commands_label.setBaseSize(QSize(0, 0))
        self.base_commands_label.setLayoutDirection(Qt.LeftToRight)
        self.base_commands_label.setFrameShape(QFrame.NoFrame)
        self.base_commands_label.setScaledContents(False)
        self.base_commands_label.setAlignment(Qt.AlignCenter)
        self.base_commands_label.setWordWrap(False)

        self.verticalLayout_3.addWidget(self.base_commands_label, 0, Qt.AlignHCenter)

        self.line = QFrame(self.frame_3)
        self.line.setObjectName(u"line")
        self.line.setMinimumSize(QSize(0, 20))
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)

        self.verticalLayout_3.addWidget(self.line)

        self.gridLayout_2 = QGridLayout()
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setSizeConstraint(QLayout.SetFixedSize)
        self.tts_tth_led = ColoredCircleWidget(self.frame_3)
        self.tts_tth_led.setObjectName(u"tts_tth_led")

        self.gridLayout_2.addWidget(self.tts_tth_led, 8, 2, 1, 1)

        self.tts_tth_btn = QPushButton(self.frame_3)
        self.tts_tth_btn.setObjectName(u"tts_tth_btn")
        sizePolicy.setHeightForWidth(self.tts_tth_btn.sizePolicy().hasHeightForWidth())
        self.tts_tth_btn.setSizePolicy(sizePolicy)
        self.tts_tth_btn.setMinimumSize(QSize(40, 20))

        self.gridLayout_2.addWidget(self.tts_tth_btn, 8, 0, 1, 2)

        self.trstat_btn = QPushButton(self.frame_3)
        self.trstat_btn.setObjectName(u"trstat_btn")
        sizePolicy.setHeightForWidth(self.trstat_btn.sizePolicy().hasHeightForWidth())
        self.trstat_btn.setSizePolicy(sizePolicy)
        self.trstat_btn.setMinimumSize(QSize(40, 20))

        self.gridLayout_2.addWidget(self.trstat_btn, 1, 0, 1, 2)

        self.rid_label = QLabel(self.frame_3)
        self.rid_label.setObjectName(u"rid_label")
        sizePolicy.setHeightForWidth(self.rid_label.sizePolicy().hasHeightForWidth())
        self.rid_label.setSizePolicy(sizePolicy)
        self.rid_label.setMinimumSize(QSize(40, 20))

        self.gridLayout_2.addWidget(self.rid_label, 5, 0, 1, 2)

        self.pll_label = QLabel(self.frame_3)
        self.pll_label.setObjectName(u"pll_label")
        sizePolicy.setHeightForWidth(self.pll_label.sizePolicy().hasHeightForWidth())
        self.pll_label.setSizePolicy(sizePolicy)
        self.pll_label.setMinimumSize(QSize(40, 20))

        self.gridLayout_2.addWidget(self.pll_label, 3, 0, 1, 2)

        self.link_label = QLabel(self.frame_3)
        self.link_label.setObjectName(u"link_label")
        sizePolicy.setHeightForWidth(self.link_label.sizePolicy().hasHeightForWidth())
        self.link_label.setSizePolicy(sizePolicy)
        self.link_label.setMinimumSize(QSize(40, 20))

        self.gridLayout_2.addWidget(self.link_label, 0, 0, 1, 2)

        self.adcd_btn = QPushButton(self.frame_3)
        self.adcd_btn.setObjectName(u"adcd_btn")
        sizePolicy.setHeightForWidth(self.adcd_btn.sizePolicy().hasHeightForWidth())
        self.adcd_btn.setSizePolicy(sizePolicy)
        self.adcd_btn.setMinimumSize(QSize(40, 20))

        self.gridLayout_2.addWidget(self.adcd_btn, 14, 0, 1, 2)

        self.adcd_number_label = QLabel(self.frame_3)
        self.adcd_number_label.setObjectName(u"adcd_number_label")
        sizePolicy.setHeightForWidth(self.adcd_number_label.sizePolicy().hasHeightForWidth())
        self.adcd_number_label.setSizePolicy(sizePolicy)
        self.adcd_number_label.setMinimumSize(QSize(40, 20))

        self.gridLayout_2.addWidget(self.adcd_number_label, 15, 0, 1, 2)

        self.trstat_led = ColoredCircleWidget(self.frame_3)
        self.trstat_led.setObjectName(u"trstat_led")

        self.gridLayout_2.addWidget(self.trstat_led, 1, 2, 1, 1)

        self.card_number_label = QLabel(self.frame_3)
        self.card_number_label.setObjectName(u"card_number_label")
        sizePolicy.setHeightForWidth(self.card_number_label.sizePolicy().hasHeightForWidth())
        self.card_number_label.setSizePolicy(sizePolicy)
        self.card_number_label.setMinimumSize(QSize(40, 20))

        self.gridLayout_2.addWidget(self.card_number_label, 2, 0, 1, 2)

        self.rid_value_label = QLabel(self.frame_3)
        self.rid_value_label.setObjectName(u"rid_value_label")
        sizePolicy.setHeightForWidth(self.rid_value_label.sizePolicy().hasHeightForWidth())
        self.rid_value_label.setSizePolicy(sizePolicy)
        self.rid_value_label.setMinimumSize(QSize(40, 20))

        self.gridLayout_2.addWidget(self.rid_value_label, 5, 2, 1, 1)

        self.mask_label = QLabel(self.frame_3)
        self.mask_label.setObjectName(u"mask_label")
        sizePolicy.setHeightForWidth(self.mask_label.sizePolicy().hasHeightForWidth())
        self.mask_label.setSizePolicy(sizePolicy)
        self.mask_label.setMinimumSize(QSize(40, 20))

        self.gridLayout_2.addWidget(self.mask_label, 6, 0, 1, 2)

        self.cid_value_label = QLabel(self.frame_3)
        self.cid_value_label.setObjectName(u"cid_value_label")
        sizePolicy.setHeightForWidth(self.cid_value_label.sizePolicy().hasHeightForWidth())
        self.cid_value_label.setSizePolicy(sizePolicy)
        self.cid_value_label.setMinimumSize(QSize(40, 20))

        self.gridLayout_2.addWidget(self.cid_value_label, 4, 2, 1, 1)

        self.line_8 = QFrame(self.frame_3)
        self.line_8.setObjectName(u"line_8")
        sizePolicy.setHeightForWidth(self.line_8.sizePolicy().hasHeightForWidth())
        self.line_8.setSizePolicy(sizePolicy)
        self.line_8.setMinimumSize(QSize(40, 20))
        self.line_8.setFrameShape(QFrame.HLine)
        self.line_8.setFrameShadow(QFrame.Sunken)

        self.gridLayout_2.addWidget(self.line_8, 13, 0, 1, 3)

        self.sh1_label = QLabel(self.frame_3)
        self.sh1_label.setObjectName(u"sh1_label")
        self.sh1_label.setMinimumSize(QSize(40, 20))

        self.gridLayout_2.addWidget(self.sh1_label, 11, 0, 1, 1)

        self.pll_value_label = QLabel(self.frame_3)
        self.pll_value_label.setObjectName(u"pll_value_label")
        sizePolicy.setHeightForWidth(self.pll_value_label.sizePolicy().hasHeightForWidth())
        self.pll_value_label.setSizePolicy(sizePolicy)
        self.pll_value_label.setMinimumSize(QSize(40, 20))

        self.gridLayout_2.addWidget(self.pll_value_label, 3, 2, 1, 1)

        self.sh0_label = QLabel(self.frame_3)
        self.sh0_label.setObjectName(u"sh0_label")
        self.sh0_label.setMinimumSize(QSize(40, 20))

        self.gridLayout_2.addWidget(self.sh0_label, 10, 0, 1, 1)

        self.sh1_value_label = QLabel(self.frame_3)
        self.sh1_value_label.setObjectName(u"sh1_value_label")
        self.sh1_value_label.setMinimumSize(QSize(40, 20))

        self.gridLayout_2.addWidget(self.sh1_value_label, 11, 1, 1, 2)

        self.cid_label = QLabel(self.frame_3)
        self.cid_label.setObjectName(u"cid_label")
        sizePolicy.setHeightForWidth(self.cid_label.sizePolicy().hasHeightForWidth())
        self.cid_label.setSizePolicy(sizePolicy)
        self.cid_label.setMinimumSize(QSize(40, 20))

        self.gridLayout_2.addWidget(self.cid_label, 4, 0, 1, 2)

        self.adcd_number_spinBox = QSpinBox(self.frame_3)
        self.adcd_number_spinBox.setObjectName(u"adcd_number_spinBox")
        sizePolicy.setHeightForWidth(self.adcd_number_spinBox.sizePolicy().hasHeightForWidth())
        self.adcd_number_spinBox.setSizePolicy(sizePolicy)
        self.adcd_number_spinBox.setMinimumSize(QSize(40, 20))
        self.adcd_number_spinBox.setMinimum(1)
        self.adcd_number_spinBox.setMaximum(1000)

        self.gridLayout_2.addWidget(self.adcd_number_spinBox, 15, 2, 1, 1)

        self.scan_pll_btn = QPushButton(self.frame_3)
        self.scan_pll_btn.setObjectName(u"scan_pll_btn")
        sizePolicy.setHeightForWidth(self.scan_pll_btn.sizePolicy().hasHeightForWidth())
        self.scan_pll_btn.setSizePolicy(sizePolicy)
        self.scan_pll_btn.setMinimumSize(QSize(40, 20))

        self.gridLayout_2.addWidget(self.scan_pll_btn, 9, 0, 1, 2)

        self.sh0_value_label = QLabel(self.frame_3)
        self.sh0_value_label.setObjectName(u"sh0_value_label")
        self.sh0_value_label.setMinimumSize(QSize(40, 20))

        self.gridLayout_2.addWidget(self.sh0_value_label, 10, 1, 1, 2)

        self.link_spinBox = QSpinBox(self.frame_3)
        self.link_spinBox.setObjectName(u"link_spinBox")
        sizePolicy.setHeightForWidth(self.link_spinBox.sizePolicy().hasHeightForWidth())
        self.link_spinBox.setSizePolicy(sizePolicy)
        self.link_spinBox.setMinimumSize(QSize(40, 20))
        self.link_spinBox.setMaximum(31)
        self.link_spinBox.setValue(31)

        self.gridLayout_2.addWidget(self.link_spinBox, 0, 2, 1, 1)

        self.card_number_value_label = QLabel(self.frame_3)
        self.card_number_value_label.setObjectName(u"card_number_value_label")
        sizePolicy.setHeightForWidth(self.card_number_value_label.sizePolicy().hasHeightForWidth())
        self.card_number_value_label.setSizePolicy(sizePolicy)
        self.card_number_value_label.setMinimumSize(QSize(40, 20))

        self.gridLayout_2.addWidget(self.card_number_value_label, 2, 2, 1, 1)

        self.mask_value_label = QLabel(self.frame_3)
        self.mask_value_label.setObjectName(u"mask_value_label")
        sizePolicy.setHeightForWidth(self.mask_value_label.sizePolicy().hasHeightForWidth())
        self.mask_value_label.setSizePolicy(sizePolicy)
        self.mask_value_label.setMinimumSize(QSize(40, 20))

        self.gridLayout_2.addWidget(self.mask_value_label, 6, 2, 1, 1)

        self.ini_btn = QPushButton(self.frame_3)
        self.ini_btn.setObjectName(u"ini_btn")
        sizePolicy.setHeightForWidth(self.ini_btn.sizePolicy().hasHeightForWidth())
        self.ini_btn.setSizePolicy(sizePolicy)
        self.ini_btn.setMinimumSize(QSize(40, 20))

        self.gridLayout_2.addWidget(self.ini_btn, 7, 0, 1, 2)

        self.set_pll_btn = QPushButton(self.frame_3)
        self.set_pll_btn.setObjectName(u"set_pll_btn")

        self.gridLayout_2.addWidget(self.set_pll_btn, 12, 0, 1, 1)

        self.set_sh0_spinbox = QSpinBox(self.frame_3)
        self.set_sh0_spinbox.setObjectName(u"set_sh0_spinbox")
        self.set_sh0_spinbox.setMaximum(31)

        self.gridLayout_2.addWidget(self.set_sh0_spinbox, 12, 1, 1, 1)

        self.set_sh1_spinbox = QSpinBox(self.frame_3)
        self.set_sh1_spinbox.setObjectName(u"set_sh1_spinbox")
        self.set_sh1_spinbox.setMaximum(31)

        self.gridLayout_2.addWidget(self.set_sh1_spinbox, 12, 2, 1, 1)

        self.scan_pll_runs_spinbox = QSpinBox(self.frame_3)
        self.scan_pll_runs_spinbox.setObjectName(u"scan_pll_runs_spinbox")
        self.scan_pll_runs_spinbox.setMinimum(1)
        self.scan_pll_runs_spinbox.setMaximum(10)

        self.gridLayout_2.addWidget(self.scan_pll_runs_spinbox, 9, 2, 1, 1)


        self.verticalLayout_3.addLayout(self.gridLayout_2)

        self.ttok_frame = QFrame(self.frame_3)
        self.ttok_frame.setObjectName(u"ttok_frame")
        self.ttok_frame.setFrameShape(QFrame.StyledPanel)
        self.verticalLayout_2 = QVBoxLayout(self.ttok_frame)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.ttok_btn = QPushButton(self.ttok_frame)
        self.ttok_btn.setObjectName(u"ttok_btn")
        sizePolicy.setHeightForWidth(self.ttok_btn.sizePolicy().hasHeightForWidth())
        self.ttok_btn.setSizePolicy(sizePolicy)
        self.ttok_btn.setMinimumSize(QSize(40, 20))

        self.verticalLayout_2.addWidget(self.ttok_btn)

        self.ttok_comand_label = QLabel(self.ttok_frame)
        self.ttok_comand_label.setObjectName(u"ttok_comand_label")
        sizePolicy.setHeightForWidth(self.ttok_comand_label.sizePolicy().hasHeightForWidth())
        self.ttok_comand_label.setSizePolicy(sizePolicy)
        self.ttok_comand_label.setMinimumSize(QSize(40, 20))

        self.verticalLayout_2.addWidget(self.ttok_comand_label)

        self.ttok_lineEdit = QLineEdit(self.ttok_frame)
        self.ttok_lineEdit.setObjectName(u"ttok_lineEdit")
        sizePolicy.setHeightForWidth(self.ttok_lineEdit.sizePolicy().hasHeightForWidth())
        self.ttok_lineEdit.setSizePolicy(sizePolicy)
        self.ttok_lineEdit.setMinimumSize(QSize(40, 20))

        self.verticalLayout_2.addWidget(self.ttok_lineEdit)


        self.verticalLayout_3.addWidget(self.ttok_frame)


        self.gridLayout_3.addWidget(self.frame_3, 0, 0, 6, 1)

        self.frame_4 = QFrame(self.centralwidget)
        self.frame_4.setObjectName(u"frame_4")
        sizePolicy3 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Preferred)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.frame_4.sizePolicy().hasHeightForWidth())
        self.frame_4.setSizePolicy(sizePolicy3)
        self.frame_4.setMinimumSize(QSize(100, 0))
        self.frame_4.setFrameShape(QFrame.StyledPanel)
        self.frame_4.setFrameShadow(QFrame.Raised)
        self.verticalLayout_5 = QVBoxLayout(self.frame_4)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.gain_label = QLabel(self.frame_4)
        self.gain_label.setObjectName(u"gain_label")
        sizePolicy2.setHeightForWidth(self.gain_label.sizePolicy().hasHeightForWidth())
        self.gain_label.setSizePolicy(sizePolicy2)
        self.gain_label.setMinimumSize(QSize(60, 20))
        self.gain_label.setAlignment(Qt.AlignCenter)

        self.verticalLayout_5.addWidget(self.gain_label)

        self.line_4 = QFrame(self.frame_4)
        self.line_4.setObjectName(u"line_4")
        sizePolicy4 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.line_4.sizePolicy().hasHeightForWidth())
        self.line_4.setSizePolicy(sizePolicy4)
        self.line_4.setMinimumSize(QSize(60, 20))
        self.line_4.setFrameShape(QFrame.HLine)
        self.line_4.setFrameShadow(QFrame.Sunken)

        self.verticalLayout_5.addWidget(self.line_4)

        self.gain_btn = QPushButton(self.frame_4)
        self.gain_btn.setObjectName(u"gain_btn")
        sizePolicy2.setHeightForWidth(self.gain_btn.sizePolicy().hasHeightForWidth())
        self.gain_btn.setSizePolicy(sizePolicy2)
        self.gain_btn.setMinimumSize(QSize(160, 20))

        self.verticalLayout_5.addWidget(self.gain_btn)

        self.gain_lastrun_label = QLabel(self.frame_4)
        self.gain_lastrun_label.setObjectName(u"gain_lastrun_label")
        sizePolicy.setHeightForWidth(self.gain_lastrun_label.sizePolicy().hasHeightForWidth())
        self.gain_lastrun_label.setSizePolicy(sizePolicy)
        self.gain_lastrun_label.setMinimumSize(QSize(60, 40))
        self.gain_lastrun_label.setAlignment(Qt.AlignCenter)
        self.gain_lastrun_label.setWordWrap(True)

        self.verticalLayout_5.addWidget(self.gain_lastrun_label)


        self.gridLayout_3.addWidget(self.frame_4, 3, 1, 1, 1)

        self.frame_2 = QFrame(self.centralwidget)
        self.frame_2.setObjectName(u"frame_2")
        sizePolicy3.setHeightForWidth(self.frame_2.sizePolicy().hasHeightForWidth())
        self.frame_2.setSizePolicy(sizePolicy3)
        self.frame_2.setMinimumSize(QSize(100, 0))
        self.frame_2.setFrameShape(QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QFrame.Raised)
        self.verticalLayout_4 = QVBoxLayout(self.frame_2)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.crosstalk_label = QLabel(self.frame_2)
        self.crosstalk_label.setObjectName(u"crosstalk_label")
        sizePolicy2.setHeightForWidth(self.crosstalk_label.sizePolicy().hasHeightForWidth())
        self.crosstalk_label.setSizePolicy(sizePolicy2)
        self.crosstalk_label.setMinimumSize(QSize(60, 20))
        self.crosstalk_label.setAlignment(Qt.AlignCenter)

        self.verticalLayout_4.addWidget(self.crosstalk_label, 0, Qt.AlignHCenter)

        self.line_3 = QFrame(self.frame_2)
        self.line_3.setObjectName(u"line_3")
        sizePolicy4.setHeightForWidth(self.line_3.sizePolicy().hasHeightForWidth())
        self.line_3.setSizePolicy(sizePolicy4)
        self.line_3.setMinimumSize(QSize(60, 20))
        self.line_3.setFrameShape(QFrame.HLine)
        self.line_3.setFrameShadow(QFrame.Sunken)

        self.verticalLayout_4.addWidget(self.line_3)

        self.crosstalk_btn = QPushButton(self.frame_2)
        self.crosstalk_btn.setObjectName(u"crosstalk_btn")
        sizePolicy2.setHeightForWidth(self.crosstalk_btn.sizePolicy().hasHeightForWidth())
        self.crosstalk_btn.setSizePolicy(sizePolicy2)
        self.crosstalk_btn.setMinimumSize(QSize(160, 20))

        self.verticalLayout_4.addWidget(self.crosstalk_btn)

        self.crosstalk_lastrun_label = QLabel(self.frame_2)
        self.crosstalk_lastrun_label.setObjectName(u"crosstalk_lastrun_label")
        sizePolicy.setHeightForWidth(self.crosstalk_lastrun_label.sizePolicy().hasHeightForWidth())
        self.crosstalk_lastrun_label.setSizePolicy(sizePolicy)
        self.crosstalk_lastrun_label.setMinimumSize(QSize(60, 40))
        self.crosstalk_lastrun_label.setAlignment(Qt.AlignCenter)
        self.crosstalk_lastrun_label.setWordWrap(True)

        self.verticalLayout_4.addWidget(self.crosstalk_lastrun_label)


        self.gridLayout_3.addWidget(self.frame_2, 2, 1, 1, 1)

        self.frame_5 = QFrame(self.centralwidget)
        self.frame_5.setObjectName(u"frame_5")
        sizePolicy3.setHeightForWidth(self.frame_5.sizePolicy().hasHeightForWidth())
        self.frame_5.setSizePolicy(sizePolicy3)
        self.frame_5.setMinimumSize(QSize(100, 0))
        self.frame_5.setFrameShape(QFrame.StyledPanel)
        self.frame_5.setFrameShadow(QFrame.Raised)
        self.verticalLayout_6 = QVBoxLayout(self.frame_5)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.pedestal_label = QLabel(self.frame_5)
        self.pedestal_label.setObjectName(u"pedestal_label")
        sizePolicy2.setHeightForWidth(self.pedestal_label.sizePolicy().hasHeightForWidth())
        self.pedestal_label.setSizePolicy(sizePolicy2)
        self.pedestal_label.setMinimumSize(QSize(60, 20))
        self.pedestal_label.setAlignment(Qt.AlignCenter)

        self.verticalLayout_6.addWidget(self.pedestal_label, 0, Qt.AlignHCenter|Qt.AlignVCenter)

        self.line_5 = QFrame(self.frame_5)
        self.line_5.setObjectName(u"line_5")
        sizePolicy2.setHeightForWidth(self.line_5.sizePolicy().hasHeightForWidth())
        self.line_5.setSizePolicy(sizePolicy2)
        self.line_5.setMinimumSize(QSize(60, 20))
        self.line_5.setFrameShape(QFrame.HLine)
        self.line_5.setFrameShadow(QFrame.Sunken)

        self.verticalLayout_6.addWidget(self.line_5)

        self.pedestal_btn = QPushButton(self.frame_5)
        self.pedestal_btn.setObjectName(u"pedestal_btn")
        sizePolicy2.setHeightForWidth(self.pedestal_btn.sizePolicy().hasHeightForWidth())
        self.pedestal_btn.setSizePolicy(sizePolicy2)
        self.pedestal_btn.setMinimumSize(QSize(160, 20))

        self.verticalLayout_6.addWidget(self.pedestal_btn)

        self.pedestal_lastrun_label = QLabel(self.frame_5)
        self.pedestal_lastrun_label.setObjectName(u"pedestal_lastrun_label")
        sizePolicy.setHeightForWidth(self.pedestal_lastrun_label.sizePolicy().hasHeightForWidth())
        self.pedestal_lastrun_label.setSizePolicy(sizePolicy)
        self.pedestal_lastrun_label.setMinimumSize(QSize(60, 40))
        self.pedestal_lastrun_label.setAlignment(Qt.AlignCenter)
        self.pedestal_lastrun_label.setWordWrap(True)

        self.verticalLayout_6.addWidget(self.pedestal_lastrun_label)


        self.gridLayout_3.addWidget(self.frame_5, 5, 1, 1, 1)

        self.frame_6 = QFrame(self.centralwidget)
        self.frame_6.setObjectName(u"frame_6")
        sizePolicy3.setHeightForWidth(self.frame_6.sizePolicy().hasHeightForWidth())
        self.frame_6.setSizePolicy(sizePolicy3)
        self.frame_6.setMinimumSize(QSize(100, 0))
        self.frame_6.setFrameShape(QFrame.StyledPanel)
        self.frame_6.setFrameShadow(QFrame.Raised)
        self.verticalLayout_7 = QVBoxLayout(self.frame_6)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.enc_label = QLabel(self.frame_6)
        self.enc_label.setObjectName(u"enc_label")
        sizePolicy2.setHeightForWidth(self.enc_label.sizePolicy().hasHeightForWidth())
        self.enc_label.setSizePolicy(sizePolicy2)
        self.enc_label.setMinimumSize(QSize(60, 20))
        self.enc_label.setAlignment(Qt.AlignCenter)

        self.verticalLayout_7.addWidget(self.enc_label, 0, Qt.AlignHCenter)

        self.line_6 = QFrame(self.frame_6)
        self.line_6.setObjectName(u"line_6")
        sizePolicy4.setHeightForWidth(self.line_6.sizePolicy().hasHeightForWidth())
        self.line_6.setSizePolicy(sizePolicy4)
        self.line_6.setMinimumSize(QSize(60, 20))
        self.line_6.setMaximumSize(QSize(9999999, 20))
        self.line_6.setFrameShape(QFrame.HLine)
        self.line_6.setFrameShadow(QFrame.Sunken)

        self.verticalLayout_7.addWidget(self.line_6)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setSizeConstraint(QLayout.SetMinimumSize)
        self.enc_cdet_label = QLabel(self.frame_6)
        self.enc_cdet_label.setObjectName(u"enc_cdet_label")
        sizePolicy.setHeightForWidth(self.enc_cdet_label.sizePolicy().hasHeightForWidth())
        self.enc_cdet_label.setSizePolicy(sizePolicy)
        self.enc_cdet_label.setMinimumSize(QSize(60, 20))

        self.horizontalLayout.addWidget(self.enc_cdet_label, 0, Qt.AlignHCenter)

        self.enc_cdet_comboBox = QComboBox(self.frame_6)
        self.enc_cdet_comboBox.addItem("")
        self.enc_cdet_comboBox.addItem("")
        self.enc_cdet_comboBox.addItem("")
        self.enc_cdet_comboBox.addItem("")
        self.enc_cdet_comboBox.setObjectName(u"enc_cdet_comboBox")
        sizePolicy.setHeightForWidth(self.enc_cdet_comboBox.sizePolicy().hasHeightForWidth())
        self.enc_cdet_comboBox.setSizePolicy(sizePolicy)
        self.enc_cdet_comboBox.setMinimumSize(QSize(60, 20))

        self.horizontalLayout.addWidget(self.enc_cdet_comboBox, 0, Qt.AlignHCenter)


        self.verticalLayout_7.addLayout(self.horizontalLayout)


        self.gridLayout_3.addWidget(self.frame_6, 0, 1, 1, 1)

        self.frame = QFrame(self.centralwidget)
        self.frame.setObjectName(u"frame")
        sizePolicy3.setHeightForWidth(self.frame.sizePolicy().hasHeightForWidth())
        self.frame.setSizePolicy(sizePolicy3)
        self.frame.setMinimumSize(QSize(200, 551))
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.verticalLayout = QVBoxLayout(self.frame)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setSizeConstraint(QLayout.SetMinimumSize)
        self.verticalLayout.setContentsMargins(9, 9, 9, 9)
        self.plot_label = QLabel(self.frame)
        self.plot_label.setObjectName(u"plot_label")
        sizePolicy2.setHeightForWidth(self.plot_label.sizePolicy().hasHeightForWidth())
        self.plot_label.setSizePolicy(sizePolicy2)
        self.plot_label.setMinimumSize(QSize(0, 20))
        self.plot_label.setAlignment(Qt.AlignCenter)

        self.verticalLayout.addWidget(self.plot_label)

        self.line_2 = QFrame(self.frame)
        self.line_2.setObjectName(u"line_2")
        sizePolicy4.setHeightForWidth(self.line_2.sizePolicy().hasHeightForWidth())
        self.line_2.setSizePolicy(sizePolicy4)
        self.line_2.setMinimumSize(QSize(100, 20))
        self.line_2.setFrameShape(QFrame.HLine)
        self.line_2.setFrameShadow(QFrame.Sunken)

        self.verticalLayout.addWidget(self.line_2)

        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.plot_card_number_lineEdit = QLineEdit(self.frame)
        self.plot_card_number_lineEdit.setObjectName(u"plot_card_number_lineEdit")
        sizePolicy.setHeightForWidth(self.plot_card_number_lineEdit.sizePolicy().hasHeightForWidth())
        self.plot_card_number_lineEdit.setSizePolicy(sizePolicy)
        self.plot_card_number_lineEdit.setMinimumSize(QSize(100, 20))

        self.gridLayout.addWidget(self.plot_card_number_lineEdit, 0, 2, 1, 2)

        self.plot_event_number_lineEdit = QLineEdit(self.frame)
        self.plot_event_number_lineEdit.setObjectName(u"plot_event_number_lineEdit")
        sizePolicy.setHeightForWidth(self.plot_event_number_lineEdit.sizePolicy().hasHeightForWidth())
        self.plot_event_number_lineEdit.setSizePolicy(sizePolicy)
        self.plot_event_number_lineEdit.setMinimumSize(QSize(100, 20))

        self.gridLayout.addWidget(self.plot_event_number_lineEdit, 5, 2, 1, 2)

        self.plot_run_number_label = QLabel(self.frame)
        self.plot_run_number_label.setObjectName(u"plot_run_number_label")
        sizePolicy.setHeightForWidth(self.plot_run_number_label.sizePolicy().hasHeightForWidth())
        self.plot_run_number_label.setSizePolicy(sizePolicy)
        self.plot_run_number_label.setMinimumSize(QSize(100, 20))

        self.gridLayout.addWidget(self.plot_run_number_label, 4, 0, 1, 2, Qt.AlignLeft)

        self.plot_run_number_lineEdit = QLineEdit(self.frame)
        self.plot_run_number_lineEdit.setObjectName(u"plot_run_number_lineEdit")
        sizePolicy.setHeightForWidth(self.plot_run_number_lineEdit.sizePolicy().hasHeightForWidth())
        self.plot_run_number_lineEdit.setSizePolicy(sizePolicy)
        self.plot_run_number_lineEdit.setMinimumSize(QSize(100, 20))

        self.gridLayout.addWidget(self.plot_run_number_lineEdit, 4, 2, 1, 2)

        self.plot_amplitude_label = QLabel(self.frame)
        self.plot_amplitude_label.setObjectName(u"plot_amplitude_label")
        sizePolicy.setHeightForWidth(self.plot_amplitude_label.sizePolicy().hasHeightForWidth())
        self.plot_amplitude_label.setSizePolicy(sizePolicy)
        self.plot_amplitude_label.setMinimumSize(QSize(100, 20))

        self.gridLayout.addWidget(self.plot_amplitude_label, 6, 0, 1, 2)

        self.plot_cdet_label = QLabel(self.frame)
        self.plot_cdet_label.setObjectName(u"plot_cdet_label")
        sizePolicy.setHeightForWidth(self.plot_cdet_label.sizePolicy().hasHeightForWidth())
        self.plot_cdet_label.setSizePolicy(sizePolicy)
        self.plot_cdet_label.setMinimumSize(QSize(100, 20))

        self.gridLayout.addWidget(self.plot_cdet_label, 1, 0, 1, 2, Qt.AlignLeft)

        self.plot_parity_label = QLabel(self.frame)
        self.plot_parity_label.setObjectName(u"plot_parity_label")
        sizePolicy.setHeightForWidth(self.plot_parity_label.sizePolicy().hasHeightForWidth())
        self.plot_parity_label.setSizePolicy(sizePolicy)
        self.plot_parity_label.setMinimumSize(QSize(100, 20))

        self.gridLayout.addWidget(self.plot_parity_label, 3, 0, 1, 2, Qt.AlignLeft)

        self.plot_parity_comboBox = QComboBox(self.frame)
        self.plot_parity_comboBox.addItem("")
        self.plot_parity_comboBox.addItem("")
        self.plot_parity_comboBox.setObjectName(u"plot_parity_comboBox")
        sizePolicy.setHeightForWidth(self.plot_parity_comboBox.sizePolicy().hasHeightForWidth())
        self.plot_parity_comboBox.setSizePolicy(sizePolicy)
        self.plot_parity_comboBox.setMinimumSize(QSize(100, 20))

        self.gridLayout.addWidget(self.plot_parity_comboBox, 3, 2, 1, 2)

        self.plot_test_name_label = QLabel(self.frame)
        self.plot_test_name_label.setObjectName(u"plot_test_name_label")
        sizePolicy.setHeightForWidth(self.plot_test_name_label.sizePolicy().hasHeightForWidth())
        self.plot_test_name_label.setSizePolicy(sizePolicy)
        self.plot_test_name_label.setMinimumSize(QSize(100, 20))

        self.gridLayout.addWidget(self.plot_test_name_label, 2, 0, 1, 2, Qt.AlignLeft)

        self.plot_amplitude_lineEdit = QLineEdit(self.frame)
        self.plot_amplitude_lineEdit.setObjectName(u"plot_amplitude_lineEdit")
        sizePolicy.setHeightForWidth(self.plot_amplitude_lineEdit.sizePolicy().hasHeightForWidth())
        self.plot_amplitude_lineEdit.setSizePolicy(sizePolicy)
        self.plot_amplitude_lineEdit.setMinimumSize(QSize(100, 20))

        self.gridLayout.addWidget(self.plot_amplitude_lineEdit, 6, 2, 1, 2)

        self.plot_card_number_label = QLabel(self.frame)
        self.plot_card_number_label.setObjectName(u"plot_card_number_label")
        sizePolicy.setHeightForWidth(self.plot_card_number_label.sizePolicy().hasHeightForWidth())
        self.plot_card_number_label.setSizePolicy(sizePolicy)
        self.plot_card_number_label.setMinimumSize(QSize(100, 20))

        self.gridLayout.addWidget(self.plot_card_number_label, 0, 0, 1, 2, Qt.AlignLeft)

        self.plot_event_number_label = QLabel(self.frame)
        self.plot_event_number_label.setObjectName(u"plot_event_number_label")
        sizePolicy.setHeightForWidth(self.plot_event_number_label.sizePolicy().hasHeightForWidth())
        self.plot_event_number_label.setSizePolicy(sizePolicy)
        self.plot_event_number_label.setMinimumSize(QSize(100, 20))

        self.gridLayout.addWidget(self.plot_event_number_label, 5, 0, 1, 2, Qt.AlignLeft)

        self.plot_cdet_comboBox = QComboBox(self.frame)
        self.plot_cdet_comboBox.addItem("")
        self.plot_cdet_comboBox.addItem("")
        self.plot_cdet_comboBox.addItem("")
        self.plot_cdet_comboBox.addItem("")
        self.plot_cdet_comboBox.setObjectName(u"plot_cdet_comboBox")
        sizePolicy.setHeightForWidth(self.plot_cdet_comboBox.sizePolicy().hasHeightForWidth())
        self.plot_cdet_comboBox.setSizePolicy(sizePolicy)
        self.plot_cdet_comboBox.setMinimumSize(QSize(100, 20))

        self.gridLayout.addWidget(self.plot_cdet_comboBox, 1, 2, 1, 2)

        self.plot_test_name_comboBox = QComboBox(self.frame)
        self.plot_test_name_comboBox.addItem("")
        self.plot_test_name_comboBox.addItem("")
        self.plot_test_name_comboBox.addItem("")
        self.plot_test_name_comboBox.addItem("")
        self.plot_test_name_comboBox.setObjectName(u"plot_test_name_comboBox")
        sizePolicy.setHeightForWidth(self.plot_test_name_comboBox.sizePolicy().hasHeightForWidth())
        self.plot_test_name_comboBox.setSizePolicy(sizePolicy)
        self.plot_test_name_comboBox.setMinimumSize(QSize(100, 20))

        self.gridLayout.addWidget(self.plot_test_name_comboBox, 2, 2, 1, 2)


        self.verticalLayout.addLayout(self.gridLayout)

        self.plot_file_exist_label = QLabel(self.frame)
        self.plot_file_exist_label.setObjectName(u"plot_file_exist_label")
        sizePolicy.setHeightForWidth(self.plot_file_exist_label.sizePolicy().hasHeightForWidth())
        self.plot_file_exist_label.setSizePolicy(sizePolicy)
        self.plot_file_exist_label.setMinimumSize(QSize(60, 40))
        self.plot_file_exist_label.setAlignment(Qt.AlignCenter)
        self.plot_file_exist_label.setWordWrap(True)

        self.verticalLayout.addWidget(self.plot_file_exist_label)

        self.show_waveform_btn = QPushButton(self.frame)
        self.show_waveform_btn.setObjectName(u"show_waveform_btn")
        sizePolicy2.setHeightForWidth(self.show_waveform_btn.sizePolicy().hasHeightForWidth())
        self.show_waveform_btn.setSizePolicy(sizePolicy2)
        self.show_waveform_btn.setMinimumSize(QSize(160, 20))

        self.verticalLayout.addWidget(self.show_waveform_btn)

        self.show_rms_btn = QPushButton(self.frame)
        self.show_rms_btn.setObjectName(u"show_rms_btn")
        sizePolicy2.setHeightForWidth(self.show_rms_btn.sizePolicy().hasHeightForWidth())
        self.show_rms_btn.setSizePolicy(sizePolicy2)
        self.show_rms_btn.setMinimumSize(QSize(160, 20))

        self.verticalLayout.addWidget(self.show_rms_btn)

        self.update_plots_btn = QPushButton(self.frame)
        self.update_plots_btn.setObjectName(u"update_plots_btn")
        sizePolicy2.setHeightForWidth(self.update_plots_btn.sizePolicy().hasHeightForWidth())
        self.update_plots_btn.setSizePolicy(sizePolicy2)
        self.update_plots_btn.setMinimumSize(QSize(160, 20))

        self.verticalLayout.addWidget(self.update_plots_btn)


        self.gridLayout_3.addWidget(self.frame, 0, 3, 4, 1)

        self.frame_7 = QFrame(self.centralwidget)
        self.frame_7.setObjectName(u"frame_7")
        sizePolicy3.setHeightForWidth(self.frame_7.sizePolicy().hasHeightForWidth())
        self.frame_7.setSizePolicy(sizePolicy3)
        self.frame_7.setMinimumSize(QSize(100, 0))
        self.frame_7.setFrameShape(QFrame.StyledPanel)
        self.frame_7.setFrameShadow(QFrame.Raised)
        self.verticalLayout_8 = QVBoxLayout(self.frame_7)
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.raw_label = QLabel(self.frame_7)
        self.raw_label.setObjectName(u"raw_label")
        sizePolicy2.setHeightForWidth(self.raw_label.sizePolicy().hasHeightForWidth())
        self.raw_label.setSizePolicy(sizePolicy2)
        self.raw_label.setMinimumSize(QSize(60, 20))
        self.raw_label.setAlignment(Qt.AlignCenter)

        self.verticalLayout_8.addWidget(self.raw_label, 0, Qt.AlignHCenter|Qt.AlignVCenter)

        self.line_9 = QFrame(self.frame_7)
        self.line_9.setObjectName(u"line_9")
        sizePolicy2.setHeightForWidth(self.line_9.sizePolicy().hasHeightForWidth())
        self.line_9.setSizePolicy(sizePolicy2)
        self.line_9.setMinimumSize(QSize(60, 20))
        self.line_9.setFrameShape(QFrame.HLine)
        self.line_9.setFrameShadow(QFrame.Sunken)

        self.verticalLayout_8.addWidget(self.line_9)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.raw_btn = QPushButton(self.frame_7)
        self.raw_btn.setObjectName(u"raw_btn")
        sizePolicy2.setHeightForWidth(self.raw_btn.sizePolicy().hasHeightForWidth())
        self.raw_btn.setSizePolicy(sizePolicy2)
        self.raw_btn.setMinimumSize(QSize(160, 20))

        self.horizontalLayout_2.addWidget(self.raw_btn)

        self.raw_runs_spinBox = QSpinBox(self.frame_7)
        self.raw_runs_spinBox.setObjectName(u"raw_runs_spinBox")
        sizePolicy.setHeightForWidth(self.raw_runs_spinBox.sizePolicy().hasHeightForWidth())
        self.raw_runs_spinBox.setSizePolicy(sizePolicy)
        self.raw_runs_spinBox.setMinimumSize(QSize(0, 20))
        self.raw_runs_spinBox.setMinimum(1)
        self.raw_runs_spinBox.setMaximum(1000)

        self.horizontalLayout_2.addWidget(self.raw_runs_spinBox)


        self.verticalLayout_8.addLayout(self.horizontalLayout_2)

        self.raw_lastrun_label = QLabel(self.frame_7)
        self.raw_lastrun_label.setObjectName(u"raw_lastrun_label")
        sizePolicy.setHeightForWidth(self.raw_lastrun_label.sizePolicy().hasHeightForWidth())
        self.raw_lastrun_label.setSizePolicy(sizePolicy)
        self.raw_lastrun_label.setMinimumSize(QSize(60, 40))
        self.raw_lastrun_label.setAlignment(Qt.AlignCenter)
        self.raw_lastrun_label.setWordWrap(True)

        self.verticalLayout_8.addWidget(self.raw_lastrun_label)


        self.gridLayout_3.addWidget(self.frame_7, 1, 1, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 800, 22))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.base_commands_label.setText(QCoreApplication.translate("MainWindow", u"Base Commands", None))
        self.tts_tth_btn.setText(QCoreApplication.translate("MainWindow", u"tts 2;tth 2", None))
        self.trstat_btn.setText(QCoreApplication.translate("MainWindow", u"Get Trstat", None))
        self.rid_label.setText(QCoreApplication.translate("MainWindow", u"RID:", None))
        self.pll_label.setText(QCoreApplication.translate("MainWindow", u"PLL:", None))
        self.link_label.setText(QCoreApplication.translate("MainWindow", u"Link:", None))
        self.adcd_btn.setText(QCoreApplication.translate("MainWindow", u"Get Adcd", None))
        self.adcd_number_label.setText(QCoreApplication.translate("MainWindow", u"Number:", None))
        self.card_number_label.setText(QCoreApplication.translate("MainWindow", u"Card number:", None))
        self.rid_value_label.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.mask_label.setText(QCoreApplication.translate("MainWindow", u"Mask:", None))
        self.cid_value_label.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.sh1_label.setText(QCoreApplication.translate("MainWindow", u"SH1", None))
        self.pll_value_label.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.sh0_label.setText(QCoreApplication.translate("MainWindow", u"SH0", None))
        self.sh1_value_label.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.cid_label.setText(QCoreApplication.translate("MainWindow", u"CID:", None))
        self.scan_pll_btn.setText(QCoreApplication.translate("MainWindow", u"Scan PLL", None))
        self.sh0_value_label.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.card_number_value_label.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.mask_value_label.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.ini_btn.setText(QCoreApplication.translate("MainWindow", u"INI", None))
        self.set_pll_btn.setText(QCoreApplication.translate("MainWindow", u"Set PLL", None))
        self.ttok_btn.setText(QCoreApplication.translate("MainWindow", u"Send ttok", None))
        self.ttok_comand_label.setText(QCoreApplication.translate("MainWindow", u"Command:", None))
        self.gain_label.setText(QCoreApplication.translate("MainWindow", u"Gain", None))
        self.gain_btn.setText(QCoreApplication.translate("MainWindow", u"GAIN", None))
        self.gain_lastrun_label.setText(QCoreApplication.translate("MainWindow", u"last_run", None))
        self.crosstalk_label.setText(QCoreApplication.translate("MainWindow", u"Cross Talk", None))
        self.crosstalk_btn.setText(QCoreApplication.translate("MainWindow", u"CROSSTALK", None))
        self.crosstalk_lastrun_label.setText(QCoreApplication.translate("MainWindow", u"last_run", None))
        self.pedestal_label.setText(QCoreApplication.translate("MainWindow", u"Pedestal", None))
        self.pedestal_btn.setText(QCoreApplication.translate("MainWindow", u"PEDESTAL", None))
        self.pedestal_lastrun_label.setText(QCoreApplication.translate("MainWindow", u"last_run", None))
        self.enc_label.setText(QCoreApplication.translate("MainWindow", u"ENC", None))
        self.enc_cdet_label.setText(QCoreApplication.translate("MainWindow", u"Cdet:", None))
        self.enc_cdet_comboBox.setItemText(0, QCoreApplication.translate("MainWindow", u"0pF", None))
        self.enc_cdet_comboBox.setItemText(1, QCoreApplication.translate("MainWindow", u"10pF", None))
        self.enc_cdet_comboBox.setItemText(2, QCoreApplication.translate("MainWindow", u"20pF", None))
        self.enc_cdet_comboBox.setItemText(3, QCoreApplication.translate("MainWindow", u"40pF", None))

        self.plot_label.setText(QCoreApplication.translate("MainWindow", u"Plot", None))
        self.plot_card_number_lineEdit.setText(QCoreApplication.translate("MainWindow", u"454", None))
        self.plot_card_number_lineEdit.setPlaceholderText(QCoreApplication.translate("MainWindow", u"454", None))
        self.plot_event_number_lineEdit.setText(QCoreApplication.translate("MainWindow", u"-1", None))
        self.plot_event_number_lineEdit.setPlaceholderText(QCoreApplication.translate("MainWindow", u"-1", None))
        self.plot_run_number_label.setText(QCoreApplication.translate("MainWindow", u"Run", None))
        self.plot_run_number_lineEdit.setText(QCoreApplication.translate("MainWindow", u"1", None))
        self.plot_run_number_lineEdit.setPlaceholderText(QCoreApplication.translate("MainWindow", u"1", None))
        self.plot_amplitude_label.setText(QCoreApplication.translate("MainWindow", u"Amplitude", None))
        self.plot_cdet_label.setText(QCoreApplication.translate("MainWindow", u"Cdet", None))
        self.plot_parity_label.setText(QCoreApplication.translate("MainWindow", u"Parity", None))
        self.plot_parity_comboBox.setItemText(0, QCoreApplication.translate("MainWindow", u"odd", None))
        self.plot_parity_comboBox.setItemText(1, QCoreApplication.translate("MainWindow", u"even", None))

        self.plot_test_name_label.setText(QCoreApplication.translate("MainWindow", u"Test", None))
        self.plot_amplitude_lineEdit.setText(QCoreApplication.translate("MainWindow", u"0.02", None))
        self.plot_amplitude_lineEdit.setPlaceholderText(QCoreApplication.translate("MainWindow", u"0.5", None))
        self.plot_card_number_label.setText(QCoreApplication.translate("MainWindow", u"Card #", None))
        self.plot_event_number_label.setText(QCoreApplication.translate("MainWindow", u"Event", None))
        self.plot_cdet_comboBox.setItemText(0, QCoreApplication.translate("MainWindow", u"0pF", None))
        self.plot_cdet_comboBox.setItemText(1, QCoreApplication.translate("MainWindow", u"10pF", None))
        self.plot_cdet_comboBox.setItemText(2, QCoreApplication.translate("MainWindow", u"20pF", None))
        self.plot_cdet_comboBox.setItemText(3, QCoreApplication.translate("MainWindow", u"40pF", None))

        self.plot_test_name_comboBox.setItemText(0, QCoreApplication.translate("MainWindow", u"raw", None))
        self.plot_test_name_comboBox.setItemText(1, QCoreApplication.translate("MainWindow", u"rms_pedestal", None))
        self.plot_test_name_comboBox.setItemText(2, QCoreApplication.translate("MainWindow", u"crosstalk", None))
        self.plot_test_name_comboBox.setItemText(3, QCoreApplication.translate("MainWindow", u"gain", None))

        self.plot_file_exist_label.setText(QCoreApplication.translate("MainWindow", u"File Exist / Not Exist", None))
        self.show_waveform_btn.setText(QCoreApplication.translate("MainWindow", u"Show WaveForm", None))
        self.show_rms_btn.setText(QCoreApplication.translate("MainWindow", u"Show RMS", None))
        self.update_plots_btn.setText(QCoreApplication.translate("MainWindow", u"Update Plots", None))
        self.raw_label.setText(QCoreApplication.translate("MainWindow", u"Raw", None))
        self.raw_btn.setText(QCoreApplication.translate("MainWindow", u"RAW", None))
        self.raw_lastrun_label.setText(QCoreApplication.translate("MainWindow", u"last_run", None))
    # retranslateUi

