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

import datetime
import gtk
import miniorganizer.models
import miniorganizer.ui
from kiwi.ui.delegates import GladeDelegate
from kiwi.ui import dialogs

class NoteEditUI(GladeDelegate):

	def __init__(self, mo, journal):
		self.mo = mo
		self.journal = journal

		GladeDelegate.__init__(self, gladefile="mo_note_edit", toplevel_name='dialog_main')

		# Set up the user interface
		self.entry_title.set_text(self.journal.get_summary())
		self.textview_description.get_buffer().set_text(self.journal.get_description())

	def run(self):
		self.show_all()
		gtk.main()
		return(self.journal)

	def on_button_ok__clicked(self, *agrs):
		c_buffer = self.textview_description.get_buffer()
		c_startpos = c_buffer.get_iter_at_offset(0)
		c_endpos = c_buffer.get_iter_at_offset(-1)
		description= c_buffer.get_text(c_startpos, c_endpos)

		self.journal.set_summary(self.entry_title.get_text())
		self.journal.set_description(description)
		
		self.quit()

	def on_button_cancel__clicked(self, *args):
		self.note = None
		self.quit()

	def on_dialog_main__delete_event(self, *args):
		self.note = None
		self.quit()

	def quit(self):
		self.view.hide()
		gtk.main_quit()

