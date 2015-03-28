# -*- coding: utf-8 -*-

__author__  = 'Patrick Michl'
__email__   = 'patrick.michl@gmail.com'
__license__ = 'GPLv3'

CACHE = None

def getPath(key, *args):

    import nemoa
    import os

    global CACHE

    if not CACHE: CACHE = {}

    if key == 'icons':
        if not CACHE.get('icons', None):
            CACHE['icons'] = nemoa.path('expand',
                ('%site_data_dir%', 'images', 'icons'))
        base = CACHE['icons']
    elif key == 'logo':
        if not CACHE.get('logo', None):
            CACHE['logo'] = nemoa.path('expand',
                ('%site_data_dir%', 'images', 'logo'))
        base = CACHE['logo']

    return os.path.sep.join([base] + list(args))

def getIcon(*args):

    from PySide import QtGui
    return QtGui.QIcon(getPath('icons', *args))

def getLogo(*args):

    from PySide import QtGui
    return QtGui.QIcon(getPath('logo', *args))
