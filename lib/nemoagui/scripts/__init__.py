#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__  = 'Patrick Michl'
__email__   = 'patrick.michl@gmail.com'
__license__ = 'GPLv3'


import nemoa
from PySide import QtGui, QtCore
import sys

class MainWindow(QtGui.QMainWindow):

    settings = None

    def __init__(self):
        super(MainWindow, self).__init__()

        self.readSettings()

        # setup MDI area
        self.mdiArea = QtGui.QMdiArea()
        self.mdiArea.setHorizontalScrollBarPolicy(
            QtCore.Qt.ScrollBarAsNeeded)
        self.mdiArea.setVerticalScrollBarPolicy(
            QtCore.Qt.ScrollBarAsNeeded)
        self.setCentralWidget(self.mdiArea)

        self.createActions()
        self.createMenus()
        self.createToolBars()
        self.createStatusBar()
        self.createDocks()

        self.setUnifiedTitleAndToolBarOnMac(True)
        self.updateChangeWorkspace()

    def about(self):

        amail = nemoa.about('email')
        aversion = nemoa.about('version')
        acopyright = nemoa.about('copyright')
        adesc = nemoa.about('description').replace('\n', '<br>')
        acredits = '</i>, <i>'.join(nemoa.about('credits'))
        alicense = nemoa.about('license')

        #import urlparse
        #import urllib
        #lfile = self.getPath('logo', 'nemoa-logo-small.png')
        #luri = urlparse.urljoin('file:', urllib.pathname2url(lfile))
        #print luri

        msgText = (
            "<h1>nemoa</h1>"
            "<b>version</b> %s<br>",
            "<i>%s</i>"
            "<h3>Copyright</h3>"
            "%s <a href = 'mailto:%s'>&lt;%s&gt;</a>"
            "<h3>License</h3>"
            "This software may be used under the terms of the "
            "%s as published by the "
            "<a href='https://gnu.org/licenses/gpl.html'>"
            "Free Software Foundation</a>."
            "<h3>Credits</h3>"
            "<i>%s</i>"
            "<h3>Third Party Credits</h3>"
            "<a href='https://www.archlinux.org/packages/extra/any/"
            "oxygen-icons/'>Oxygen icon set</a>, license: LGPL" % (
            aversion, adesc, acopyright, amail,
            amail, alicense, acredits))

        #msgStyle = (
            #"QMessageBox { background-image: url(%s); }")
        #msgStyle = (
            #"QMessageBox QPushButton {color: white;}")

        #msgBox = QtGui.QMessageBox()
        #msgBox.setStyleSheet(msgStyle)

        aboutBox = QtGui.QMessageBox.about(self, "About Nemoa", msgText)

    def closeEvent(self, event):
        event.accept()
        if self.maybeSave():
            self.writeSettings()
            event.accept()
        else:
            event.ignore()

    def closeWorkspace(self):
        nemoa.close()
        self.updateChangeWorkspace()

    def createActions(self):
        self.actNewProject = QtGui.QAction(
            self.getIcon('actions', 'window-new.png'),
            "&New Project", self,
            shortcut = "Ctrl+N",
            statusTip = "Create a new workspace",
            triggered = self.newWorkspace)
        self.actOpenProject = QtGui.QAction(
            self.getIcon('actions', 'project-open.png'),
            '&Open Poject', self,
            shortcut = "Ctrl+O",
            statusTip = "Open an existing project",
            triggered = self.openWorkspace)
        self.actSaveProject = QtGui.QAction(
            self.getIcon('actions', 'document-save-all.png'),
            '&Save Project', self,
            shortcut = "Ctrl+S",
            statusTip = "Save current workspace to disk",
            triggered = self.saveWorkspace)
        self.actCloseProject = QtGui.QAction(
            self.getIcon('actions', 'project-development-close.png'),
            "Close Project", self,
            shortcut = "Ctrl+W",
            statusTip = "Close current project",
            triggered = self.closeWorkspace)
        self.actSaveAsFile = QtGui.QAction(
            self.getIcon('actions', 'document-save-as.png'),
            'Save as...', self,
            statusTip = "Save current workspace in new directory",
            triggered = self.saveWorkspaceAs)
        self.actPrintFile = QtGui.QAction(
            self.getIcon('actions', 'document-print.png'),
            "&Print", self,
            shortcut = QtGui.QKeySequence.Print,
            statusTip = "Print the document",
            triggered = self.printFile)
        self.actExit = QtGui.QAction(
            self.getIcon('actions', 'window-close.png'),
            "Exit", self,
            shortcut = "Ctrl+Q",
            statusTip = "Exit the application",
            triggered = self.close)
        self.actAbout = QtGui.QAction(
            self.getIcon('actions', 'help-about.png'),
            "About", self,
            statusTip = "About nemoa",
            triggered = self.about)

    def createDocks(self):

        self.createDockObjects()
        self.createDockTools()

    def createDockObjects(self):

        dock = QtGui.QDockWidget("Objects", self)
        dock.setTitleBarWidget(QtGui.QWidget())
        dock.setAllowedAreas(QtCore.Qt.LeftDockWidgetArea \
            | QtCore.Qt.RightDockWidgetArea)
        widget = QtGui.QWidget(dock)
        self.treeWidget = QtGui.QTreeWidget(widget)
        self.treeWidget.setColumnCount( 1 )
        self.treeWidget.setHeaderLabels( ('Objects', ) )
        self.treeWidget.itemDoubleClicked.connect(self.openObject)
        self.treeWidget.setIconSize(QtCore.QSize(22, 22))
        #self.button1 = QtGui.QPushButton('Show')
        #self.button1.clicked.connect(self.doShowObject)

        #stylesheet = \
            #".QPushButton {\n" \
            #+ "border: none;\n" \
            #+ "background: none;\n" \
            #+ "}"

        #self.button1.setIcon(QtGui.QIcon(":/images/nemoa_logo.png"))
        #self.button1.setIconSize(QtCore.QSize(16, 16))
        #self.button1.setStyleSheet(stylesheet)

        self.btEdit = QtGui.QPushButton("Edit")
        self.btEdit.clicked.connect(self.openObject)
        self.btNew = QtGui.QPushButton("New")
        self.btAdd = QtGui.QPushButton("Add")
        self.btExport = QtGui.QPushButton("Export")
        self.btDelete = QtGui.QPushButton("Delete")
        grid = QtGui.QGridLayout()
        grid.setSpacing(0)
        grid.setContentsMargins(0, 0, 0, 0)
        grid.addWidget(self.btEdit, 1, 0)
        grid.addWidget(self.btNew, 1, 1)
        grid.addWidget(self.btAdd, 1, 2)
        grid.addWidget(self.btExport, 1, 3)
        grid.addWidget(self.btDelete, 1, 4)
        grid.addWidget(self.treeWidget, 0, 0, 1, -1)
        self.setLayout(grid)
        widget.setLayout(grid)
        dock.setWidget(widget)
        self.addDockWidget(QtCore.Qt.RightDockWidgetArea, dock)
        self.viewMenu.addAction(dock.toggleViewAction())

    def createDockTools(self):

        dock = QtGui.QDockWidget("Tools", self)
        dock.setAllowedAreas(QtCore.Qt.LeftDockWidgetArea \
            | QtCore.Qt.RightDockWidgetArea)
        self.dockDatasetList = QtGui.QListWidget(dock)
        self.dockDatasetList.setDragEnabled(True)
        #self.dockDatasetList.setAcceptDrops(True)
        self.dockDatasetList.setIconSize(QtCore.QSize(32, 32))
        self.dockDatasetList.setAlternatingRowColors(True)
        dock.setWidget(self.dockDatasetList)
        self.addDockWidget(QtCore.Qt.RightDockWidgetArea, dock)
        self.viewMenu.addAction(dock.toggleViewAction())

    def createMenus(self):
        self.fileMenu = self.menuBar().addMenu("&File")
        self.projectMenu = self.fileMenu.addMenu("&Projects")
        self.projectMenu.addAction(self.actNewProject)
        self.projectMenu.addAction(self.actOpenProject)
        self.projectMenu.addAction(self.actSaveProject)
        self.projectMenu.addAction(self.actCloseProject)
        self.fileMenu.addSeparator()
        self.fileMenu.addAction(self.actSaveAsFile)
        self.fileMenu.addAction(self.actPrintFile)
        self.fileMenu.addSeparator()
        self.fileMenu.addAction(self.actExit)
        self.viewMenu = self.menuBar().addMenu("&View")
        self.viewToolbarsMenu = self.viewMenu.addMenu("&Toolbars")
        self.aboutMenu = self.menuBar().addMenu("&Help")
        self.aboutMenu.addAction(self.actAbout)

    def createStatusBar(self):
        self.statusBar().showMessage("Ready")

    def createToolBars(self):
        self.fileToolBar = self.addToolBar("Project")
        self.fileToolBar.addAction(self.actNewProject)
        self.fileToolBar.addAction(self.actOpenProject)
        self.fileToolBar.addAction(self.actSaveProject)
        self.fileToolBar.addAction(self.actCloseProject)
        self.viewToolbarsMenu.addAction(self.fileToolBar.toggleViewAction())


        #self.editToolBar = self.addToolBar("Edit")
        #self.editToolBar.addAction(self.cutAct)
        #self.editToolBar.addAction(self.copyAct)
        #self.editToolBar.addAction(self.pasteAct)

    def createMdiChild(self, type):

        if type == ('script', 'editor'):
            from nemoagui.objects.script import Editor
            child = Editor()
        elif type == ('dataset', 'editor'):
            from nemoagui.objects.dataset import Editor
            child = Editor()
        elif type == ('model', 'editor'):
            from nemoagui.objects.model import Editor
            child = Editor()
        elif type == ('network', 'editor'):
            from nemoagui.objects.network import Editor
            child = Editor()
        elif type == ('system', 'editor'):
            from nemoagui.objects.system import Editor
            child = Editor()
        else:
            return None

        self.mdiArea.addSubWindow(child)

        #child.copyAvailable.connect(self.cutAct.setEnabled)
        #child.copyAvailable.connect(self.copyAct.setEnabled)

        return child

    def documentWasModified(self):
        modified = True
        self.setWindowModified(modified)

    def maybeSave(self):
        modified = True

        if modified:
            ret = QtGui.QMessageBox.warning(self, "Nemoa",
                "The document has been modified."
                "\nDo you want to save "
                "your changes?",
                QtGui.QMessageBox.Save | QtGui.QMessageBox.Discard |
                QtGui.QMessageBox.Cancel)
            if ret == QtGui.QMessageBox.Save:
                return self.save()
            elif ret == QtGui.QMessageBox.Cancel:
                return False

        return True

    def readSettings(self):

        # nemoa gui settings
        settings = QtCore.QSettings("Froot", "Nemoa")
        pos = settings.value("pos", QtCore.QPoint(200, 200))
        size = settings.value("size", QtCore.QSize(400, 400))

        self.resize(size)
        self.move(pos)

    def writeSettings(self):
        settings = QtCore.QSettings("Froot", "Nemoa")
        settings.setValue("pos", self.pos())
        settings.setValue("size", self.size())

    def updateWindowTitle(self):
        #self.textEdit.document().setModified(False)
        self.setWindowModified(False)
        if nemoa.get('workspace'): shownName = nemoa.get('workspace')
        else: shownName = 'untitled'
        self.setWindowTitle("%s[*] - Nemoa" % shownName)

    def updateChangeWorkspace(self):
        self.updateDockWindows()
        self.updateWindowTitle()

    def updateDockWindows(self):
        self.updateDockObjects()
        self.updateDockTools()

    def updateDockObjects(self):
        self.treeWidget.clear()
        self.treeWidget.setDragEnabled(True)
        objTypes = [
            ('model', ('mimetypes', 'application-x-designer.png')),
            ('dataset', ('mimetypes', 'text-csv.png')),
            ('network', ('mimetypes', 'text-rdf.png')),
            ('system', ('mimetypes', 'text-mathml.png')),
            ('script', ('mimetypes', 'text-x-python.png'))]
        for objType, objIconPath in objTypes:
            objList = nemoa.list(objType + 's')
            if not objList: continue
            objTypeItem = QtGui.QTreeWidgetItem(self.treeWidget,
                [objType.title() + 's', None, None])
            objTypeIcon = self.getIcon(*objIconPath)
            objTypeItem.setIcon(0, objTypeIcon)
            for objName in objList:
                objItem = QtGui.QTreeWidgetItem(objTypeItem,
                    [objName, objName, objType])
                objItem.setIcon(0, objTypeIcon)

    def updateDockTools(self):
        pass

    def openWorkspace(self):
        path = nemoa.path('basepath', 'user')
        options = QtGui.QFileDialog.DontResolveSymlinks \
            | QtGui.QFileDialog.ShowDirsOnly
        directory = QtGui.QFileDialog.getExistingDirectory(self,
            "test", path, options)
        if not directory: return False
        name = nemoa.common.ospath.basename(directory)
        if not nemoa.open(name): return False
        self.updateChangeWorkspace()

    def openObject(self, *args, **kwargs):

        # get name and type of object
        curItem = self.treeWidget.currentItem()
        objTitle = curItem.text(0)
        objName = curItem.text(1)
        objType = curItem.text(2)
        objPath = nemoa.path(objType, objName)

        #fileName, filtr = QtGui.QFileDialog.getOpenFileName(self)
        if objPath:
            existing = self.findMdiChild(objPath)
            if existing:
                self.mdiArea.setActiveSubWindow(existing)
                return
            child = self.createMdiChild(type = (objType, 'editor'))
            if child.loadFile(objPath):
                self.statusBar().showMessage("File loaded", 2000)
                child.show()
            else:
                child.close()
            return True
        return False

    def findMdiChild(self, fileName):
        canonicalFilePath = QtCore.QFileInfo(fileName).canonicalFilePath()

        for window in self.mdiArea.subWindowList():
            if window.widget().currentFile() == canonicalFilePath:
                return window
        return None

    def getPath(self, key, *args):

        import os

        if not self.settings:
            self.settings = {}

        if key == 'icons':
            if not self.settings.get('icons', None):
                self.settings['icons'] = nemoa.path('expand',
                    ('%site_data_dir%', 'images', 'icons'))
            base = self.settings['icons']
        elif key == 'logo':
            if not self.settings.get('logo', None):
                self.settings['logo'] = nemoa.path('expand',
                    ('%site_data_dir%', 'images', 'logo'))
            base = self.settings['logo']

        return os.path.sep.join([base] + list(args))

    def getIcon(self, *args):
        return QtGui.QIcon(self.getPath('icons', *args))

    def getLogo(self, *args):
        return QtGui.QIcon(self.getPath('logo', *args))

    def printFile(self):
        return True

    def newWorkspace(self):
        return True

    def save(self):
        return self.saveWorkspace()

    def saveWorkspace(self):
        return True

    def saveWorkspaceAs(self):
        return True

def main():

    nemoa.set('mode', 'silent')
    app = QtGui.QApplication(sys.argv)
    Window = MainWindow()
    Window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
