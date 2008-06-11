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
from kiwi.ui.delegates import GladeSlaveDelegate, GladeDelegate
from kiwi.ui.objectlist import ObjectList, Column, ColoredColumn
from kiwi.ui.widgets.entry import ProxyEntry
from kiwi.datatypes import ValidationError
from kiwi.ui.dateentry import DateEntry
from kiwi.ui import dialogs
from kiwi.utils import gsignal

class DateTimeEditUI(GladeSlaveDelegate):

	def __init__(self, dt = None):
		if not dt:
			self.dt = datetime.datetime.now()
		else:
			self.dt = dt
			
		# Set up the user interface
		GladeSlaveDelegate.__init__(self, gladefile="mo_datetime_edit", toplevel_name="window_main")

		self.entry_date = DateEntry()
		self.entry_time = ProxyEntry(data_type=datetime.time)
		self.set_datetime(self.dt)
		self.entry_date.connect('changed', self.entry_date__changed)
		self.entry_time.connect('changed', self.entry_time__changed)
		self.hbox.pack_start(self.entry_date, expand=False, fill=False)
		self.hbox.pack_start(self.entry_time, expand=False, fill=False)

		self.show()

	def entry_date__changed(self, *args):
		dt = self.entry_date.get_date()
		if dt != None:
			self.dt = self.dt.replace(dt.year, dt.month, dt.day)

	def entry_time__changed(self, *args):
		dt = None
		try:
			dt = self.entry_time.read()
		except ValidationError, e:
			# Ignore invalid times because the user might still be filling it
			# out.
			pass

		if dt != None:
			self.dt = self.dt.replace(self.dt.year, self.dt.month, self.dt.day, dt.hour, dt.minute)

	def set_datetime(self, dt):
		self.dt = dt
		self.entry_date.set_date(self.dt)
		self.entry_time.update(self.dt)

	def set_sensitive(self, state):
		self.hbox.set_sensitive(state)
