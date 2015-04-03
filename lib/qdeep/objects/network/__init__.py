# -*- coding: utf-8 -*-

__author__  = 'Patrick Michl'
__email__   = 'patrick.michl@gmail.com'
__license__ = 'GPLv3'

import nemoa
import qdeep.objects.common
from PySide import QtGui, QtCore

class Editor(qdeep.objects.common.Editor):
    objType = 'network'

    def createActions(self):
        self.actPlotNetwork = QtGui.QAction(
            qdeep.common.getIcon('actions', 'view-preview.png'),
            "Plot network", self,
            shortcut = "F5",
            statusTip = "Plot network",
            triggered = self.plotNetwork)

    def plotNetwork(self):
        if self.objInstance:
            self.objInstance.show()

    def createToolBars(self):
        self.tbar = self.addToolBar("Network")
        self.tbar.addAction(self.actPlotNetwork)
