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
import icalendar
import miniorganizer
from kiwi.model import Model

class TodoModel(Model):

	def __init__(self, mo, vtodo):
		assert(type(vtodo) == icalendar.cal.Todo)

		self.mo = mo
		self.__vtodo = vtodo
		self.__alarms = []
		for valarm in self.__vtodo.walk('VALARM'):
			self.__alarms.append(self.mo.factory.alarmFromVComponent(valarm, self))

	def get_summary(self):
		return(self.__vtodo.get('SUMMARY', ''))

	def set_summary(self, summary):
		self.__vtodo.set('SUMMARY', summary)

	def get_summaryformat(self):
		if self.get_done():
			fmt = '<s>%s</s>'
		else:
			fmt = '%s'
		return(fmt % (self.__vtodo.get('SUMMARY', '')))

	def get_priority(self):
		return(self.__vtodo.get('PRIORITY', '0'))

	def set_priority(self, priority):
		self.__vtodo.set('PRIORITY', priority)

	def get_description(self):
		return(self.__vtodo.get('DESCRIPTION', '').replace('\\n', '\n'))

	def set_description(self, description):
		self.__vtodo.set('DESCRIPTION', description.replace('\n', '\\n'))

	def get_done(self):
		if self.__vtodo.get('PERCENT-COMPLETE', 0) == 100:
			return(True)
		else:
			return(False)

	def set_done(self, done):
		if done:
			self.__vtodo.set('PERCENT-COMPLETE', 100)
		else:
			self.__vtodo.set('PERCENT-COMPLETE', 0)

	def get_created(self):
		created = self.__vtodo.get('CREATED', None)
		if created:
			created = created.dt
		return(created)

	def get_due(self):
		due = self.__vtodo.get('DUE', None)
		if due:
			due = datetime.datetime(*due.dt.timetuple()[:-2])
		return(due)

	def set_due(self, due_dt):
		if due_dt == None:
			self.__vtodo.pop('DUE')
		else:
			self.__vtodo.set('DUE', due_dt)

	def get_start(self):
		return(self.get_due())

	def get_uid(self):
		return(self.__vtodo.get('UID', None))

	def get_parent(self):
		parent = None
		parent_uid = self.__vtodo.get('RELATED-TO', None)
		if parent_uid:
			parent = self.mo.getComponentByUID(parent_uid)
		return(parent)

	def get_children(self):
		return(self.mo.getRelatedComponents(self.get_uid()))

	def get_related_to(self):
		return(self.__vtodo.get('RELATED-TO', None))
			
	def get_alarms(self):
		return(self.__alarms)

	def add_alarm(self, alarm):
		self.__vtodo.add_component(alarm.get_valarm())
		self.__alarms.append(alarm)

	def del_alarm(self, alarm):
		self.__vtodo.subcomponents.remove(alarm.get_valarm())
		self.__alarms.remove(alarm)

	def get_vcomponent(self):
		return(self.__vtodo)

	def __setattr__(self, key, value):
		f = getattr(self, 'set_%s' % (key), None)
		if f:
			f(value)
		else:
			self.__dict__[key] = value
		Model.__setattr__(self, key, value)