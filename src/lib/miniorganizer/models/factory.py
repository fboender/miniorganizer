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
from event import EventModel
from alarm import AlarmModel
from todo import TodoModel

class Factory():
	def __init__(self, mo):
		self.mo = mo
	
	def event(self, start, end):
		vevent = icalendar.Event()
		vevent.set('UID', self.mo.genUID())
		vevent.set('CREATED', datetime.datetime.now())
		vevent.set('DTSTART', start)
		vevent.set('DTEND', end)
		event_model = EventModel(self.mo, vevent)
		return(event_model)

	def eventFromVComponent(self, vevent):
		event_model = EventModel(self.mo, vevent)
		return(event_model)

	def alarm(self, delta, parent_model):
		valarm = icalendar.Alarm()
		valarm.set('UID', self.mo.genUID())
		valarm.set('TRIGGER', delta)
		valarm.set('ACTION', 'DISPLAY')
		alarm_model = AlarmModel(self.mo, valarm, parent_model)
		return(alarm_model)
		
	def alarmFromVComponent(self, valarm, parent_model):
		alarm_model = AlarmModel(self.mo, valarm, parent_model)
		return(alarm_model)

	def todo(self, parent_model=None):
		vtodo = icalendar.Todo()
		vtodo.set('UID', self.mo.genUID())
		vtodo.set('CREATED', datetime.datetime.now())
		vtodo.set('PERCENTAGE-COMPLETE', 0)
		if parent_model:
			vtodo.set('RELATED-TO', parent_model.get_uid())
		todo_model = TodoModel(self.mo, vtodo)
		return(todo_model)

	def todoFromVComponent(self, vtodo):
		todo_model = TodoModel(self.mo, vtodo)
		return(todo_model)
		
	def modelFromVComponent(self, vcomponent):
		if isinstance(vcomponent, icalendar.cal.Event):
			return(self.eventFromVComponent(vcomponent))
		elif isinstance(vcomponent, icalendar.cal.Todo):
			return(self.todoFromVComponent(vcomponent))
		elif isinstance(vcomponent, icalendar.cal.Alarm):
			return(self.alarmFromVComponent(vcomponent))
		else:
			raise NotImplementedError('Component type \'%s\' is not supported yet.' % (type(vcomponent)))
