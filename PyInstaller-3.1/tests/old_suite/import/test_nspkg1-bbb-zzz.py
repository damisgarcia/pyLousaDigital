#-----------------------------------------------------------------------------
# Copyright (c) 2013-2016, PyInstaller Development Team.
#
# Distributed under the terms of the GNU General Public License with exception
# for distributing bootloader.
#
# The full license is in the file COPYING.txt, distributed with this software.
#-----------------------------------------------------------------------------

# Test inclusion of a namespace packages in an zipped egg

import sys
if not getattr(sys, 'frozen', None):
    import os
    sys.path.append(os.path.join(
        os.path.dirname(__file__), 'nspkg1-pkg', 'nspkg1_bbb.egg'))

import nspkg1.bbb.zzz
