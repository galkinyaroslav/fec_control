# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ConnectionWindow_UI.ui'
##
## Created by: Qt User Interface Compiler version 6.8.1
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
from PySide6.QtWidgets import (QAbstractButton, QApplication, QDialog, QDialogButtonBox,
    QFrame, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QSizePolicy, QSpacerItem, QVBoxLayout,
    QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(515, 206)
        self.verticalLayout_2 = QVBoxLayout(Dialog)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.gen_name_label = QLabel(Dialog)
        self.gen_name_label.setObjectName(u"gen_name_label")

        self.horizontalLayout_2.addWidget(self.gen_name_label)

        self.gen_name_lineEdit = QLineEdit(Dialog)
        self.gen_name_lineEdit.setObjectName(u"gen_name_lineEdit")

        self.horizontalLayout_2.addWidget(self.gen_name_lineEdit)

        self.gen_connect_pushButton = QPushButton(Dialog)
        self.gen_connect_pushButton.setObjectName(u"gen_connect_pushButton")

        self.horizontalLayout_2.addWidget(self.gen_connect_pushButton)


        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.gen_message_label = QLabel(Dialog)
        self.gen_message_label.setObjectName(u"gen_message_label")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.gen_message_label.sizePolicy().hasHeightForWidth())
        self.gen_message_label.setSizePolicy(sizePolicy)
        self.gen_message_label.setMinimumSize(QSize(0, 0))
        self.gen_message_label.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.gen_message_label.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.horizontalLayout_3.addWidget(self.gen_message_label)

        self.gen_message_received_label = QLabel(Dialog)
        self.gen_message_received_label.setObjectName(u"gen_message_received_label")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.gen_message_received_label.sizePolicy().hasHeightForWidth())
        self.gen_message_received_label.setSizePolicy(sizePolicy1)
        self.gen_message_received_label.setMaximumSize(QSize(16777215, 16777215))
        self.gen_message_received_label.setBaseSize(QSize(0, 0))
        self.gen_message_received_label.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.horizontalLayout_3.addWidget(self.gen_message_received_label, 0, Qt.AlignmentFlag.AlignLeft)


        self.verticalLayout.addLayout(self.horizontalLayout_3)

        self.line = QFrame(Dialog)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.Shape.HLine)
        self.line.setFrameShadow(QFrame.Shadow.Sunken)

        self.verticalLayout.addWidget(self.line)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.rcu_ip_label = QLabel(Dialog)
        self.rcu_ip_label.setObjectName(u"rcu_ip_label")

        self.horizontalLayout.addWidget(self.rcu_ip_label)

        self.rcu_ip_lineEdit = QLineEdit(Dialog)
        self.rcu_ip_lineEdit.setObjectName(u"rcu_ip_lineEdit")

        self.horizontalLayout.addWidget(self.rcu_ip_lineEdit)

        self.rcu_port_label = QLabel(Dialog)
        self.rcu_port_label.setObjectName(u"rcu_port_label")

        self.horizontalLayout.addWidget(self.rcu_port_label)

        self.rcu_port_lineEdit = QLineEdit(Dialog)
        self.rcu_port_lineEdit.setObjectName(u"rcu_port_lineEdit")

        self.horizontalLayout.addWidget(self.rcu_port_lineEdit)

        self.rcu_connect_pushButton = QPushButton(Dialog)
        self.rcu_connect_pushButton.setObjectName(u"rcu_connect_pushButton")

        self.horizontalLayout.addWidget(self.rcu_connect_pushButton)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.rcu_message_label = QLabel(Dialog)
        self.rcu_message_label.setObjectName(u"rcu_message_label")
        sizePolicy.setHeightForWidth(self.rcu_message_label.sizePolicy().hasHeightForWidth())
        self.rcu_message_label.setSizePolicy(sizePolicy)

        self.horizontalLayout_4.addWidget(self.rcu_message_label)

        self.rcu_message_received_label = QLabel(Dialog)
        self.rcu_message_received_label.setObjectName(u"rcu_message_received_label")

        self.horizontalLayout_4.addWidget(self.rcu_message_received_label)


        self.verticalLayout.addLayout(self.horizontalLayout_4)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)

        self.buttonBox = QDialogButtonBox(Dialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setStandardButtons(QDialogButtonBox.StandardButton.Cancel|QDialogButtonBox.StandardButton.Ok)

        self.verticalLayout.addWidget(self.buttonBox)


        self.verticalLayout_2.addLayout(self.verticalLayout)


        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Dialog", None))
        self.gen_name_label.setText(QCoreApplication.translate("Dialog", u"Gen name:", None))
        self.gen_name_lineEdit.setText(QCoreApplication.translate("Dialog", u"AFG3152C", None))
        self.gen_connect_pushButton.setText(QCoreApplication.translate("Dialog", u"Connect", None))
        self.gen_message_label.setText(QCoreApplication.translate("Dialog", u"Message:", None))
        self.gen_message_received_label.setText("")
        self.rcu_ip_label.setText(QCoreApplication.translate("Dialog", u"IP:", None))
        self.rcu_ip_lineEdit.setInputMask(QCoreApplication.translate("Dialog", u"000.000.000.000", None))
        self.rcu_ip_lineEdit.setText(QCoreApplication.translate("Dialog", u"1...", None))
        self.rcu_port_label.setText(QCoreApplication.translate("Dialog", u"Port:", None))
        self.rcu_port_lineEdit.setText(QCoreApplication.translate("Dialog", u"30", None))
        self.rcu_connect_pushButton.setText(QCoreApplication.translate("Dialog", u"Connect", None))
        self.rcu_message_label.setText(QCoreApplication.translate("Dialog", u"Message:", None))
        self.rcu_message_received_label.setText("")
    # retranslateUi

