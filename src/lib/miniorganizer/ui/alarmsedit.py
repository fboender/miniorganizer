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
import miniorganizer.models
from kiwi.ui.objectlist import Column
from kiwi.ui.listdialog import ListContainer

class AlarmsEditUI(ListContainer):
	def __init__(self, mo, alarms = None, parent_model = None):
		self.mo = mo
		self.alarms = alarms
		self.parent_model = parent_model
		columns = [
			Column("offsetformat", title='Offset'),
			Column("type", title='Type')
		]
		self.listcontainer_alarms = ListContainer(columns)
		self.listcontainer_alarms.add_items(alarms)
		self.listcontainer_alarms.connect('add-item', self.listcontainer__add_item)
		self.listcontainer_alarms.connect('remove-item', self.listcontainer__remove_item)
		self.listcontainer_alarms.connect('edit-item', self.listcontainer__edit_item)

	def listcontainer__add_item(self, *args):
		delta = datetime.timedelta()
		alarm = self.mo.factory.alarm(delta, self.parent_model)
		alarm = miniorganizer.ui.AlarmEditUI(self.mo, alarm).run()
		self.alarms.append(alarm)
		self.listcontainer_alarms.add_item(alarm)

	def listcontainer__remove_item(self, listcontainer, alarm):
		self.alarms.remove(alarm)
		self.listcontainer_alarms.remove_item(alarm)

	def listcontainer__edit_item(self, listcontainer, alarm):
		x = miniorganizer.ui.AlarmEditUI(self.mo, alarm)
		alarm = x.run()
		if alarm:
			self.listcontainer_alarms.update_item(alarm)

	def set_sensitive(self, state):
		self.listcontainer_alarms.set_sensitive(state)
