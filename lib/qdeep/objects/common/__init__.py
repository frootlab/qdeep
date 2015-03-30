# -*- coding: utf-8 -*-

__author__  = 'Patrick Michl'
__email__   = 'patrick.michl@gmail.com'
__license__ = 'GPLv3'

import nemoa
import qdeep
from PySide import QtGui, QtCore

class Editor(QtGui.QMainWindow):
    sequenceNumber = 1
    settings = None
    isUntitled = True

    objInstance = None
    objName = None
    objType = None
    objPath = None

    def __init__(self):
        super(Editor, self).__init__()

        self.settings = {}

        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.isUntitled = True

        self.updateWindowTitle()

        self.createActions()
        self.createToolBars()
        self.createCentralWidget()

    def createActions(self): pass
    def createToolBars(self): pass
    def createCentralWidget(self): pass

    def newFile(self):
        self.isUntitled = True
        self.objPath = "script%d.py" % self.sequenceNumber
        self.sequenceNumber += 1
        self.setWindowTitle(self.objPath + '[*]')

    def openFromWorkspace(self, objName):

        objPath = nemoa.path(self.objType, objName)
        if not objPath: return False
        QtGui.QApplication.setOverrideCursor(QtCore.Qt.WaitCursor)
        if self.objType == 'script':
            instance = None
            retVal = self.loadFile(objPath)
        else:
            instance = nemoa.open(self.objType, objName)
            retVal = bool(instance)
        QtGui.QApplication.restoreOverrideCursor()

        if not retVal:
            QtGui.QMessageBox.warning(self, "MDI",
                "Cannot open %s '%s':\n%s." % (
                self.getType(), objName, '2Do: nemoa error message'))
            return False

        self.objName = objName
        self.objPath = objPath
        self.objInstance = instance

        self.isUntitled = False
        self.setModified(False)
        self.updateWindowTitle()

        return True

    def getType(self):
        return self.objType

    def getName(self):
        return self.objInstance.name \
            if self.objInstance else self.objName

    def getPath(self):
        return self.objInstance.path \
            if self.objInstance else self.objPath

    def getTitle(self):
        path = self.getPath()
        if path: return QtCore.QFileInfo(path).fileName()
        return 'untitled'

    def save(self):
        if self.isUntitled: return self.saveAs()
        return self.saveFile(self.getPath())

    def saveAs(self):
        fileName, filtr = QtGui.QFileDialog.getSaveFileName(
            self, "Save As", self.objPath)
        if not fileName: return False
        #2do: change name of object
        return self.saveFile(fileName)

    def saveFile(self, *args, **kwargs):
        if self.objInstance.save(*args, **kwargs):
            self.isUntitled = False
            self.updateWindowTitle()
            return True
        return False

    def closeEvent(self, event):
        if self.maybeSave(): event.accept()
        else: event.ignore()

    def documentWasModified(self):
        self.setWindowModified(self.getModified())

    def getModified(self):
        return False

    def setModified(self, value):
        pass

    def maybeSave(self):
        if self.getModified():
            ret = QtGui.QMessageBox.warning(self, "MDI",
                "'%s' has been modified.\nDo you want to save your "
                "changes?" % self.getTitle(),
                QtGui.QMessageBox.Save | QtGui.QMessageBox.Discard |
                QtGui.QMessageBox.Cancel)
            if ret == QtGui.QMessageBox.Save:
                return self.save()
            elif ret == QtGui.QMessageBox.Cancel:
                return False
        return True

    def updateWindowTitle(self):
        self.setWindowTitle(self.getTitle() + "[*]")
        self.setWindowModified(False)
