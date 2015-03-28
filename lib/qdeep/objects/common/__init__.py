# -*- coding: utf-8 -*-

__author__  = 'Patrick Michl'
__email__   = 'patrick.michl@gmail.com'
__license__ = 'GPLv3'

import nemoa
import qdeep
from PySide import QtGui, QtCore

class Editor(QtGui.QMainWindow):
    sequenceNumber = 1

    def __init__(self):
        super(Editor, self).__init__()

        self.textArea = QtGui.QTextEdit()
        self.textArea.setHorizontalScrollBarPolicy(
            QtCore.Qt.ScrollBarAsNeeded)
        self.textArea.setVerticalScrollBarPolicy(
            QtCore.Qt.ScrollBarAsNeeded)
        self.setCentralWidget(self.textArea)

        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.isUntitled = True

        self.createActions()
        self.createMenus()

    def createActions(self): pass
    def createMenus(self): pass

    def newFile(self):
        self.isUntitled = True
        self.curFile = "script%d.py" % MdiChild.sequenceNumber
        MdiChild.sequenceNumber += 1
        self.setWindowTitle(self.curFile + '[*]')

        self.textArea.document().contentsChanged.connect(
            self.documentWasModified)

    def loadFile(self, fileName):
        file = QtCore.QFile(fileName)
        if not file.open(QtCore.QFile.ReadOnly | QtCore.QFile.Text):
            QtGui.QMessageBox.warning(self, "MDI",
                "Cannot read file %s:\n%s." % (
                fileName, file.errorString()))
            return False

        instr = QtCore.QTextStream(file)
        QtGui.QApplication.setOverrideCursor(QtCore.Qt.WaitCursor)
        self.textArea.setPlainText(instr.readAll())
        QtGui.QApplication.restoreOverrideCursor()

        self.setCurrentFile(fileName)

        self.textArea.document().contentsChanged.connect(
            self.documentWasModified)

        return True

    def save(self):
        if self.isUntitled:
            return self.saveAs()
        else:
            return self.saveFile(self.curFile)

    def saveAs(self):
        fileName, filtr = QtGui.QFileDialog.getSaveFileName(
            self, "Save As", self.curFile)
        if not fileName:
            return False

        return self.saveFile(fileName)

    def saveFile(self, fileName):
        file = QtCore.QFile(fileName)

        if not file.open(QtCore.QFile.WriteOnly | QtCore.QFile.Text):
            QtGui.QMessageBox.warning(self, "MDI",
                "Cannot write file %s:\n%s." % (fileName,
                file.errorString()))
            return False

        outstr = QtCore.QTextStream(file)
        QtGui.QApplication.setOverrideCursor(QtCore.Qt.WaitCursor)
        outstr << self.textArea.toPlainText()
        QtGui.QApplication.restoreOverrideCursor()

        self.setCurrentFile(fileName)
        return True

    def userFriendlyCurrentFile(self):
        return self.strippedName(self.curFile)

    def currentFile(self):
        return self.curFile

    def closeEvent(self, event):
        if self.maybeSave():
            event.accept()
        else:
            event.ignore()

    def documentWasModified(self):
        self.setWindowModified(self.textArea.document().isModified())

    def maybeSave(self):
        if self.textArea.document().isModified():
            ret = QtGui.QMessageBox.warning(self, "MDI",
                "'%s' has been modified.\nDo you want to save your "
                "changes?" % self.userFriendlyCurrentFile(),
                QtGui.QMessageBox.Save | QtGui.QMessageBox.Discard |
                QtGui.QMessageBox.Cancel)
            if ret == QtGui.QMessageBox.Save:
                return self.save()
            elif ret == QtGui.QMessageBox.Cancel:
                return False

        return True

    def setCurrentFile(self, fileName):
        self.curFile = QtCore.QFileInfo(fileName).canonicalFilePath()
        self.isUntitled = False
        self.textArea.document().setModified(False)
        self.setWindowModified(False)
        self.setWindowTitle(self.userFriendlyCurrentFile() + "[*]")

    def strippedName(self, fullFileName):
        return QtCore.QFileInfo(fullFileName).fileName()
