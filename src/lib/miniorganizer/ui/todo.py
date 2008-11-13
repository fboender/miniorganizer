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

class TodoUI(GladeSlaveDelegate):
	
	def __init__(self, parent, mo):
		self.parent = parent
		self.mo = mo
		self.factory = Factory()

		GladeSlaveDelegate.__init__(self, gladefile="mo_tab_todo", toplevel_name="window_main")

		# Set up the user interface
		todoColumns = [
			Column("done", title='Done', data_type=bool, editable=True),
			Column("summaryformat", title='Summary', use_markup=True),
			Column('priority', title='Priority', sorted=True, order=gtk.SORT_DESCENDING),
			ColoredColumn('due', title='Due', data_type=datetime.datetime, color='red', data_func=self.color_due),
			Column('created', title='Created', data_type=datetime.datetime)
		]
		self.treeview_todo = ObjectTree(todoColumns)
		self.vbox_todolist.add(self.treeview_todo)

		# Connect signals
		self.treeview_todo.connect('row-activated', self.treeview_todo__row_activated)
		self.treeview_todo.connect('selection-changed', self.treeview_todo__selection_changed)
		self.treeview_todo.connect('key-press-event', self.treeview_todo__key_press_event)

		self.refresh()

	def refresh(self):
		"""
		Refresh the entire todo tab. This clears everything and rebuilds it.
		Call this when todos are removed outside of this class.
		"""
		self.treeview_todo.clear()

		# Fill the user interface with information
		for todo in self.mo.cal_model.get_todos():
			parent = self.mo.cal_model.get_model_by_uid(todo.get_related_to())
			self.treeview_todo.append(parent, todo)
	
	def color_due(self, value):
		if not value:
			return(False)
		return(value < datetime.datetime.now())

	def on_toolbutton_add__clicked(self, *args):
		todo = self.factory.todo()
		todo = miniorganizer.ui.TodoEditUI(self.mo, todo).run()
		if todo:
			self.mo.cal_model.add(todo)
			self.treeview_todo.append(None, todo)
			self.parent.menuitem_save.set_sensitive(True)

	def on_toolbutton_edit__clicked(self, *args):
		sel_todo = self.treeview_todo.get_selected()
		self.treeview_todo__row_activated(self.treeview_todo, sel_todo)

	def on_toolbutton_remove__clicked(self, *args):
		sel_todo = self.treeview_todo.get_selected()
		if sel_todo:
			children = self.mo.cal_model.get_models_related_by_uid(sel_todo.get_uid())

			if children:
				response = dialogs.warning('This Todo contains sub-todos. Removing it will also remove the sub-todos. Is this what you want?', buttons=gtk.BUTTONS_YES_NO)
				if response != gtk.RESPONSE_YES:
					return

			self.treeview_todo.remove(sel_todo, True)
			self.mo.cal_model.delete(sel_todo, True)
			self.parent.menuitem_save.set_sensitive(True)

	def on_toolbutton_addsub__clicked(self, *args):
		parent_todo = self.treeview_todo.get_selected()
		todo = self.factory.todo(parent_todo)
		if miniorganizer.ui.TodoEditUI(self.mo, todo).run():
			self.mo.cal_model.add(todo)
			self.treeview_todo.append(parent_todo, todo)
			self.treeview_todo.expand(parent_todo)
			self.parent.menuitem_save.set_sensitive(True)
		
	def treeview_todo__selection_changed(self, list, selection):
		has_selection = selection is not None
		self.toolbutton_addsub.set_sensitive(has_selection)
		self.toolbutton_remove.set_sensitive(has_selection)
		self.toolbutton_edit.set_sensitive(has_selection)
	
	def treeview_todo__row_activated(self, list, object):
		todo = miniorganizer.ui.TodoEditUI(self.mo, object).run()
		self.parent.menuitem_save.set_sensitive(True)
	
	def treeview_todo__key_press_event(self, treeview, event):
		if event.keyval == gtk.keysyms.Delete:
			self.on_toolbutton_remove__clicked()
