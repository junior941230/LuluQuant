# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'UImainWindow.ui'
##
## Created by: Qt User Interface Compiler version 6.10.2
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
from PySide6.QtWidgets import (QApplication, QDateEdit, QDoubleSpinBox, QHBoxLayout,
    QLabel, QLineEdit, QMainWindow, QMenuBar,
    QPushButton, QRadioButton, QSizePolicy, QSpinBox,
    QStatusBar, QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1920, 1080)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayoutWidget = QWidget(self.centralwidget)
        self.verticalLayoutWidget.setObjectName(u"verticalLayoutWidget")
        self.verticalLayoutWidget.setGeometry(QRect(160, 30, 1751, 1001))
        self.chartLayout = QVBoxLayout(self.verticalLayoutWidget)
        self.chartLayout.setObjectName(u"chartLayout")
        self.chartLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayoutWidget_2 = QWidget(self.centralwidget)
        self.verticalLayoutWidget_2.setObjectName(u"verticalLayoutWidget_2")
        self.verticalLayoutWidget_2.setGeometry(QRect(0, 0, 151, 311))
        self.verticalLayout = QVBoxLayout(self.verticalLayoutWidget_2)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.label = QLabel(self.verticalLayoutWidget_2)
        self.label.setObjectName(u"label")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)

        self.verticalLayout.addWidget(self.label)

        self.UserInStockID = QLineEdit(self.verticalLayoutWidget_2)
        self.UserInStockID.setObjectName(u"UserInStockID")

        self.verticalLayout.addWidget(self.UserInStockID)

        self.label_2 = QLabel(self.verticalLayoutWidget_2)
        self.label_2.setObjectName(u"label_2")

        self.verticalLayout.addWidget(self.label_2)

        self.UserInFund = QSpinBox(self.verticalLayoutWidget_2)
        self.UserInFund.setObjectName(u"UserInFund")
        self.UserInFund.setMaximum(1000000)
        self.UserInFund.setSingleStep(10000)
        self.UserInFund.setValue(500000)

        self.verticalLayout.addWidget(self.UserInFund)

        self.label_4 = QLabel(self.verticalLayoutWidget_2)
        self.label_4.setObjectName(u"label_4")

        self.verticalLayout.addWidget(self.label_4)

        self.UserInFee = QDoubleSpinBox(self.verticalLayoutWidget_2)
        self.UserInFee.setObjectName(u"UserInFee")
        self.UserInFee.setDecimals(4)
        self.UserInFee.setMaximum(5.000000000000000)
        self.UserInFee.setSingleStep(0.010000000000000)
        self.UserInFee.setValue(0.142500000000000)

        self.verticalLayout.addWidget(self.UserInFee)

        self.label_5 = QLabel(self.verticalLayoutWidget_2)
        self.label_5.setObjectName(u"label_5")

        self.verticalLayout.addWidget(self.label_5)

        self.UserInStartDate = QDateEdit(self.verticalLayoutWidget_2)
        self.UserInStartDate.setObjectName(u"UserInStartDate")
        self.UserInStartDate.setDate(QDate(2024, 4, 1))

        self.verticalLayout.addWidget(self.UserInStartDate)

        self.label_3 = QLabel(self.verticalLayoutWidget_2)
        self.label_3.setObjectName(u"label_3")

        self.verticalLayout.addWidget(self.label_3)

        self.UserInEndDate = QDateEdit(self.verticalLayoutWidget_2)
        self.UserInEndDate.setObjectName(u"UserInEndDate")
        self.UserInEndDate.setDate(QDate(2026, 3, 6))

        self.verticalLayout.addWidget(self.UserInEndDate)

        self.UserInStartBackTest = QPushButton(self.verticalLayoutWidget_2)
        self.UserInStartBackTest.setObjectName(u"UserInStartBackTest")

        self.verticalLayout.addWidget(self.UserInStartBackTest)

        self.horizontalLayoutWidget = QWidget(self.centralwidget)
        self.horizontalLayoutWidget.setObjectName(u"horizontalLayoutWidget")
        self.horizontalLayoutWidget.setGeometry(QRect(160, 0, 161, 31))
        self.CandleMode = QHBoxLayout(self.horizontalLayoutWidget)
        self.CandleMode.setObjectName(u"CandleMode")
        self.CandleMode.setContentsMargins(0, 0, 0, 0)
        self.UserInDayCandleMode = QRadioButton(self.horizontalLayoutWidget)
        self.UserInDayCandleMode.setObjectName(u"UserInDayCandleMode")
        font = QFont()
        font.setPointSize(12)
        font.setBold(True)
        self.UserInDayCandleMode.setFont(font)
        self.UserInDayCandleMode.setChecked(True)

        self.CandleMode.addWidget(self.UserInDayCandleMode)

        self.UserInWeekCandleMode = QRadioButton(self.horizontalLayoutWidget)
        self.UserInWeekCandleMode.setObjectName(u"UserInWeekCandleMode")
        self.UserInWeekCandleMode.setFont(font)

        self.CandleMode.addWidget(self.UserInWeekCandleMode)

        self.UserInMonthCandleMode = QRadioButton(self.horizontalLayoutWidget)
        self.UserInMonthCandleMode.setObjectName(u"UserInMonthCandleMode")
        self.UserInMonthCandleMode.setFont(font)

        self.CandleMode.addWidget(self.UserInMonthCandleMode)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1920, 21))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"\u6a19\u7684", None))
        self.UserInStockID.setText(QCoreApplication.translate("MainWindow", u"00940", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"\u521d\u59cb\u8cc7\u91d1", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"\u624b\u7e8c\u8cbb%", None))
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"\u8d77\u59cb\u65e5\u671f", None))
        self.UserInStartDate.setDisplayFormat(QCoreApplication.translate("MainWindow", u"yyyy-M-d", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"\u7d50\u675f\u65e5\u671f", None))
        self.UserInEndDate.setDisplayFormat(QCoreApplication.translate("MainWindow", u"yyyy-M-d", None))
        self.UserInStartBackTest.setText(QCoreApplication.translate("MainWindow", u"\u958b\u59cb\u56de\u6e2c", None))
        self.UserInDayCandleMode.setText(QCoreApplication.translate("MainWindow", u"\u5929", None))
        self.UserInWeekCandleMode.setText(QCoreApplication.translate("MainWindow", u"\u5468", None))
        self.UserInMonthCandleMode.setText(QCoreApplication.translate("MainWindow", u"\u6708", None))
    # retranslateUi

