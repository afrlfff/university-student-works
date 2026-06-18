# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'num_cycles_panel_old.ui'
##
## Created by: Qt User Interface Compiler version 6.11.0
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
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QLabel, QPushButton,
    QSizePolicy, QSlider, QSpacerItem, QSpinBox,
    QVBoxLayout, QWidget)

class Ui_NumCyclesPanel(object):
    def setupUi(self, NumCyclesPanel):
        if not NumCyclesPanel.objectName():
            NumCyclesPanel.setObjectName(u"NumCyclesPanel")
        NumCyclesPanel.resize(643, 438)
        self.verticalLayout_2 = QVBoxLayout(NumCyclesPanel)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalSpacer_2 = QSpacerItem(20, 181, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_2.addItem(self.verticalSpacer_2)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.lbl_cycles = QLabel(NumCyclesPanel)
        self.lbl_cycles.setObjectName(u"lbl_cycles")

        self.horizontalLayout_4.addWidget(self.lbl_cycles)

        self.spin_cycles = QSpinBox(NumCyclesPanel)
        self.spin_cycles.setObjectName(u"spin_cycles")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.spin_cycles.sizePolicy().hasHeightForWidth())
        self.spin_cycles.setSizePolicy(sizePolicy)
        self.spin_cycles.setMinimumSize(QSize(0, 0))
        self.spin_cycles.setMaximumSize(QSize(200, 16777215))
        self.spin_cycles.setMinimum(1)

        self.horizontalLayout_4.addWidget(self.spin_cycles)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer_2)


        self.verticalLayout.addLayout(self.horizontalLayout_4)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.lbl_min_cycle = QLabel(NumCyclesPanel)
        self.lbl_min_cycle.setObjectName(u"lbl_min_cycle")

        self.horizontalLayout_3.addWidget(self.lbl_min_cycle)

        self.slider_cycles = QSlider(NumCyclesPanel)
        self.slider_cycles.setObjectName(u"slider_cycles")
        self.slider_cycles.setMinimum(1)
        self.slider_cycles.setOrientation(Qt.Orientation.Horizontal)

        self.horizontalLayout_3.addWidget(self.slider_cycles)

        self.lbl_max_cycle = QLabel(NumCyclesPanel)
        self.lbl_max_cycle.setObjectName(u"lbl_max_cycle")

        self.horizontalLayout_3.addWidget(self.lbl_max_cycle)


        self.verticalLayout.addLayout(self.horizontalLayout_3)


        self.verticalLayout_2.addLayout(self.verticalLayout)

        self.verticalSpacer = QSpacerItem(20, 180, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_2.addItem(self.verticalSpacer)

        self.horizontalLayout_buttons = QHBoxLayout()
        self.horizontalLayout_buttons.setObjectName(u"horizontalLayout_buttons")
        self.horizontalSpacer_buttons = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_buttons.addItem(self.horizontalSpacer_buttons)

        self.btn_cancel = QPushButton(NumCyclesPanel)
        self.btn_cancel.setObjectName(u"btn_cancel")
        self.btn_cancel.setEnabled(False)

        self.horizontalLayout_buttons.addWidget(self.btn_cancel)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_buttons.addItem(self.horizontalSpacer)

        self.btn_apply = QPushButton(NumCyclesPanel)
        self.btn_apply.setObjectName(u"btn_apply")
        self.btn_apply.setEnabled(False)

        self.horizontalLayout_buttons.addWidget(self.btn_apply)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_buttons.addItem(self.horizontalSpacer_3)

        self.horizontalLayout_buttons.setStretch(0, 1)
        self.horizontalLayout_buttons.setStretch(1, 1)
        self.horizontalLayout_buttons.setStretch(3, 1)
        self.horizontalLayout_buttons.setStretch(4, 1)

        self.verticalLayout_2.addLayout(self.horizontalLayout_buttons)


        self.retranslateUi(NumCyclesPanel)

        QMetaObject.connectSlotsByName(NumCyclesPanel)
    # setupUi

    def retranslateUi(self, NumCyclesPanel):
        NumCyclesPanel.setWindowTitle(QCoreApplication.translate("NumCyclesPanel", u"Form", None))
        self.lbl_cycles.setText(QCoreApplication.translate("NumCyclesPanel", u"<html><head/><body><p><span style=\" font-size:12pt;\">\u041a\u043e\u043b\u0438\u0447\u0435\u0441\u0442\u0432\u043e \u0446\u0438\u043a\u043b\u043e\u0432</span></p></body></html>", None))
        self.lbl_min_cycle.setText(QCoreApplication.translate("NumCyclesPanel", u"<html><head/><body><p><span style=\" font-size:12pt;\">1</span></p></body></html>", None))
        self.lbl_max_cycle.setText(QCoreApplication.translate("NumCyclesPanel", u"<html><head/><body><p><span style=\" font-size:12pt;\">1000</span></p></body></html>", None))
        self.btn_cancel.setText(QCoreApplication.translate("NumCyclesPanel", u"\u041e\u0442\u043c\u0435\u043d\u0430", None))
        self.btn_apply.setText(QCoreApplication.translate("NumCyclesPanel", u"\u041f\u0440\u0438\u043c\u0435\u043d\u0438\u0442\u044c", None))
    # retranslateUi

