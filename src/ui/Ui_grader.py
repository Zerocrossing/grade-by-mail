# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'grader.ui'
##
## Created by: Qt User Interface Compiler version 5.15.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1041, 823)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setUnifiedTitleAndToolBarOnMac(True)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy)
        self.gridLayout = QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.nameplate = QLabel(self.centralwidget)
        self.nameplate.setObjectName(u"nameplate")
        self.nameplate.setMaximumSize(QSize(16777215, 50))
        font = QFont()
        font.setFamily(u"Arial")
        font.setPointSize(16)
        self.nameplate.setFont(font)
        self.nameplate.setAlignment(Qt.AlignCenter)

        self.verticalLayout.addWidget(self.nameplate)

        self.grade_comments_layout = QGridLayout()
        self.grade_comments_layout.setObjectName(u"grade_comments_layout")
        self.grades = QLabel(self.centralwidget)
        self.grades.setObjectName(u"grades")
        self.grades.setMaximumSize(QSize(16777215, 50))
        self.grades.setFont(font)
        self.grades.setAlignment(Qt.AlignCenter)

        self.grade_comments_layout.addWidget(self.grades, 0, 0, 1, 1)

        self.comment = QLabel(self.centralwidget)
        self.comment.setObjectName(u"comment")
        self.comment.setMaximumSize(QSize(16777215, 50))
        self.comment.setFont(font)
        self.comment.setAlignment(Qt.AlignCenter)

        self.grade_comments_layout.addWidget(self.comment, 0, 1, 1, 1)

        self.grades_layout = QVBoxLayout()
        self.grades_layout.setObjectName(u"grades_layout")
        self.grade_layout = QHBoxLayout()
        self.grade_layout.setObjectName(u"grade_layout")
        self.req_label = QLabel(self.centralwidget)
        self.req_label.setObjectName(u"req_label")

        self.grade_layout.addWidget(self.req_label)

        self.grade_edit = QLineEdit(self.centralwidget)
        self.grade_edit.setObjectName(u"grade_edit")
        self.grade_edit.setMaximumSize(QSize(30, 16777215))

        self.grade_layout.addWidget(self.grade_edit)

        self.total_label = QLabel(self.centralwidget)
        self.total_label.setObjectName(u"total_label")
        self.total_label.setMaximumSize(QSize(30, 16777215))

        self.grade_layout.addWidget(self.total_label)


        self.grades_layout.addLayout(self.grade_layout)


        self.grade_comments_layout.addLayout(self.grades_layout, 1, 0, 1, 1)

        self.comment_text = QPlainTextEdit(self.centralwidget)
        self.comment_text.setObjectName(u"comment_text")

        self.grade_comments_layout.addWidget(self.comment_text, 1, 1, 1, 1)


        self.verticalLayout.addLayout(self.grade_comments_layout)

        self.partner_layout = QFormLayout()
        self.partner_layout.setObjectName(u"partner_layout")
        self.partner_line = QLineEdit(self.centralwidget)
        self.partner_line.setObjectName(u"partner_line")
        self.partner_line.setMaximumSize(QSize(125, 16777215))

        self.partner_layout.setWidget(0, QFormLayout.FieldRole, self.partner_line)

        self.partnerLabel = QLabel(self.centralwidget)
        self.partnerLabel.setObjectName(u"partnerLabel")
        font1 = QFont()
        font1.setFamily(u"Arial")
        font1.setPointSize(12)
        self.partnerLabel.setFont(font1)

        self.partner_layout.setWidget(0, QFormLayout.LabelRole, self.partnerLabel)


        self.verticalLayout.addLayout(self.partner_layout)

        self.btns_layout = QHBoxLayout()
        self.btns_layout.setObjectName(u"btns_layout")
        self.btn_prev = QPushButton(self.centralwidget)
        self.btn_prev.setObjectName(u"btn_prev")
        self.btn_prev.setFont(font)

        self.btns_layout.addWidget(self.btn_prev)

        self.btn_save = QPushButton(self.centralwidget)
        self.btn_save.setObjectName(u"btn_save")
        self.btn_save.setFont(font)

        self.btns_layout.addWidget(self.btn_save)

        self.btn_next = QPushButton(self.centralwidget)
        self.btn_next.setObjectName(u"btn_next")
        self.btn_next.setFont(font)

        self.btns_layout.addWidget(self.btn_next)


        self.verticalLayout.addLayout(self.btns_layout)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setSpacing(6)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.horizontalLayout.setContentsMargins(0, -1, -1, -1)
        self.btn_restore = QPushButton(self.centralwidget)
        self.btn_restore.setObjectName(u"btn_restore")
        self.btn_restore.setEnabled(True)
        self.btn_restore.setFont(font)

        self.horizontalLayout.addWidget(self.btn_restore)

        self.btn_load = QPushButton(self.centralwidget)
        self.btn_load.setObjectName(u"btn_load")
        self.btn_load.setEnabled(True)
        self.btn_load.setFont(font)

        self.horizontalLayout.addWidget(self.btn_load)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.btn_complete = QPushButton(self.centralwidget)
        self.btn_complete.setObjectName(u"btn_complete")
        self.btn_complete.setFont(font)

        self.verticalLayout.addWidget(self.btn_complete)

        self.progressBar = QProgressBar(self.centralwidget)
        self.progressBar.setObjectName(u"progressBar")
        self.progressBar.setValue(24)

        self.verticalLayout.addWidget(self.progressBar)


        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setEnabled(True)
        self.menubar.setGeometry(QRect(0, 0, 1041, 21))
        self.menuasdf = QMenu(self.menubar)
        self.menuasdf.setObjectName(u"menuasdf")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        self.statusbar.setEnabled(True)
        MainWindow.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menuasdf.menuAction())

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.nameplate.setText(QCoreApplication.translate("MainWindow", u"StudentID", None))
        self.grades.setText(QCoreApplication.translate("MainWindow", u"Grades", None))
        self.comment.setText(QCoreApplication.translate("MainWindow", u"Comment", None))
        self.req_label.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.total_label.setText(QCoreApplication.translate("MainWindow", u"/100", None))
        self.partnerLabel.setText(QCoreApplication.translate("MainWindow", u"Partner", None))
        self.btn_prev.setText(QCoreApplication.translate("MainWindow", u"Previous", None))
        self.btn_save.setText(QCoreApplication.translate("MainWindow", u"Save", None))
        self.btn_next.setText(QCoreApplication.translate("MainWindow", u"Next", None))
        self.btn_restore.setText(QCoreApplication.translate("MainWindow", u"RESTORE", None))
        self.btn_load.setText(QCoreApplication.translate("MainWindow", u"LOAD", None))
        self.btn_complete.setText(QCoreApplication.translate("MainWindow", u"Toggle Complete", None))
        self.menuasdf.setTitle(QCoreApplication.translate("MainWindow", u"Grader", None))
    # retranslateUi

