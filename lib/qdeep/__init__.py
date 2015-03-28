# -*- coding: utf-8 -*-
"""nemoa gui."""

__version__     = '0.1.2'
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
import qdeep.scripts

def start(*args, **kwargs):
    """Start nemoa gui."""
    return qdeep.scripts.main()
