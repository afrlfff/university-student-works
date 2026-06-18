# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main_window.ui'
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
from PySide6.QtWidgets import (QApplication, QGroupBox, QHBoxLayout, QMainWindow,
    QPushButton, QScrollArea, QSizePolicy, QSpacerItem,
    QStackedWidget, QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(967, 650)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.horizontalLayout = QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.scroll = QScrollArea(self.centralwidget)
        self.scroll.setObjectName(u"scroll")
        self.scroll.setMinimumSize(QSize(250, 0))
        self.scroll.setMaximumSize(QSize(300, 16777215))
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.scroll.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 296, 628))
        self.verticalLayout_5 = QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_5.setSpacing(0)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.grp_data_load = QGroupBox(self.scrollAreaWidgetContents)
        self.grp_data_load.setObjectName(u"grp_data_load")
        self.verticalLayout = QVBoxLayout(self.grp_data_load)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.btn_data_load = QPushButton(self.grp_data_load)
        self.btn_data_load.setObjectName(u"btn_data_load")

        self.verticalLayout.addWidget(self.btn_data_load)


        self.verticalLayout_5.addWidget(self.grp_data_load)

        self.verticalSpacer = QSpacerItem(20, 77, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_5.addItem(self.verticalSpacer)

        self.grp_setup = QGroupBox(self.scrollAreaWidgetContents)
        self.grp_setup.setObjectName(u"grp_setup")
        self.verticalLayout_2 = QVBoxLayout(self.grp_setup)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.btn_num_cycles = QPushButton(self.grp_setup)
        self.btn_num_cycles.setObjectName(u"btn_num_cycles")

        self.verticalLayout_2.addWidget(self.btn_num_cycles)

        self.btn_set_reset = QPushButton(self.grp_setup)
        self.btn_set_reset.setObjectName(u"btn_set_reset")

        self.verticalLayout_2.addWidget(self.btn_set_reset)


        self.verticalLayout_5.addWidget(self.grp_setup)

        self.verticalSpacer_3 = QSpacerItem(20, 11, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_5.addItem(self.verticalSpacer_3)

        self.grp_search = QGroupBox(self.scrollAreaWidgetContents)
        self.grp_search.setObjectName(u"grp_search")
        self.verticalLayout_4 = QVBoxLayout(self.grp_search)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.btn_shottky_search = QPushButton(self.grp_search)
        self.btn_shottky_search.setObjectName(u"btn_shottky_search")

        self.verticalLayout_4.addWidget(self.btn_shottky_search)

        self.btn_switching_params_calc = QPushButton(self.grp_search)
        self.btn_switching_params_calc.setObjectName(u"btn_switching_params_calc")

        self.verticalLayout_4.addWidget(self.btn_switching_params_calc)


        self.verticalLayout_5.addWidget(self.grp_search)

        self.verticalSpacer_2 = QSpacerItem(20, 77, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_5.addItem(self.verticalSpacer_2)

        self.grp_param_identification = QGroupBox(self.scrollAreaWidgetContents)
        self.grp_param_identification.setObjectName(u"grp_param_identification")
        self.verticalLayout_3 = QVBoxLayout(self.grp_param_identification)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.btn_shottky = QPushButton(self.grp_param_identification)
        self.btn_shottky.setObjectName(u"btn_shottky")

        self.verticalLayout_3.addWidget(self.btn_shottky)

        self.btn_state_X = QPushButton(self.grp_param_identification)
        self.btn_state_X.setObjectName(u"btn_state_X")

        self.verticalLayout_3.addWidget(self.btn_state_X)

        self.btn_ron_roff = QPushButton(self.grp_param_identification)
        self.btn_ron_roff.setObjectName(u"btn_ron_roff")

        self.verticalLayout_3.addWidget(self.btn_ron_roff)

        self.btn_vset_vreset = QPushButton(self.grp_param_identification)
        self.btn_vset_vreset.setObjectName(u"btn_vset_vreset")

        self.verticalLayout_3.addWidget(self.btn_vset_vreset)


        self.verticalLayout_5.addWidget(self.grp_param_identification)

        self.verticalLayout_5.setStretch(1, 1)
        self.verticalLayout_5.setStretch(3, 1)
        self.verticalLayout_5.setStretch(5, 1)
        self.scroll.setWidget(self.scrollAreaWidgetContents)

        self.horizontalLayout.addWidget(self.scroll)

        self.stack = QStackedWidget(self.centralwidget)
        self.stack.setObjectName(u"stack")

        self.horizontalLayout.addWidget(self.stack)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.grp_data_load.setTitle(QCoreApplication.translate("MainWindow", u"\u0417\u0430\u0433\u0440\u0443\u0437\u043a\u0430 \u0434\u0430\u043d\u043d\u044b\u0445", None))
        self.btn_data_load.setText(QCoreApplication.translate("MainWindow", u"\u0417\u0430\u0433\u0440\u0443\u0437\u043a\u0430 \u0434\u0430\u043d\u043d\u044b\u0445", None))
        self.grp_setup.setTitle(QCoreApplication.translate("MainWindow", u"\u041d\u0430\u0441\u0442\u0440\u043e\u0439\u043a\u0430", None))
        self.btn_num_cycles.setText(QCoreApplication.translate("MainWindow", u"\u041a\u043e\u043b\u0438\u0447\u0435\u0441\u0442\u0432\u043e \u0446\u0438\u043a\u043b\u043e\u0432", None))
        self.btn_set_reset.setText(QCoreApplication.translate("MainWindow", u"\u0414\u0435\u0442\u0435\u043a\u0446\u0438\u044f SET, RESET", None))
        self.grp_search.setTitle(QCoreApplication.translate("MainWindow", u"\u0412\u044b\u0447\u0438\u0441\u043b\u0435\u043d\u0438\u0435", None))
        self.btn_shottky_search.setText(QCoreApplication.translate("MainWindow", u"\u041f\u0430\u0440\u0430\u043c\u0435\u0442\u0440\u044b \u0431\u0430\u0440\u044c\u0435\u0440\u0430 \u0428\u043e\u0442\u0442\u043a\u0438", None))
        self.btn_switching_params_calc.setText(QCoreApplication.translate("MainWindow", u"Ron, Roff, Vset, Vreset", None))
        self.grp_param_identification.setTitle(QCoreApplication.translate("MainWindow", u"\u0420\u0435\u0437\u0443\u043b\u044c\u0442\u0430\u0442\u044b", None))
        self.btn_shottky.setText(QCoreApplication.translate("MainWindow", u"\u0411\u0430\u0440\u044c\u0435\u0440 \u0428\u043e\u0442\u0442\u043a\u0438", None))
        self.btn_state_X.setText(QCoreApplication.translate("MainWindow", u"\u041f\u0435\u0440\u0435\u043c\u0435\u043d\u043d\u0430\u044f \u0441\u043e\u0441\u0442\u043e\u044f\u043d\u0438\u044f X", None))
        self.btn_ron_roff.setText(QCoreApplication.translate("MainWindow", u"Ron, Roff", None))
        self.btn_vset_vreset.setText(QCoreApplication.translate("MainWindow", u"Vset, Vreset", None))
    # retranslateUi

