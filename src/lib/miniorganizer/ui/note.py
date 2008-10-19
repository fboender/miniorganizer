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
from kiwi.ui.objectlist import ObjectTree, Column, ColoredColumn
from kiwi.ui import dialogs
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
		#self.treeview_note = ObjectList(noteColumns)
		self.treeview_note = ObjectTree(noteColumns)
		self.vbox_notelist.add(self.treeview_note)

		for journal in self.mo.cal_model.get_journals():
			parent = self.mo.cal_model.get_model_by_uid(journal.get_related_to())
			self.treeview_note.append(parent, journal)

		# Connect signals
		self.treeview_note.connect('row-activated', self.treeview_note__row_activated)
		self.treeview_note.connect('selection-changed', self.treeview_note__selection_changed)
		self.treeview_note.connect('key-press-event', self.treeview_note__key_press_event)

	def on_toolbutton_add__clicked(self, *args):
		journal = self.factory.journal()
		journal = miniorganizer.ui.NoteEditUI(self.mo, journal).run()
		if journal:
			self.mo.cal_model.add(journal)
			self.treeview_note.append(None, journal)
			self.parent.menuitem_save.set_sensitive(True)

	def on_toolbutton_addsub__clicked(self, *args):
		parent_journal = self.treeview_note.get_selected()
		journal = self.factory.journal(parent_journal)
		if miniorganizer.ui.NoteEditUI(self.mo, journal).run():
			self.mo.cal_model.add(journal)
			self.treeview_note.append(parent_journal, journal)
			self.treeview_note.expand(parent_journal)
			self.parent.menuitem_save.set_sensitive(True)
		
	def on_toolbutton_edit__clicked(self, *args):
		sel_note = self.treeview_note.get_selected()
		self.treeview_note__row_activated(self.treeview_note, sel_note)

	def on_toolbutton_remove__clicked(self, *args):
		sel_note = self.treeview_note.get_selected()
		if sel_note:
			children = self.mo.cal_model.get_models_related_by_uid(sel_note.get_uid())

			if children:
				response = dialogs.warning('This note contains sub-notes. Removing it will also remove the sub-notes. Is this what you want?', buttons=gtk.BUTTONS_YES_NO)
				if response != gtk.RESPONSE_YES:
					return

			self.mo.cal_model.delete(sel_note, True)
			self.treeview_note.remove(sel_note, True)
			self.parent.menuitem_save.set_sensitive(True)

	def treeview_note__selection_changed(self, list, selection):
		has_selection = selection is not None
		self.toolbutton_addsub.set_sensitive(has_selection)
		self.toolbutton_remove.set_sensitive(has_selection)
		self.toolbutton_edit.set_sensitive(has_selection)
	
	def treeview_note__row_activated(self, list, object):
		sel_note = self.treeview_note.get_selected()
		note = miniorganizer.ui.NoteEditUI(self.mo, sel_note).run()

	def treeview_note__key_press_event(self, treeview, event):
		if event.keyval == gtk.keysyms.Delete:
			self.on_toolbutton_remove__clicked()
