#!/usr/bin/env python
# 
# Copyright (C) 2008 Ferry Boender 
#
# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation, either version 3 of the License, or (at your option) any later
# version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License along with
# this program. If not, see <http://www.gnu.org/licenses/>.

from kiwi.ui.delegates import GladeDelegate

class AboutUI(GladeDelegate):
	def __init__(self):
		x = GladeDelegate.__init__(self, gladefile="mo_about", toplevel_name='dialog_main')
		self.toplevel.connect('response', self.on_close)
		self.show_all()

	def on_close(self, dialog, response):
		dialog.destroy()
