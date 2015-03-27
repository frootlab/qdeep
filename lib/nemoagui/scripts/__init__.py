#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__  = 'Patrick Michl'
__email__   = 'patrick.michl@gmail.com'
__license__ = 'GPLv3'

def main():

    import nemoa

    try:
        from PySide import QtGui, QtCore, QtSql
    except ImportError:
        return nemoa.log('error',
            """could not execute nemoa gui:
            you have to install pyside.""")

    import sys
    import qtgui_rc

    class MainWindow(QtGui.QMainWindow):

        settings = None

        def __init__(self):
            super(MainWindow, self).__init__()

            # setup MDI area
            self.mdiArea = QtGui.QMdiArea()
            self.mdiArea.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
            self.mdiArea.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
            self.setCentralWidget(self.mdiArea)

            self.createActions()
            self.createMenus()
            self.createToolBars()
            self.createStatusBar()
            self.createDockWindows()

            self.readSettings()

            #self.textEdit.document().contentsChanged.connect(self.documentWasModified)

            self.setUnifiedTitleAndToolBarOnMac(True)
            self.updateChangeWorkspace()

        def documentWasModified(self):
            #modified = self.textEdit.document().isModified()
            modified = True

            self.setWindowModified(modified)

        def closeEvent(self, event):
            event.accept()
            if self.maybeSave():
                self.writeSettings()
                event.accept()
            else:
                event.ignore()

        def maybeSave(self):
            #modified = self.textEdit.document().isModified()
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

        def createActions(self):
            iconGet = self.style().standardIcon

            self.actNewFile = QtGui.QAction(
                QtGui.QIcon(':/images/nemoa_logo.png'),
                "&New", self,
                shortcut = "Ctrl+N",
                statusTip = "Create a new workspace",
                triggered = self.menuNewFile)

            self.actOpenFile = QtGui.QAction(
                iconGet(QtGui.QStyle.SP_FileDialogNewFolder),
                '&Open...', self,
                shortcut = "Ctrl+O",
                statusTip = "Open an existing workspace",
                triggered = self.menuOpenFile)

            self.actSaveFile = QtGui.QAction(
                QtGui.QIcon.fromTheme('document-save'),
                #iconGet(QtGui.QStyle.SP_DialogSaveButton),
                '&Save', self,
                shortcut = "Ctrl+S",
                statusTip = "Save the workspace to disk",
                triggered = self.menuSaveFile)

            self.actSaveAsFile = QtGui.QAction(
                'Save as...', self,
                statusTip = "Save the workspace under a new name",
                triggered = self.menuSaveFile)

            #2do only show ...
            self.actPrintFile = QtGui.QAction(
                "&Print", self,
                shortcut = QtGui.QKeySequence.Print,
                statusTip = "Print the document",
                triggered = self.menuPrintFile)

            self.actCloseFile = QtGui.QAction(
                "Close", self,
                shortcut = "Ctrl+W",
                statusTip = "Close current workspace",
                triggered = self.menuCloseFile)

            self.actExit = QtGui.QAction(
                "Exit", self,
                shortcut = "Ctrl+Q",
                statusTip = "Exit the application",
                triggered = self.close)

            self.actAbout = QtGui.QAction(
                "About", self,
                triggered = self.menuAbout)

        def createMenus(self):
            self.fileMenu = self.menuBar().addMenu("&File")
            self.fileMenu.addAction(self.actNewFile)
            self.fileMenu.addAction(self.actOpenFile)
            self.fileMenu.addAction(self.actSaveFile)
            self.fileMenu.addAction(self.actSaveAsFile)
            self.fileMenu.addAction(self.actPrintFile)
            self.fileMenu.addSeparator()
            self.fileMenu.addAction(self.actCloseFile)
            self.fileMenu.addAction(self.actExit)

            self.viewMenu = self.menuBar().addMenu("&View")

            self.aboutMenu = self.menuBar().addMenu("&Help")
            self.aboutMenu.addAction(self.actAbout)

        def createStatusBar(self):
            self.statusBar().showMessage("Ready")

        def createToolBars(self):
            self.fileToolBar = self.addToolBar("File")
            self.fileToolBar.addAction(self.actNewFile)
            self.fileToolBar.addAction(self.actOpenFile)
            self.fileToolBar.addAction(self.actSaveFile)

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

        def createDockWindows(self):

            self.createDockResource()

            dock = QtGui.QDockWidget("Datasets", self)
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

            dock = QtGui.QDockWidget("Networks", self)
            dock.setAllowedAreas(QtCore.Qt.LeftDockWidgetArea \
                | QtCore.Qt.RightDockWidgetArea)
            self.dockNetworkList = QtGui.QListWidget(dock)
            self.dockNetworkList.setDragEnabled(True)
            #self.dockNetworkList.setAlternatingRowColors(True)
            self.dockNetworkList.setIconSize(QtCore.QSize(32, 32))
            self.dockNetworkList.setAlternatingRowColors(True)
            self.dockNetworkList.currentTextChanged.connect(
                self.dockNetworkListChanged)
            dock.setWidget(self.dockNetworkList)
            self.addDockWidget(QtCore.Qt.RightDockWidgetArea, dock)
            self.viewMenu.addAction(dock.toggleViewAction())

            dock = QtGui.QDockWidget("Systems", self)
            dock.setAllowedAreas(QtCore.Qt.LeftDockWidgetArea \
                | QtCore.Qt.RightDockWidgetArea)
            self.dockSystemList = QtGui.QListWidget(dock)
            self.dockSystemList.setDragEnabled(True)
            #self.dockSystemList.setAlternatingRowColors(True)
            self.dockSystemList.setIconSize(QtCore.QSize(32, 32))
            self.dockSystemList.setAlternatingRowColors(True)
            dock.setWidget(self.dockSystemList)
            self.addDockWidget(QtCore.Qt.RightDockWidgetArea, dock)
            self.viewMenu.addAction(dock.toggleViewAction())

        def createDockResource(self):
            dock = QtGui.QDockWidget("Resource", self)

            dock.setTitleBarWidget(QtGui.QWidget())
            dock.setAllowedAreas(QtCore.Qt.LeftDockWidgetArea \
                | QtCore.Qt.RightDockWidgetArea)
            widget = QtGui.QWidget(dock)

            #self.amountLabel = QtGui.QLabel('Amount')
            #self.amountLabel2 = QtGui.QLabel('bla')
            #self.checkbox1 = QtGui.QCheckBox("Checkbox1")
            #self.checkbox2 = QtGui.QCheckBox("Checkbox2")
            #self.listTest = QtGui.QListWidget()

            self.treeWidget = QtGui.QTreeWidget(widget)
            self.treeWidget.setColumnCount( 1 )
            self.treeWidget.setHeaderLabels( ('objects', ) )
            self.treeWidget.itemDoubleClicked.connect(self.doOpenObject)
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
            self.btEdit.clicked.connect(self.doOpenObject)
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

        def dockNetworkListChanged(self, name):
            if not name: return None

        def doShowObject(self, *args, **kwargs):
            print self.treeWidget.currentItem()
            print 'hi'
            self.open()

            #network = nemoa.network.open(name)
            #network.show()

        def doOpenObject(self, *args, **kwargs):

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

        def readSettings(self):
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

            if nemoa.get('workspace'):
                shownName = nemoa.get('workspace')
            else:
                shownName = 'untitled'

            self.setWindowTitle("%s[*] - Nemoa" % shownName)

        def menuAbout(self):
            amail = nemoa.about('email')
            aversion = nemoa.about('version')
            acopyright = nemoa.about('copyright')
            adesc = nemoa.about('description').replace('\n', '<br>')
            acredits = '</i>, <i>'.join(nemoa.about('credits'))
            alicense = nemoa.about('license')

            text = (
                "<h1>nemoa</h1>"
                "<b>version</b> %s<br>"
                "<i>%s</i>"
                "<h3>Copyright</h3>"
                "%s <a href = 'mailto:%s'>&lt;%s&gt;</a>"
                "<h3>License</h3>"
                "This software may be used under the terms of the "
                "%s as published by the "
                "<a href='https://gnu.org/licenses/gpl.html'>"
                "Free Software Foundation</a>."
                "<h3>Credits</h3>"
                "<i>%s</i>" % (aversion, adesc, acopyright, amail,
                amail, alicense, acredits))

            QtGui.QMessageBox.about(self, "About Nemoa", text)

        def updateChangeWorkspace(self):

            self.updateDockWindows()
            self.updateWindowTitle()

        def updateDockWindows(self):

            self.updateDockResource()

            self.dockDatasetList.clear()
            self.dockDatasetList.addItems(nemoa.list('datasets'))
            self.dockNetworkList.clear()
            self.dockNetworkList.addItems(nemoa.list('networks'))
            self.dockSystemList.clear()
            self.dockSystemList.addItems(nemoa.list('systems'))

        def updateDockResource(self):

            self.treeWidget.clear()
            self.treeWidget.setDragEnabled(True)
            objTypes = ['model', 'dataset', 'network', 'system', 'script']
            for objType in objTypes:
                objList = nemoa.list(objType + 's')
                objTypeItem = QtGui.QTreeWidgetItem(self.treeWidget,
                    [objType.title(), None, None])
                objTypeItem.setIcon(0,
                    QtGui.QIcon(":/images/nemoa_logo.png"))
                if not objList:
                    objTypeItem.setDisabled(True)
                    continue
                for objName in objList:
                    objItem = QtGui.QTreeWidgetItem(objTypeItem,
                        [objName, objName, objType])

        def menuCloseFile(self):
            nemoa.close()
            self.updateChangeWorkspace()

        def menuOpenFile(self):
            path = nemoa.path('basepath', 'user')
            options = QtGui.QFileDialog.DontResolveSymlinks \
                | QtGui.QFileDialog.ShowDirsOnly
            directory = QtGui.QFileDialog.getExistingDirectory(self,
                "test", path, options)
            if not directory: return False
            name = nemoa.common.ospath.basename(directory)
            if not nemoa.open(name): return False
            self.updateChangeWorkspace()

        def open(self):
            fileName, filtr = QtGui.QFileDialog.getOpenFileName(self)
            if fileName:
                existing = self.findMdiChild(fileName)
                if existing:
                    self.mdiArea.setActiveSubWindow(existing)
                    return

                child = self.createMdiChild()
                if child.loadFile(fileName):
                    self.statusBar().showMessage("File loaded", 2000)
                    child.show()
                else:
                    child.close()

        def findMdiChild(self, fileName):
            canonicalFilePath = QtCore.QFileInfo(fileName).canonicalFilePath()

            for window in self.mdiArea.subWindowList():
                if window.widget().currentFile() == canonicalFilePath:
                    return window
            return None

        def menuPrintFile(self):
            pass

        def menuNewFile(self):
            pass

        def menuSaveFile(self):
            pass

    nemoa.set('mode', 'silent')
    app = QtGui.QApplication(sys.argv)
    Window = MainWindow()
    Window.show()

    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
