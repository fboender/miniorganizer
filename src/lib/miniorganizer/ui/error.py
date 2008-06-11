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

import gtk
import miniorganizer.ui
from kiwi.ui.delegates import GladeDelegate
from kiwi.ui import dialogs

class ErrorUI(GladeDelegate):

	def __init__(self, mo, text):
		self.mo = mo

		GladeDelegate.__init__(self, gladefile="mo_error_display", toplevel_name='dialog_main')

		c_buffer = self.textview_details.get_buffer()
		c_inspos = c_buffer.get_insert()
		c_insiter = c_buffer.get_iter_at_mark(c_inspos)
		self.textview_details.get_buffer().insert(c_insiter, text)

	def run(self):
		self.show_all()
		gtk.main()

	def on_dialog_main__delete_event(self, *args):
		self.quit()
		
	def on_button_ok__clicked(self, *args):
		self.quit()

	def quit(self):
		self.view.hide()
		gtk.main_quit()

