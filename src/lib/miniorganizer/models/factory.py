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

# FIXME: This shouldn't be a class, or at least the methods should be static.
# Now, all classes have to initialize this class first, which is rather
# annoying.

import datetime
import icalendar
from calendar import CalendarModel
from event import EventModel
from alarm import AlarmModel
from todo import TodoModel
from journal import JournalModel
from miniorganizer.tools import gen_uid

class Factory():
	"""
	The model factory class provides a mechanism for creating new empty models
	from scratch. It fills in the default required fields of the models if
	needed.
	"""
	def __init__(self):
		pass

	def calendar(self):
		"""
		Create a new CalendarModel.
		"""
		vcalendar = icalendar.Calendar()
		vcalendar.set('PRODID', 'MiniOrganizer %%VERSION%%')
		calendar_model = CalendarModel(vcalendar)
		return(calendar_model)

	def calendar_from_vcomponent(self, vcalendar):
		calendar_model = CalendarModel(vcalendar)
		return(calendar_model)

	def event(self, start, end):
		"""
		Create a new EventModel. `start` and `end` are datetime values for the
		DTSTART and DTEND field of the model.
		"""
		vevent = icalendar.Event()
		vevent.set('UID', gen_uid())
		vevent.set('CREATED', datetime.datetime.now())
		vevent.set('DTSTART', start)
		vevent.set('DTEND', end)
		event_model = EventModel(vevent)
		return(event_model)

	#def event_from_vcomponent(self, vevent):
	def event_from_vcomponent(self, vevent):
		"""
		Create a EventModel from a vEvent iCalendar component.
		"""
		event_model = EventModel(vevent)
		return(event_model)

	def todo(self, parent_model=None):
		"""
		Create a new TodoModel. `parent_model` is the parent TodoModel to which
		this todo belongs.
		"""
		vtodo = icalendar.Todo()
		vtodo.set('UID', gen_uid())
		vtodo.set('CREATED', datetime.datetime.now())
		vtodo.set('PERCENTAGE-COMPLETE', 0)
		if parent_model:
			vtodo.set('RELATED-TO', parent_model.get_uid())
		todo_model = TodoModel(vtodo)
		return(todo_model)

	def todo_from_vcomponent(self, vtodo):
		"""
		Create a TodoModel from a vTodo iCalendar component.
		"""
		# FIXME: no parent_model?
		todo_model = TodoModel(vtodo)
		return(todo_model)
		
	def alarm(self, delta, parent_model):
		"""
		Create a new AlarmModel. `delta` is a date/time offset as returned by
		datetime.timedelta(). `parent_model` is the parent model to which this
		alarm belongs, such as a EventModel or TodoModel.
		"""
		valarm = icalendar.Alarm()
		valarm.set('UID', gen_uid())
		valarm.set('TRIGGER', delta)
		valarm.set('ACTION', 'DISPLAY')
		alarm_model = AlarmModel(valarm, parent_model)
		return(alarm_model)
		
	#def alarm_from_vcomponent(self, valarm, parent_model):
	def alarm_from_vcomponent(self, valarm, parent_model):
		"""
		Create an AlarmModel from a vAlarm iCalendar component. `parent_model`
		is the parent model to which this alarm belongs, such as an EventModel
		or TodoModel.
		"""
		alarm_model = AlarmModel(valarm, parent_model)
		return(alarm_model)

	def journal(self, parent_model=None):
		"""
		Create a new JournalModel. `parent_model` is the parent JournalModel to which
		this todo belongs.
		"""
		vjournal = icalendar.Journal()
		vjournal.set('UID', gen_uid())
		if parent_model:
			vjournal.set('RELATED-TO', parent_model.get_uid())
		journal_model = JournalModel(vjournal)
		return(journal_model)
		
	def journal_from_vcomponent(self, vjournal):
		"""
		Create an JournalModel from a vJournal iCalendar component. 
		"""
		journal_model = JournalModel(vjournal)
		return(journal_model)

	def model_from_vcomponent(self, vcomponent):
		"""
		Create a Model from a vComponent. Automatically guesses the type of the
		vComponent (vEvent, vTodo, etc) and returns a EventModel, TodoModel,
		etc created from the vComponent, or None is the type of vComponent is
		not supported.
		"""
		if isinstance(vcomponent, icalendar.cal.Calendar):
			return(self.calendar_from_vcomponent(vcomponent))
		elif isinstance(vcomponent, icalendar.cal.Event):
			return(self.event_from_vcomponent(vcomponent))
		elif isinstance(vcomponent, icalendar.cal.Todo):
			return(self.todo_from_vcomponent(vcomponent))
		elif isinstance(vcomponent, icalendar.cal.Alarm):
			return(self.alarm_from_vcomponent(vcomponent))
		elif isinstance(vcomponent, icalendar.cal.Journal):
			return(self.journal_from_vcomponent(vcomponent))
		else:
			return(None)
			#raise NotImplementedError('Component type \'%s\' is not supported yet.' % (type(vcomponent)))
