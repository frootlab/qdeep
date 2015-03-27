# -*- coding: utf-8 -*-

__author__  = 'Patrick Michl'
__email__   = 'patrick.michl@gmail.com'
__license__ = 'GPLv3'

import nemoa
import nemoagui.objects.common
from PySide import QtGui, QtCore, QtSql

class Editor(nemoagui.objects.common.Editor):

    def loadFile(self, fileName):

        dataset = nemoa.dataset.open(fileName)

        print dataset.columns

        file = QtCore.QFile(fileName)
        if not file.open(QtCore.QFile.ReadOnly | QtCore.QFile.Text):
            QtGui.QMessageBox.warning(self, "MDI",
                "Cannot read file %s:\n%s." % (
                fileName, file.errorString()))
            return False

        instr = QtCore.QTextStream(file)
        QtGui.QApplication.setOverrideCursor(QtCore.Qt.WaitCursor)
        self.setPlainText(instr.readAll())
        QtGui.QApplication.restoreOverrideCursor()

        self.setCurrentFile(fileName)

        self.document().contentsChanged.connect(
            self.documentWasModified)

        return True
