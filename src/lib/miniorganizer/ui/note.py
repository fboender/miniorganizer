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
import miniorganizer.ui
from kiwi.ui.delegates import GladeSlaveDelegate
from kiwi.ui.objectlist import ObjectList, Column, ColoredColumn
from miniorganizer.models import Factory

class NoteUI(GladeSlaveDelegate):

	def __init__(self, parent, mo):
		self.parent = parent
		self.mo = mo
		self.factory = Factory()

		# Set up the user interface
		GladeSlaveDelegate.__init__(self, gladefile="mo_tab_notes", toplevel_name="window_main")
	
		noteColumns = [
			Column("summary", title='Title', data_type=str),
		]
		self.treeview_note = ObjectList(noteColumns)
		self.vbox_notelist.add(self.treeview_note)

		for journal in self.mo.cal_model.get_journals():
			self.treeview_note.append(journal)

		# Connect signals
		self.treeview_note.connect('row-activated', self.treeview_note__row_activated)
		self.treeview_note.connect('key-press-event', self.treeview_note__key_press_event)

	def on_toolbutton_add__clicked(self, *args):
		journal = self.factory.journal()
		journal = miniorganizer.ui.NoteEditUI(self.mo, journal).run()
		if journal:
			self.mo.cal_model.add(journal)
			self.treeview_note.append(journal)
			self.parent.menuitem_save.set_sensitive(True)

	def on_toolbutton_remove__clicked(self, *args):
		sel_note = self.treeview_note.get_selected()

		if sel_note:
			self.mo.cal_model.delete(sel_note)
			self.treeview_note.remove(sel_note)

	def treeview_note__row_activated(self, list, object):
		sel_note = self.treeview_note.get_selected()
		note = miniorganizer.ui.NoteEditUI(self.mo, sel_note).run()

	def treeview_note__key_press_event(self, treeview, event):
		if event.keyval == gtk.keysyms.Delete:
			self.on_toolbutton_remove__clicked()
