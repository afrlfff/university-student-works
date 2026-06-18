# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'num_cycles_panel.ui'
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
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QSizePolicy, QSlider, QSpacerItem,
    QSpinBox, QVBoxLayout, QWidget)

class Ui_NumCyclesPanel(object):
    def setupUi(self, NumCyclesPanel):
        if not NumCyclesPanel.objectName():
            NumCyclesPanel.setObjectName(u"NumCyclesPanel")
        NumCyclesPanel.resize(730, 621)
        self.verticalLayout_4 = QVBoxLayout(NumCyclesPanel)
        self.verticalLayout_4.setSpacing(0)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalSpacer_2 = QSpacerItem(20, 181, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_4.addItem(self.verticalSpacer_2)

        self.wgt_cycles = QWidget(NumCyclesPanel)
        self.wgt_cycles.setObjectName(u"wgt_cycles")
        self.verticalLayout_3 = QVBoxLayout(self.wgt_cycles)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.lbl_first_cycle = QLabel(self.wgt_cycles)
        self.lbl_first_cycle.setObjectName(u"lbl_first_cycle")
        self.lbl_first_cycle.setMinimumSize(QSize(150, 0))

        self.horizontalLayout_5.addWidget(self.lbl_first_cycle)

        self.spin_first_cycle = QSpinBox(self.wgt_cycles)
        self.spin_first_cycle.setObjectName(u"spin_first_cycle")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.spin_first_cycle.sizePolicy().hasHeightForWidth())
        self.spin_first_cycle.setSizePolicy(sizePolicy)
        self.spin_first_cycle.setMinimumSize(QSize(0, 0))
        self.spin_first_cycle.setMaximumSize(QSize(200, 16777215))
        self.spin_first_cycle.setMinimum(1)

        self.horizontalLayout_5.addWidget(self.spin_first_cycle)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_5.addItem(self.horizontalSpacer_4)

        self.lbl_tstart = QLabel(self.wgt_cycles)
        self.lbl_tstart.setObjectName(u"lbl_tstart")
        font = QFont()
        font.setPointSize(12)
        self.lbl_tstart.setFont(font)

        self.horizontalLayout_5.addWidget(self.lbl_tstart)

        self.le_tstart = QLineEdit(self.wgt_cycles)
        self.le_tstart.setObjectName(u"le_tstart")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.le_tstart.sizePolicy().hasHeightForWidth())
        self.le_tstart.setSizePolicy(sizePolicy1)
        self.le_tstart.setReadOnly(True)

        self.horizontalLayout_5.addWidget(self.le_tstart)


        self.verticalLayout_2.addLayout(self.horizontalLayout_5)

        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.lbl_first_cycle_min = QLabel(self.wgt_cycles)
        self.lbl_first_cycle_min.setObjectName(u"lbl_first_cycle_min")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.lbl_first_cycle_min.sizePolicy().hasHeightForWidth())
        self.lbl_first_cycle_min.setSizePolicy(sizePolicy2)
        self.lbl_first_cycle_min.setMinimumSize(QSize(0, 0))

        self.horizontalLayout_6.addWidget(self.lbl_first_cycle_min)

        self.slider_first_cycle = QSlider(self.wgt_cycles)
        self.slider_first_cycle.setObjectName(u"slider_first_cycle")
        self.slider_first_cycle.setMinimum(1)
        self.slider_first_cycle.setMaximum(1000)
        self.slider_first_cycle.setOrientation(Qt.Orientation.Horizontal)

        self.horizontalLayout_6.addWidget(self.slider_first_cycle)

        self.lbl_first_cycle_max = QLabel(self.wgt_cycles)
        self.lbl_first_cycle_max.setObjectName(u"lbl_first_cycle_max")
        self.lbl_first_cycle_max.setMinimumSize(QSize(75, 0))
        self.lbl_first_cycle_max.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.horizontalLayout_6.addWidget(self.lbl_first_cycle_max)


        self.verticalLayout_2.addLayout(self.horizontalLayout_6)


        self.verticalLayout_3.addLayout(self.verticalLayout_2)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.lbl_num_cycles = QLabel(self.wgt_cycles)
        self.lbl_num_cycles.setObjectName(u"lbl_num_cycles")
        sizePolicy2.setHeightForWidth(self.lbl_num_cycles.sizePolicy().hasHeightForWidth())
        self.lbl_num_cycles.setSizePolicy(sizePolicy2)
        self.lbl_num_cycles.setMinimumSize(QSize(150, 0))
        self.lbl_num_cycles.setMaximumSize(QSize(16777215, 16777215))

        self.horizontalLayout_4.addWidget(self.lbl_num_cycles)

        self.spin_num_cycles = QSpinBox(self.wgt_cycles)
        self.spin_num_cycles.setObjectName(u"spin_num_cycles")
        sizePolicy.setHeightForWidth(self.spin_num_cycles.sizePolicy().hasHeightForWidth())
        self.spin_num_cycles.setSizePolicy(sizePolicy)
        self.spin_num_cycles.setMinimumSize(QSize(0, 0))
        self.spin_num_cycles.setMaximumSize(QSize(200, 16777215))
        self.spin_num_cycles.setMinimum(1)

        self.horizontalLayout_4.addWidget(self.spin_num_cycles)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer_2)

        self.lbl_tend = QLabel(self.wgt_cycles)
        self.lbl_tend.setObjectName(u"lbl_tend")
        self.lbl_tend.setFont(font)

        self.horizontalLayout_4.addWidget(self.lbl_tend)

        self.le_tend = QLineEdit(self.wgt_cycles)
        self.le_tend.setObjectName(u"le_tend")
        sizePolicy1.setHeightForWidth(self.le_tend.sizePolicy().hasHeightForWidth())
        self.le_tend.setSizePolicy(sizePolicy1)
        self.le_tend.setReadOnly(True)

        self.horizontalLayout_4.addWidget(self.le_tend)


        self.verticalLayout.addLayout(self.horizontalLayout_4)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.lbl_num_cycles_min = QLabel(self.wgt_cycles)
        self.lbl_num_cycles_min.setObjectName(u"lbl_num_cycles_min")
        sizePolicy2.setHeightForWidth(self.lbl_num_cycles_min.sizePolicy().hasHeightForWidth())
        self.lbl_num_cycles_min.setSizePolicy(sizePolicy2)
        self.lbl_num_cycles_min.setMinimumSize(QSize(0, 0))

        self.horizontalLayout_3.addWidget(self.lbl_num_cycles_min)

        self.slider_num_cycles = QSlider(self.wgt_cycles)
        self.slider_num_cycles.setObjectName(u"slider_num_cycles")
        self.slider_num_cycles.setMinimum(1)
        self.slider_num_cycles.setMaximum(1000)
        self.slider_num_cycles.setOrientation(Qt.Orientation.Horizontal)

        self.horizontalLayout_3.addWidget(self.slider_num_cycles)

        self.lbl_num_cycles_max = QLabel(self.wgt_cycles)
        self.lbl_num_cycles_max.setObjectName(u"lbl_num_cycles_max")
        self.lbl_num_cycles_max.setMinimumSize(QSize(75, 0))
        self.lbl_num_cycles_max.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.horizontalLayout_3.addWidget(self.lbl_num_cycles_max)


        self.verticalLayout.addLayout(self.horizontalLayout_3)


        self.verticalLayout_3.addLayout(self.verticalLayout)


        self.verticalLayout_4.addWidget(self.wgt_cycles)

        self.verticalSpacer = QSpacerItem(20, 180, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_4.addItem(self.verticalSpacer)

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

        self.verticalLayout_4.addLayout(self.horizontalLayout_buttons)

        self.verticalLayout_4.setStretch(0, 1)
        self.verticalLayout_4.setStretch(1, 1)
        self.verticalLayout_4.setStretch(2, 1)

        self.retranslateUi(NumCyclesPanel)

        QMetaObject.connectSlotsByName(NumCyclesPanel)
    # setupUi

    def retranslateUi(self, NumCyclesPanel):
        NumCyclesPanel.setWindowTitle(QCoreApplication.translate("NumCyclesPanel", u"Form", None))
        self.lbl_first_cycle.setText(QCoreApplication.translate("NumCyclesPanel", u"<html><head/><body><p><span style=\" font-size:12pt;\">\u041f\u0435\u0440\u0432\u044b\u0439 \u0446\u0438\u043a\u043b</span></p></body></html>", None))
        self.lbl_tstart.setText(QCoreApplication.translate("NumCyclesPanel", u"t=", None))
        self.le_tstart.setText(QCoreApplication.translate("NumCyclesPanel", u"0.000001", None))
        self.lbl_first_cycle_min.setText(QCoreApplication.translate("NumCyclesPanel", u"<html><head/><body><p><span style=\" font-size:12pt;\">1</span></p></body></html>", None))
        self.lbl_first_cycle_max.setText(QCoreApplication.translate("NumCyclesPanel", u"<html><head/><body><p><span style=\" font-size:12pt;\">1000</span></p></body></html>", None))
        self.lbl_num_cycles.setText(QCoreApplication.translate("NumCyclesPanel", u"<html><head/><body><p><span style=\" font-size:12pt;\">\u041a\u043e\u043b\u0438\u0447\u0435\u0441\u0442\u0432\u043e \u0446\u0438\u043a\u043b\u043e\u0432</span></p></body></html>", None))
        self.lbl_tend.setText(QCoreApplication.translate("NumCyclesPanel", u"t=", None))
        self.le_tend.setText(QCoreApplication.translate("NumCyclesPanel", u"60.000001", None))
        self.lbl_num_cycles_min.setText(QCoreApplication.translate("NumCyclesPanel", u"<html><head/><body><p><span style=\" font-size:12pt;\">1</span></p></body></html>", None))
        self.lbl_num_cycles_max.setText(QCoreApplication.translate("NumCyclesPanel", u"<html><head/><body><p><span style=\" font-size:12pt;\">1000</span></p></body></html>", None))
        self.btn_cancel.setText(QCoreApplication.translate("NumCyclesPanel", u"\u041e\u0442\u043c\u0435\u043d\u0430", None))
        self.btn_apply.setText(QCoreApplication.translate("NumCyclesPanel", u"\u041f\u0440\u0438\u043c\u0435\u043d\u0438\u0442\u044c", None))
    # retranslateUi

