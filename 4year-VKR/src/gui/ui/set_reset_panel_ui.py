# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'set_reset_panel.ui'
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
from PySide6.QtWidgets import (QApplication, QDoubleSpinBox, QHBoxLayout, QLabel,
    QPushButton, QSizePolicy, QSlider, QSpacerItem,
    QSpinBox, QVBoxLayout, QWidget)

class Ui_SetResetPanel(object):
    def setupUi(self, SetResetPanel):
        if not SetResetPanel.objectName():
            SetResetPanel.setObjectName(u"SetResetPanel")
        SetResetPanel.resize(856, 553)
        self.verticalLayout_2 = QVBoxLayout(SetResetPanel)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_cycles = QVBoxLayout()
        self.verticalLayout_cycles.setObjectName(u"verticalLayout_cycles")
        self.horizontalLayout_cycle_spin = QHBoxLayout()
        self.horizontalLayout_cycle_spin.setObjectName(u"horizontalLayout_cycle_spin")
        self.lbl_cycle = QLabel(SetResetPanel)
        self.lbl_cycle.setObjectName(u"lbl_cycle")

        self.horizontalLayout_cycle_spin.addWidget(self.lbl_cycle)

        self.spin_cycle = QSpinBox(SetResetPanel)
        self.spin_cycle.setObjectName(u"spin_cycle")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.spin_cycle.sizePolicy().hasHeightForWidth())
        self.spin_cycle.setSizePolicy(sizePolicy)
        self.spin_cycle.setMinimumSize(QSize(0, 0))
        self.spin_cycle.setMaximumSize(QSize(200, 16777215))
        self.spin_cycle.setMinimum(1)

        self.horizontalLayout_cycle_spin.addWidget(self.spin_cycle)

        self.horizontalSpacer_cycle_spin = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_cycle_spin.addItem(self.horizontalSpacer_cycle_spin)


        self.verticalLayout_cycles.addLayout(self.horizontalLayout_cycle_spin)

        self.horizontalLayout_cycle_slider = QHBoxLayout()
        self.horizontalLayout_cycle_slider.setObjectName(u"horizontalLayout_cycle_slider")
        self.lbl_cycle_min = QLabel(SetResetPanel)
        self.lbl_cycle_min.setObjectName(u"lbl_cycle_min")

        self.horizontalLayout_cycle_slider.addWidget(self.lbl_cycle_min)

        self.slider_cycle = QSlider(SetResetPanel)
        self.slider_cycle.setObjectName(u"slider_cycle")
        self.slider_cycle.setMinimum(1)
        self.slider_cycle.setOrientation(Qt.Orientation.Horizontal)

        self.horizontalLayout_cycle_slider.addWidget(self.slider_cycle)

        self.lbl_cycle_max = QLabel(SetResetPanel)
        self.lbl_cycle_max.setObjectName(u"lbl_cycle_max")

        self.horizontalLayout_cycle_slider.addWidget(self.lbl_cycle_max)


        self.verticalLayout_cycles.addLayout(self.horizontalLayout_cycle_slider)


        self.verticalLayout_2.addLayout(self.verticalLayout_cycles)

        self.mpl_canvas = QWidget(SetResetPanel)
        self.mpl_canvas.setObjectName(u"mpl_canvas")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(1)
        sizePolicy1.setHeightForWidth(self.mpl_canvas.sizePolicy().hasHeightForWidth())
        self.mpl_canvas.setSizePolicy(sizePolicy1)
        self.mpl_canvas.setMinimumSize(QSize(600, 300))
        self.verticalLayout_canvas = QVBoxLayout(self.mpl_canvas)
        self.verticalLayout_canvas.setSpacing(0)
        self.verticalLayout_canvas.setObjectName(u"verticalLayout_canvas")
        self.verticalLayout_canvas.setContentsMargins(0, 0, 0, 0)

        self.verticalLayout_2.addWidget(self.mpl_canvas)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout_vset_label = QHBoxLayout()
        self.horizontalLayout_vset_label.setObjectName(u"horizontalLayout_vset_label")
        self.lbl_k_set = QLabel(SetResetPanel)
        self.lbl_k_set.setObjectName(u"lbl_k_set")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.lbl_k_set.sizePolicy().hasHeightForWidth())
        self.lbl_k_set.setSizePolicy(sizePolicy2)
        self.lbl_k_set.setMinimumSize(QSize(60, 0))

        self.horizontalLayout_vset_label.addWidget(self.lbl_k_set)

        self.spin_k_set = QDoubleSpinBox(SetResetPanel)
        self.spin_k_set.setObjectName(u"spin_k_set")
        sizePolicy.setHeightForWidth(self.spin_k_set.sizePolicy().hasHeightForWidth())
        self.spin_k_set.setSizePolicy(sizePolicy)
        self.spin_k_set.setMaximumSize(QSize(200, 16777215))
        self.spin_k_set.setMaximum(500.000000000000000)
        self.spin_k_set.setSingleStep(0.010000000000000)
        self.spin_k_set.setValue(1.000000000000000)

        self.horizontalLayout_vset_label.addWidget(self.spin_k_set)

        self.horizontalSpacer_vset_label = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_vset_label.addItem(self.horizontalSpacer_vset_label)


        self.verticalLayout.addLayout(self.horizontalLayout_vset_label)

        self.horizontalLayout_vset_slider = QHBoxLayout()
        self.horizontalLayout_vset_slider.setObjectName(u"horizontalLayout_vset_slider")
        self.lbl_k_set_min = QLabel(SetResetPanel)
        self.lbl_k_set_min.setObjectName(u"lbl_k_set_min")
        self.lbl_k_set_min.setMinimumSize(QSize(40, 0))

        self.horizontalLayout_vset_slider.addWidget(self.lbl_k_set_min)

        self.slider_k_set = QSlider(SetResetPanel)
        self.slider_k_set.setObjectName(u"slider_k_set")
        self.slider_k_set.setMinimum(0)
        self.slider_k_set.setMaximum(50000)
        self.slider_k_set.setValue(100)
        self.slider_k_set.setSliderPosition(100)
        self.slider_k_set.setOrientation(Qt.Orientation.Horizontal)

        self.horizontalLayout_vset_slider.addWidget(self.slider_k_set)

        self.lbl_k_set_max = QLabel(SetResetPanel)
        self.lbl_k_set_max.setObjectName(u"lbl_k_set_max")
        self.lbl_k_set_max.setMinimumSize(QSize(40, 0))
        self.lbl_k_set_max.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.horizontalLayout_vset_slider.addWidget(self.lbl_k_set_max)


        self.verticalLayout.addLayout(self.horizontalLayout_vset_slider)

        self.horizontalLayout_vreset_label = QHBoxLayout()
        self.horizontalLayout_vreset_label.setObjectName(u"horizontalLayout_vreset_label")
        self.lbl_k_reset = QLabel(SetResetPanel)
        self.lbl_k_reset.setObjectName(u"lbl_k_reset")
        sizePolicy2.setHeightForWidth(self.lbl_k_reset.sizePolicy().hasHeightForWidth())
        self.lbl_k_reset.setSizePolicy(sizePolicy2)
        self.lbl_k_reset.setMinimumSize(QSize(60, 0))

        self.horizontalLayout_vreset_label.addWidget(self.lbl_k_reset)

        self.spin_k_reset = QDoubleSpinBox(SetResetPanel)
        self.spin_k_reset.setObjectName(u"spin_k_reset")
        sizePolicy.setHeightForWidth(self.spin_k_reset.sizePolicy().hasHeightForWidth())
        self.spin_k_reset.setSizePolicy(sizePolicy)
        self.spin_k_reset.setMaximumSize(QSize(200, 16777215))
        self.spin_k_reset.setMaximum(500.000000000000000)
        self.spin_k_reset.setSingleStep(0.010000000000000)
        self.spin_k_reset.setValue(1.000000000000000)

        self.horizontalLayout_vreset_label.addWidget(self.spin_k_reset)

        self.horizontalSpacer_vreset_label = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_vreset_label.addItem(self.horizontalSpacer_vreset_label)


        self.verticalLayout.addLayout(self.horizontalLayout_vreset_label)

        self.horizontalLayout_vreset_slider = QHBoxLayout()
        self.horizontalLayout_vreset_slider.setObjectName(u"horizontalLayout_vreset_slider")
        self.lbl_k_reset_min = QLabel(SetResetPanel)
        self.lbl_k_reset_min.setObjectName(u"lbl_k_reset_min")
        self.lbl_k_reset_min.setMinimumSize(QSize(40, 0))

        self.horizontalLayout_vreset_slider.addWidget(self.lbl_k_reset_min)

        self.slider_k_reset = QSlider(SetResetPanel)
        self.slider_k_reset.setObjectName(u"slider_k_reset")
        self.slider_k_reset.setMinimum(0)
        self.slider_k_reset.setMaximum(50000)
        self.slider_k_reset.setValue(100)
        self.slider_k_reset.setSliderPosition(100)
        self.slider_k_reset.setOrientation(Qt.Orientation.Horizontal)

        self.horizontalLayout_vreset_slider.addWidget(self.slider_k_reset)

        self.lbl_k_reset_max = QLabel(SetResetPanel)
        self.lbl_k_reset_max.setObjectName(u"lbl_k_reset_max")
        self.lbl_k_reset_max.setMinimumSize(QSize(40, 0))
        font = QFont()
        font.setPointSize(9)
        self.lbl_k_reset_max.setFont(font)
        self.lbl_k_reset_max.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.horizontalLayout_vreset_slider.addWidget(self.lbl_k_reset_max)


        self.verticalLayout.addLayout(self.horizontalLayout_vreset_slider)


        self.verticalLayout_2.addLayout(self.verticalLayout)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.btn_cancel = QPushButton(SetResetPanel)
        self.btn_cancel.setObjectName(u"btn_cancel")
        sizePolicy.setHeightForWidth(self.btn_cancel.sizePolicy().hasHeightForWidth())
        self.btn_cancel.setSizePolicy(sizePolicy)

        self.horizontalLayout.addWidget(self.btn_cancel)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_2)

        self.btn_apply = QPushButton(SetResetPanel)
        self.btn_apply.setObjectName(u"btn_apply")
        sizePolicy.setHeightForWidth(self.btn_apply.sizePolicy().hasHeightForWidth())
        self.btn_apply.setSizePolicy(sizePolicy)

        self.horizontalLayout.addWidget(self.btn_apply)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_3)

        self.horizontalLayout.setStretch(0, 1)
        self.horizontalLayout.setStretch(1, 1)
        self.horizontalLayout.setStretch(3, 1)
        self.horizontalLayout.setStretch(4, 1)

        self.verticalLayout_2.addLayout(self.horizontalLayout)


        self.retranslateUi(SetResetPanel)

        QMetaObject.connectSlotsByName(SetResetPanel)
    # setupUi

    def retranslateUi(self, SetResetPanel):
        SetResetPanel.setWindowTitle(QCoreApplication.translate("SetResetPanel", u"Form", None))
        self.lbl_cycle.setText(QCoreApplication.translate("SetResetPanel", u"<html><head/><body><p><span style=\" font-size:12pt;\">\u0426\u0438\u043a\u043b \u2116</span></p></body></html>", None))
        self.lbl_cycle_min.setText(QCoreApplication.translate("SetResetPanel", u"<html><head/><body><p><span style=\" font-size:12pt;\">1</span></p></body></html>", None))
        self.lbl_cycle_max.setText(QCoreApplication.translate("SetResetPanel", u"<html><head/><body><p><span style=\" font-size:12pt;\">1000</span></p></body></html>", None))
        self.lbl_k_set.setText(QCoreApplication.translate("SetResetPanel", u"<html><head/><body><p><span style=\" font-size:12pt;\">k</span><span style=\" font-size:12pt; vertical-align:sub;\">SET</span></p></body></html>", None))
        self.lbl_k_set_min.setText(QCoreApplication.translate("SetResetPanel", u"<html><head/><body><p><span style=\" font-size:12pt;\">0</span></p></body></html>", None))
        self.lbl_k_set_max.setText(QCoreApplication.translate("SetResetPanel", u"<html><head/><body><p><span style=\" font-size:12pt;\">5000</span></p></body></html>", None))
        self.lbl_k_reset.setText(QCoreApplication.translate("SetResetPanel", u"<html><head/><body><p><span style=\" font-size:12pt;\">k</span><span style=\" font-size:12pt; vertical-align:sub;\">RESET</span></p></body></html>", None))
        self.lbl_k_reset_min.setText(QCoreApplication.translate("SetResetPanel", u"<html><head/><body><p><span style=\" font-size:12pt;\">0</span></p></body></html>", None))
        self.lbl_k_reset_max.setText(QCoreApplication.translate("SetResetPanel", u"<html><head/><body><p><span style=\" font-size:12pt;\">5000</span></p></body></html>", None))
        self.btn_cancel.setText(QCoreApplication.translate("SetResetPanel", u"\u041e\u0442\u043c\u0435\u043d\u0430", None))
        self.btn_apply.setText(QCoreApplication.translate("SetResetPanel", u"\u041f\u0440\u0438\u043c\u0435\u043d\u0438\u0442\u044c", None))
    # retranslateUi

