#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""QT based graphical user interface for nemoa."""

__version__     = '0.1.3'
__status__      = 'Development'
__description__ = 'Deep data analysis and visualization'
__url__         = 'https://github.com/fishroot/nemoa-gui'
__license__     = 'GPLv3'
__copyright__   = 'Copyright 2015, Patrick Michl'
__author__      = 'Patrick Michl'
__email__       = 'patrick.michl@gmail.com'
__maintainer__  = 'Patrick Michl'
__credits__     = ['Rebecca Krauss', 'Sebastian Michl']

import qdeep.common
import nemoa
from PySide import QtGui, QtCore
import sys
import pyqtgraph.console

class MainWindow(QtGui.QMainWindow):

    settings = None

    def __init__(self):
        super(MainWindow, self).__init__()

        self.readSettings()

        # setup MDI area
        self.mdiArea = QtGui.QMdiArea()
        self.mdiArea.setViewMode(QtGui.QMdiArea.TabbedView)
        self.mdiArea.setTabsClosable(True)
        self.mdiArea.setTabsMovable(True)
        #self.mdiArea.setObjectName("mdiArea")
        self.mdiArea.setAcceptDrops(True)
        self.setCentralWidget(self.mdiArea)

        self.createActions()
        self.createMenus()
        self.createToolBars()
        self.createStatusBar()
        self.createDocks()

        self.setUnifiedTitleAndToolBarOnMac(True)

        self.applySettings()

    def aboutNemoa(self):
        aboutBox = QtGui.QMessageBox.about(self,
            "About Nemoa", self.getAboutNemoa())

    def getAboutNemoa(self):

        amail = nemoa.about('email')
        aversion = nemoa.about('version')
        acopyright = nemoa.about('copyright')
        adesc = nemoa.about('description').replace('\n', '<br>')
        acredits = '</i>, <i>'.join(nemoa.about('credits'))
        alicense = nemoa.about('license')

        return (
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
            "<i>%s</i>" % (
            aversion, adesc, acopyright, amail,
            amail, alicense, acredits))

    def aboutQDeep(self):
        aboutBox = QtGui.QMessageBox.about(
            self, "About QDeep", self.getAboutQDeep())

    def getAboutQDeep(self):

        amail = __email__
        aversion = __version__
        acopyright = __copyright__
        adesc = __doc__
        acredits = ', '.join(__credits__)
        alicense = __license__

        return (
            "<h1>QDeep</h1>"
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
            "<i>%s</i>"
            "<h3>Third Party Credits</h3>"
            "<a href='https://www.archlinux.org/packages/extra/any/"
            "oxygen-icons/'>Oxygen icon set</a> license: LGPL" % (
            aversion, adesc, acopyright, amail,
            amail, alicense, acredits))

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

        # project
        self.actNewProject = QtGui.QAction(
            qdeep.common.getIcon('actions', 'window-new.png'),
            "New Project", self,
            statusTip = "Create a new project",
            triggered = self.newWorkspace)
        self.actOpenProject = QtGui.QAction(
            qdeep.common.getIcon('actions', 'project-open.png'),
            'Open Poject', self,
            statusTip = "Open an existing project",
            triggered = self.openWorkspace)
        self.actSaveProject = QtGui.QAction(
            qdeep.common.getIcon('actions', 'document-save-all.png'),
            'Save Project', self,
            statusTip = "Save all files of current project to disk",
            triggered = self.saveProject)
        self.actCloseProject = QtGui.QAction(
            qdeep.common.getIcon('actions', 'project-development-close.png'),
            "Close Project", self,
            statusTip = "Close current project",
            triggered = self.closeWorkspace)

        # files
        self.actNewFile= QtGui.QAction(
            qdeep.common.getIcon('actions', 'document-new.png'),
            "&New", self,
            shortcut = "Ctrl+N",
            statusTip = "Create a new file",
            triggered = self.newFile)
        self.actOpenFile = QtGui.QAction(
            qdeep.common.getIcon('actions', 'document-open.png'),
            '&Open', self,
            shortcut = "Ctrl+O",
            statusTip = "Open an existing file",
            triggered = self.openFile)
        self.actSaveFile = QtGui.QAction(
            qdeep.common.getIcon('actions', 'document-save.png'),
            '&Save', self,
            shortcut = "Ctrl+S",
            statusTip = "Save current file to disk",
            triggered = self.save)
        self.actSaveAsFile = QtGui.QAction(
            qdeep.common.getIcon('actions', 'document-save-as.png'),
            'Save as...', self,
            statusTip = "Save current file to disk",
            triggered = self.saveAs)
        self.actPrintFile = QtGui.QAction(
            qdeep.common.getIcon('actions', 'document-print.png'),
            "&Print", self,
            shortcut = QtGui.QKeySequence.Print,
            statusTip = "Print the document",
            triggered = self.printFile)
        self.actExit = QtGui.QAction(
            qdeep.common.getIcon('actions', 'window-close.png'),
            "Exit", self,
            shortcut = "Ctrl+Q",
            statusTip = "Exit the application",
            triggered = self.close)
        self.actAboutNemoa = QtGui.QAction(
            qdeep.common.getIcon('actions', 'help-about.png'),
            "About Nemoa", self,
            statusTip = "About Nemoa",
            triggered = self.aboutNemoa)
        self.actAboutQDeep = QtGui.QAction(
            qdeep.common.getIcon('actions', 'help-about.png'),
            "About QDeep", self,
            statusTip = "About QDeep",
            triggered = self.aboutQDeep)

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
        self.treeWidget.itemDoubleClicked.connect(
            self.openObjectFromObjectsDock)
        self.treeWidget.setIconSize(QtCore.QSize(22, 22))
        self.btEdit = QtGui.QPushButton("Edit")
        self.btEdit.clicked.connect(self.openObjectFromObjectsDock)
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
        self.mbarView.addAction(dock.toggleViewAction())
        self.dockObjects = dock

    def createDockTools(self):

        dock = QtGui.QDockWidget("Tools", self)
        dock.setAllowedAreas(QtCore.Qt.LeftDockWidgetArea \
            | QtCore.Qt.RightDockWidgetArea)

        #self.dockTools = pyqtgraph.console.ConsoleWidget(dock)
        widget = QtGui.QListWidget(dock)
        widget.setDragEnabled(True)
        widget.setAlternatingRowColors(True)
        dock.setWidget(widget)
        self.addDockWidget(QtCore.Qt.RightDockWidgetArea, dock)
        self.mbarView.addAction(dock.toggleViewAction())
        self.dockTools = dock

    def createMenus(self):

        self.mbarFile = self.menuBar().addMenu("&File")
        self.mbarFilePrj = self.mbarFile.addMenu("&Projects")
        self.mbarFilePrj.addAction(self.actNewProject)
        self.mbarFilePrj.addAction(self.actOpenProject)
        self.mbarFilePrj.addAction(self.actSaveProject)
        self.mbarFilePrj.addAction(self.actCloseProject)
        self.mbarFile.addSeparator()
        self.mbarFile.addAction(self.actNewFile)
        self.mbarFile.addAction(self.actOpenFile)
        self.mbarFile.addAction(self.actSaveFile)
        self.mbarFile.addAction(self.actSaveAsFile)
        self.mbarFile.addSeparator()
        self.mbarFile.addAction(self.actPrintFile)
        self.mbarFile.addSeparator()
        self.mbarFile.addAction(self.actExit)

        if len(self.mdiArea.subWindowList()):
            self.objectMenu = self.menuBar().addMenu("&Object")

        self.mbarView = self.menuBar().addMenu("&View")
        self.mbarViewTbar = self.mbarView.addMenu("&Toolbars")

        self.mbarAbout = self.menuBar().addMenu("&Help")
        self.mbarAbout.addAction(self.actAboutQDeep)
        self.mbarAbout.addAction(self.actAboutNemoa)

    def createStatusBar(self):
        self.statusBar().showMessage("Ready")

    def createToolBars(self):

        self.tbarPrj = self.addToolBar("Project")
        self.tbarPrj.addAction(self.actNewProject)
        self.tbarPrj.addAction(self.actOpenProject)
        self.tbarPrj.addAction(self.actSaveProject)
        self.tbarPrj.addAction(self.actCloseProject)
        self.mbarViewTbar.addAction(
            self.tbarPrj.toggleViewAction())

        #self.editToolBar = self.addToolBar("Edit")
        #self.editToolBar.addAction(self.cutAct)
        #self.editToolBar.addAction(self.copyAct)
        #self.editToolBar.addAction(self.pasteAct)

    def documentWasModified(self):
        modified = True
        self.setWindowModified(modified)

    def maybeSave(self):
        modified = True

        if modified:
            ret = QtGui.QMessageBox.warning(self, "QDeep",
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

        # read settings from system
        QtCore.QCoreApplication.setOrganizationName("Froot")
        QtCore.QCoreApplication.setApplicationName("QDeep")

        qsettings = QtCore.QSettings()
        self.settings = {}

        # section 'mainwindow'
        self.settings['mainwindow'] = {}
        qsettings.beginGroup('mainwindow')
        self.settings['mainwindow']['pos'] = \
            qsettings.value("pos", QtCore.QPoint(200, 200))
        self.settings['mainwindow']['size'] = \
            qsettings.value("size", QtCore.QSize(400, 400))
        qsettings.endGroup()

        # section 'mdiarea'
        self.settings['mdiarea'] = {}
        qsettings.beginGroup('mdiarea')
        self.settings['mdiarea']['child'] = []
        size = qsettings.beginReadArray("child")
        for i in range(size):
            qsettings.setArrayIndex(i)
            childType = qsettings.value("type", None)
            childName = qsettings.value("name", None)
            self.settings['mdiarea']['child'].append(
                (childType, childName))
        qsettings.endArray()
        qsettings.beginGroup('active')
        childType = qsettings.value("type", None)
        childName = qsettings.value("name", None)
        self.settings['mdiarea']['active'] = (childType, childName)
        qsettings.endGroup()
        qsettings.endGroup()

        # section 'tbarprj'
        self.settings['tbarprj'] = {}
        qsettings.beginGroup('tbarprj')
        self.settings['tbarprj']['visible'] = \
            qsettings.value("visible", False) in ['true', 'True', True]
        qsettings.endGroup()

        # section 'dockobjects'
        self.settings['dockobjects'] = {}
        qsettings.beginGroup('dockobjects')
        self.settings['dockobjects']['visible'] = \
            qsettings.value("visible", True) in ['true', 'True', True]
        qsettings.endGroup()

        # section 'docktools'
        self.settings['docktools'] = {}
        qsettings.beginGroup('docktools')
        self.settings['docktools']['visible'] = \
            qsettings.value("visible", True) in ['true', 'True', True]
        qsettings.endGroup()

        workspace = qsettings.value("workspace", None) or None
        base = qsettings.value("base", None) or None

        if workspace and base:
            nemoa.open(workspace, base = base)

    def applySettings(self):
        self.updateChangeWorkspace()

        self.resize(self.settings['mainwindow']['size'])
        self.move(self.settings['mainwindow']['pos'])

        if 'child' in self.settings['mdiarea']:
            childList = self.settings['mdiarea']['child']
            for childType, childName in childList:
                self.openObject(childType, childName)
        if 'active' in self.settings['mdiarea']:
            actType, actName = self.settings['mdiarea']['active']
            self.openObject(actType, actName)

        self.tbarPrj.setVisible(
            self.settings['tbarprj']['visible'])
        self.dockObjects.setVisible(
            self.settings['dockobjects']['visible'])
        self.dockTools.setVisible(
            self.settings['docktools']['visible'])

    def writeSettings(self):
        qsettings = QtCore.QSettings()

        qsettings.beginGroup('mdiarea')
        qsettings.beginWriteArray('child')
        windows = self.mdiArea.subWindowList()
        for i, window in enumerate(windows):
            qsettings.setArrayIndex(i)
            child = window.widget()
            qsettings.setValue("name", child.getName())
            qsettings.setValue("type", child.getType())
        qsettings.endArray()
        qsettings.beginGroup('active')
        activeChild = self.mdiArea.activeSubWindow().widget()
        qsettings.setValue("name", activeChild.getName())
        qsettings.setValue("type", activeChild.getType())
        qsettings.endGroup()
        qsettings.endGroup()

        qsettings.beginGroup('mainwindow')
        qsettings.setValue("pos", self.pos())
        qsettings.setValue("size", self.size())
        qsettings.endGroup()

        qsettings.beginGroup('tbarprj')
        qsettings.setValue("visible", self.tbarPrj.isVisible())
        qsettings.endGroup()

        qsettings.beginGroup('docktools')
        qsettings.setValue("visible", self.dockTools.isVisible())
        qsettings.endGroup()

        qsettings.beginGroup('dockobjects')
        qsettings.setValue("visible", self.dockObjects.isVisible())
        qsettings.endGroup()

        qsettings.setValue("workspace", nemoa.get('workspace'))
        qsettings.setValue("base", nemoa.get('base'))

    def updateWindowTitle(self):
        #self.textEdit.document().setModified(False)
        self.setWindowModified(False)
        if nemoa.get('workspace'): shownName = nemoa.get('workspace')
        else: shownName = 'untitled'
        self.setWindowTitle("%s[*] - QDeep" % shownName)

    def updateChangeWorkspace(self):
        # 2Do: close all MDI windows
        self.mdiArea.closeAllSubWindows()
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
            objTypeIcon = qdeep.common.getIcon(*objIconPath)
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

    def openObjectFromObjectsDock(self):

        # get name and type of object
        curItem = self.treeWidget.currentItem()
        objTitle = curItem.text(0)
        objName = curItem.text(1)
        objType = curItem.text(2)
        objPath = nemoa.path(objType, objName)

        if objPath: self.openObject(objType, objName, objTitle)

    def openObject(self, objType, objName, objTitle = None):

        # get name and type of object
        objPath = nemoa.path(objType, objName)
        if objPath:
            existing = self.findMdiChild(objType, objName)
            if existing:
                self.mdiArea.setActiveSubWindow(existing)
                return
            child = self.createMdiChild(type = (objType, 'editor'))
            if child.openFromWorkspace(objName):
                self.statusBar().showMessage("File loaded", 2000)
                child.show()
            else:
                child.close()
            return True
        return False

    def saveProject(self):
        return True

    def saveProjectAs(self):
        return True

    #
    # MDI
    #

    def createMdiChild(self, type):

        if type == ('script', 'editor'):
            from qdeep.objects.script import Editor
            child = Editor()
        elif type == ('dataset', 'editor'):
            from qdeep.objects.dataset import Editor
            child = Editor()
        elif type == ('model', 'editor'):
            from qdeep.objects.model import Editor
            child = Editor()
        elif type == ('network', 'editor'):
            from qdeep.objects.network import Editor
            child = Editor()
        elif type == ('system', 'editor'):
            from qdeep.objects.system import Editor
            child = Editor()
        else:
            return None

        child.setAcceptDrops(True)
        self.mdiArea.addSubWindow(child)

        #child.copyAvailable.connect(self.cutAct.setEnabled)
        #child.copyAvailable.connect(self.copyAct.setEnabled)

        return child


    def findMdiChild(self, objType, objName):
        windows = self.mdiArea.subWindowList()
        for window in windows:
            child = window.widget()
            if not child.getType() == objType: continue
            if not child.getName() == objName: continue
            return window
        return None

    def getActiveMdiChild(self):
        activeSubWindow = self.mdiArea.activeSubWindow()
        if activeSubWindow:
            return activeSubWindow.widget()
        return None

    def printFile(self):
        return True

    def newWorkspace(self):
        return True

    def newFile(self):
        return True

    def openFile(self):
        return True

    def save(self):
        if self.getActiveMdiChild() \
            and self.getActiveMdiChild().save():
            self.statusBar().showMessage("File saved", 2000)

    def saveAs(self):
        if self.getActiveMdiChild() \
            and self.mdiArea.activeMdiChild().saveAs():
            self.statusBar().showMessage("File saved", 2000)

    #def saveFile(self):
        #return True

    ##def save(self):
        ##return self.saveWorkspace()

def main():
    nemoa.set('mode', 'silent')
    app = QtGui.QApplication(sys.argv)
    Window = MainWindow()
    Window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()

