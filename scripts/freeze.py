#!/usr/bin/python

# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

# Copyright 2014 Florian Bruhin (The Compiler) <mail@qutebrowser.org>
#
# This file is part of qutebrowser.
#
# qutebrowser is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# qutebrowser is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with qutebrowser.  If not, see <http://www.gnu.org/licenses/>.

"""cx_Freeze script for qutebrowser.

Builds a standalone executable.
"""


import os
import os.path
import sys
import platform

from cx_Freeze import setup, Executable

sys.path.insert(0, os.getcwd())
from scripts.setupcommon import setupdata, write_git_file


try:
    BASEDIR = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                           os.path.pardir)
except NameError:
    BASEDIR = None


def get_egl_path():
    """Get the path for PyQt5's libEGL.dll."""
    if not sys.platform.startswith('win'):
        return None
    bits = platform.architecture()[0]
    if bits == '32bit':
        return r'C:\Python33_x32\Lib\site-packages\PyQt5\libEGL.dll'
    elif bits == '64bit':
        return r'C:\Python33\Lib\site-packages\PyQt5\libEGL.dll'
    else:
        raise ValueError("Unknown architecture")

build_exe_options = {
    'include_files': [
        ('qutebrowser/html', 'html'),
        ('qutebrowser/git-commit-id', 'git-commit-id'),
    ],
    'include_msvcr': True,
}

egl_path = get_egl_path()
if egl_path is not None:
    build_exe_options['include_files'].append((egl_path, 'libEGL.dll'))

bdist_msi_options = {
    # random GUID generated by uuid.uuid4()
    'upgrade_code': '{a7119e75-4eb7-466c-ae0d-3c0eccb45196}',
    'add_to_path': False,
}

base = 'Win32GUI' if sys.platform.startswith('win') else None

executable = Executable('qutebrowser/__main__.py', base=base,
                        targetName='qutebrowser.exe',
                        shortcutName='qutebrowser',
                        shortcutDir='ProgramMenuFolder')

try:
    write_git_file()
    setup(
        executables=[executable],
        options={
            'build_exe': build_exe_options,
            'bdist_msi': bdist_msi_options,
        },
        **setupdata
    )
finally:
    if BASEDIR is not None:
        path = os.path.join(BASEDIR, 'qutebrowser', 'git-commit-id')
        if os.path.exists(path):
            os.remove(path)
