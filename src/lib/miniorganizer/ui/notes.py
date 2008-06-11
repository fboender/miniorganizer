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
from kiwi.ui.delegates import GladeSlaveDelegate
from kiwi.ui.objectlist import ObjectList, Column, ColoredColumn

class NotesUI(GladeSlaveDelegate):

	def __init__(self, parent, mo):
		self.parent = parent
		self.mo = mo 

		# Set up the user interface
		GladeSlaveDelegate.__init__(self, gladefile="mo_tab_notes", toplevel_name="window_main")

		noteColumns = [
			Column("name", title='Name', data_type=str),
		]
		self.treeview_notes = ObjectList(noteColumns)
		self.vbox_notelist.add(self.treeview_notes)

	def on_toolbutton_add__clicked(self, *args):
		raise NotImplementedError("Not implemented")
