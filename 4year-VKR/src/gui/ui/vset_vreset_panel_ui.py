# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'vset_vreset_panel.ui'
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
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QPushButton, QSizePolicy,
    QSpacerItem, QStackedWidget, QVBoxLayout, QWidget)

class Ui_VsetVresetPanel(object):
    def setupUi(self, VsetVresetPanel):
        if not VsetVresetPanel.objectName():
            VsetVresetPanel.setObjectName(u"VsetVresetPanel")
        VsetVresetPanel.resize(712, 410)
        self.verticalLayout_3 = QVBoxLayout(VsetVresetPanel)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.stack = QStackedWidget(VsetVresetPanel)
        self.stack.setObjectName(u"stack")
        self.mpl_canvas_1 = QWidget()
        self.mpl_canvas_1.setObjectName(u"mpl_canvas_1")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.mpl_canvas_1.sizePolicy().hasHeightForWidth())
        self.mpl_canvas_1.setSizePolicy(sizePolicy)
        self.verticalLayout = QVBoxLayout(self.mpl_canvas_1)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.stack.addWidget(self.mpl_canvas_1)
        self.mpl_canvas_2 = QWidget()
        self.mpl_canvas_2.setObjectName(u"mpl_canvas_2")
        sizePolicy.setHeightForWidth(self.mpl_canvas_2.sizePolicy().hasHeightForWidth())
        self.mpl_canvas_2.setSizePolicy(sizePolicy)
        self.verticalLayout_2 = QVBoxLayout(self.mpl_canvas_2)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.stack.addWidget(self.mpl_canvas_2)

        self.verticalLayout_3.addWidget(self.stack)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.btn_trend = QPushButton(VsetVresetPanel)
        self.btn_trend.setObjectName(u"btn_trend")

        self.horizontalLayout_2.addWidget(self.btn_trend)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_3)

        self.btn_distribution = QPushButton(VsetVresetPanel)
        self.btn_distribution.setObjectName(u"btn_distribution")

        self.horizontalLayout_2.addWidget(self.btn_distribution)

        self.horizontalLayout_2.setStretch(0, 1)
        self.horizontalLayout_2.setStretch(1, 2)
        self.horizontalLayout_2.setStretch(2, 1)

        self.verticalLayout_3.addLayout(self.horizontalLayout_2)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.btn_export = QPushButton(VsetVresetPanel)
        self.btn_export.setObjectName(u"btn_export")

        self.horizontalLayout.addWidget(self.btn_export)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_2)

        self.horizontalLayout.setStretch(0, 1)
        self.horizontalLayout.setStretch(1, 1)
        self.horizontalLayout.setStretch(2, 1)

        self.verticalLayout_3.addLayout(self.horizontalLayout)


        self.retranslateUi(VsetVresetPanel)

        self.stack.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(VsetVresetPanel)
    # setupUi

    def retranslateUi(self, VsetVresetPanel):
        VsetVresetPanel.setWindowTitle(QCoreApplication.translate("VsetVresetPanel", u"Form", None))
        self.btn_trend.setText(QCoreApplication.translate("VsetVresetPanel", u"\u0422\u0440\u0435\u043d\u0434", None))
        self.btn_distribution.setText(QCoreApplication.translate("VsetVresetPanel", u"\u0420\u0430\u0441\u043f\u0440\u0435\u0434\u0435\u043b\u0435\u043d\u0438\u0435", None))
        self.btn_export.setText(QCoreApplication.translate("VsetVresetPanel", u"\u042d\u043a\u0441\u043f\u043e\u0440\u0442", None))
    # retranslateUi

