# -*- coding: utf-8 -*-

__author__  = 'Patrick Michl'
__email__   = 'patrick.michl@gmail.com'
__license__ = 'GPLv3'

import nemoa
import qdeep.objects.common

class Editor(qdeep.objects.common.Editor):

    objType = 'script'
    objName = None

    def createActions(self): pass
    def createMenus(self): pass

    def getName(self):
        return self.objName
