#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''DOCSTRING'''

import sys
import os
from PyQt5 import uic, QtCore, QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow

from mathcad2smath.converter import ConverterSetup
from mathcad2smath.converter import run


DIRNAME = os.path.dirname(__file__)


class MainApp(QMainWindow):
    """Main app"""

    def __init__(self) -> None:
        super().__init__()
        uic.loadUi(os.path.join(DIRNAME, 'app.ui'), self)
        self.button_convert.clicked.connect(self.run_and_wait)
        self.show()

    def run(self):
        """Run the converter"""
        setup = ConverterSetup(
            ignore_custom=False,
            basedir='.',
            overwrite=True,
            recursive=True,
            prefix='',
            sufix='',
            add_external=[],
            external_path='.',
            filename='',
            smath_path=r'C:\Program Files (x86)\SMath Studio',
            save_as_sm=True
        )
        print('Running')
        self.setEnabled(False)
        run(setup)
        from time import sleep
        sleep(5)
        self.setEnabled(True)
        print('Done')

    def run_and_wait(self):
        QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.WaitCursor))
        # if incase function failed then restore it
        try:
            self.run()
            QApplication.restoreOverrideCursor()
        except:
            QApplication.restoreOverrideCursor()


def window():
    '''Create a simple test app'''
    app = QApplication(sys.argv)
    win = MainApp()
    sys.exit(app.exec_())


window()
