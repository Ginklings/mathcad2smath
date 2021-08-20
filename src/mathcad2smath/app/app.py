#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''DOCSTRING'''

import sys
import os
from PyQt5 import uic, QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog,\
    QPushButton, QVBoxLayout, QFileDialog

from mathcad2smath.converter import ConverterSetup
from mathcad2smath.converter import run


DIRNAME = os.path.dirname(__file__)


class RunnerDialog(QDialog):
    """Popup for run the converter"""

    def __init__(self, parent, flags) -> None:
        super().__init__(parent=parent, flags=flags)
        size_policy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        size_policy.setHorizontalStretch(0)
        size_policy.setVerticalStretch(0)
        size_policy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(size_policy)
        self.setMinimumSize(QtCore.QSize(200, 45))
        self.setMaximumSize(QtCore.QSize(200, 45))
        self.setWindowFlags( QtCore.Qt.CustomizeWindowHint )
        ok_bt = QPushButton('Converted!')
        ok_bt.setFixedSize(120, 30)
        ok_bt.clicked.connect(self.close)
        boxlayout = QVBoxLayout(self)
        boxlayout.setAlignment(QtCore.Qt.AlignCenter)
        boxlayout.addWidget(ok_bt)


class MainApp(QMainWindow):
    """Main app"""

    def __init__(self) -> None:
        super().__init__()
        uic.loadUi(os.path.join(DIRNAME, 'app.ui'), self)
        self.button_convert.clicked.connect(self.run_and_wait)
        self.bt_basedir.clicked.connect(self.select_and_set_folder(self.edit_basedir, 'file'))
        self.bt_smath_path.clicked.connect(self.select_and_set_folder(self.edit_smath_path))
        self.bt_external_file.clicked.connect(self.create_external_files_list)
        self.single_file_mode.clicked.connect(self.set_single_mode)
        self.multi_files_mode.clicked.connect(self.set_multi_mode)
        self.edit_external_file.textChanged.connect(self.update_external_files)
        self.last_external_folder = ''
        self.show()
        
    def set_single_mode(self):
        self.file_mode_label.setText('Filename:')
        self.check_recursive.setChecked(False)

    def set_multi_mode(self):
        self.file_mode_label.setText('Basedir:')
        
    def create_external_files_list(self):
        self.select_and_set_folder(self.edit_external_file)()
        
    def update_external_files(self, folder=''):
        folder = self.edit_external_file.text()
        if os.path.isdir(folder):
            if self.last_external_path_changed(folder):
                self.last_external_folder = folder
                for filename in os.listdir(folder):
                    if os.path.isfile(os.path.join(folder, filename)):
                        if filename.lower().endswith('.sm'):
                            self.list_files.addItem(filename)
                self.list_files.selectAll()
        else:
            self.list_files.clear()
         
    def last_external_path_changed(self, folder):
        changed = True
        if self.last_external_folder:
            changed = not os.path.samefile(folder, self.last_external_folder)
        return changed

    def get_item_text(self, item):
        return item.text()
        
    def get_selected_basedir(self):
        folder = self.select_folder()
        self.edit_basedir.setText(folder)
        
    def select_and_set_folder(self, edit, mode='directory'):
        def selec_and_set_folder():
            if mode == 'directory':
                folder = self.select_folder()
            else:
                folder = self.select_filename()
            edit.setText(folder)
            return folder
        return selec_and_set_folder

    def select_filename(self):
        options = QFileDialog.Options()
        filename = QFileDialog.getOpenFileName(self,"Select directory", "", "All Files (*)", options=options)
        return filename[0]

    def select_folder(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ShowDirsOnly
        basedir = QFileDialog.getExistingDirectory(self,"Select directory", "", options=options)
        return basedir

    def run_and_wait(self):
        """Run the converter task and show sucess dialog after the task"""
        dialog = RunnerDialog(None, QtCore.Qt.WindowSystemMenuHint | QtCore.Qt.WindowTitleHint)
        QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.WaitCursor))
        try:
            self.convert()
            QApplication.restoreOverrideCursor()
            dialog.exec()
        except Exception:
            QApplication.restoreOverrideCursor()

    def convert(self):
        """Run the converter"""
        external_file_path = self.edit_external_file.text()
        if not external_file_path:
            external_file_path = '.'
        setup = ConverterSetup(
            ignore_custom=self.check_ignore_custom.isChecked(),
            basedir=self.get_basedir(),
            overwrite=self.check_overwrite.isChecked(),
            recursive=self.check_recursive.isChecked(),
            prefix=self.edit_prefix.text(),
            sufix=self.edit_sufix.text(),
            add_external=list(map(self.get_item_text, self.list_files.selectedItems())),
            external_path=external_file_path,
            filename='',
            smath_path=self.edit_smath_path.text(),
            save_as_sm=self.check_save_as_sm.isChecked()
        )
        print('Running')
        self.setEnabled(False)
        run(setup)
        self.setEnabled(True)
        print('Done')

    def get_basedir(self):
        """Get the basedir for the converter"""
        text = self.edit_basedir.text()
        if not text:
            text = '.'
        return text


def window():
    '''Main app'''
    app = QApplication(sys.argv)
    win = MainApp()
    win.setWindowTitle('Mathcad XMCD to Smath Converter')
    sys.exit(app.exec_())


window()
