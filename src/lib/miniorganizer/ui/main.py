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

class MiniOrganizerUI(GladeDelegate):

	widgets = []

	def __init__(self, mo):
		self.mo = mo

		GladeDelegate.__init__(self, gladefile="mo", toplevel_name='window_main')
		self.window_main.set_size_request(400, 500)

		self.tab_todos = miniorganizer.ui.TodoUI(self, self.mo)
		self.attach_slave("eventbox_todos", self.tab_todos)

		self.tab_events = miniorganizer.ui.EventUI(self, self.mo)
		self.attach_slave("eventbox_events", self.tab_events)

		self.tab_notes = miniorganizer.ui.NotesUI(self, self.mo)
		self.attach_slave("eventbox_notes", self.tab_notes)

		self.show_all()

		if mo.first_time:
			dialogs.warning('This version of MiniOrganizer is still in development. Even though it works, and can be used in everyday life, there may still be bugs in it.\n\nIf you notice such a bug, or see anything else you would like to see changed or added, please contact the author. Your feedback is greatly appreciated.');

		gtk.main()

	def on_window_main__delete_event(self, *args):
		self.quit()
		
	def on_menu_quit__activate(self, *args):
		self.quit()

	def on_menu_about__activate(self, *args):
		miniorganizer.ui.AboutUI()

	def on_menuitem_import__activate(self, *args):
		filename = dialogs.open('Select file to import', patterns=['*.ics'])
		if filename:
			self.mo.import_(filename)

	def quit(self):
		self.view.hide()
		gtk.main_quit()

