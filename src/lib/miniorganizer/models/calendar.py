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

from base import BaseModel
from alarm import AlarmModel
from event import EventModel
from todo import TodoModel
from dateutil import rrule

class CalendarModel(BaseModel):
	"""
	The CalendarModel class is a high-level wrapper which provides create,
	read, update and delete access to vCalendar files via models. Models are
	required as a bridge between the iCalendar library's vComponents and the
	rest of the application because of the way the Kiwi library's MVC works.

	All access to calendars from the application should go through this class,
	as it provides verification and consitancy of the data in the calendar.
	"""
	
	def __init__(self, vcalendar):
		BaseModel.__init__(self)

		self.__models = [] # List of Model derived class instances which bridge between Kiwi and iCalendar components
		self.__vcalendar = vcalendar
		self.modified = True
		for vcomponent in self.__vcalendar.subcomponents:
			self.__models.append(self.factory.model_from_vcomponent(vcomponent))

	def get_models(self, model_type):
		"""
		Return a list of models which match the model type given. Model type
		must be a class type from the miniorganizer.models module.
		"""
		return([model for model in self.__models if isinstance(model, model_type)])

	def get_model_by_uid(self, uid):
		"""
		Return the model that matches the vcal UID or None if no model matches the UID.
		"""
		m = [model for model in self.__models if model.get_uid() == uid]
		if m:
			return(m[0])
		else:
			return(None)

	def get_models_related_by_uid(self, uid):
		"""
		Return a list of models related to the model identified by 'uid'.
		"""
		return([model for model in self.__models if model.get_related_to() == uid])

	def get_events(self):
		"""
		Return a list of EventModel models in the calendar.
		"""
		return(self.get_models(EventModel))

	def get_events_recurring(self, dtstart, dtend):
		"""
		Return a list of EventModel models in the calendar, including fake
		events for recurring events. Fake events are generated for every
		occrurence of the event between dtstart and dtend.
		"""
		events = []
		for model in self.__models:
			if isinstance(model, EventModel):
				recur = model.get_recur()
				if recur:
					freq = getattr(rrule, recur['FREQ'][0])
					interval = int(recur['INTERVAL'][0])
					paramdict = {
						'freq': freq,
						'dtstart': model.get_start(),
						'interval': interval,
						'until': dtend
					}
					if recur['FREQ'] == ['WEEKLY'] and 'BYDAY' in recur:
						paramdict['byweekday'] = [getattr(rrule, weekday) for weekday in recur['BYDAY']]
					if (recur['FREQ'] == ['MONTHLY'] or recur['FREQ'] == ['YEARLY']) and 'BYDAY' in recur:
						m = re.match('(-?\d+)(.*)', recur['BYDAY'][0])
						bd_index = int(m.groups()[0]) - 1
						if bd_index >= 0:
							bd_index += 1
						paramdict['bysetpos'] = bd_index
						paramdict['byweekday'] = getattr(rrule, m.groups()[1])
					if 'BYMONTHDAY' in recur:
						paramdict['bymonthday'] = int(recur['BYMONTHDAY'][0])
					if 'BYMONTH' in recur:
						paramdict['bymonth'] = int(recur['BYMONTH'][0])
					if 'BYYEARDAY' in recur:
						paramdict['byyearday'] = int(recur['BYYEARDAY'][0])

					# Generate a list of dates on which this event recurs. Then
					# create fake events which are duplicates of this event so
					# that they can easily be displayed in the calendar, etc.
					irrule = rrule.rrule(**paramdict)
					if model.get_start() > dtstart:
						recur_dates = irrule.between(model.get_start(), dtend, inc=False)
					else:
						recur_dates = irrule.between(dtstart, dtend, inc=False)

					for date in recur_dates:
						event_start = model.get_start()
						event_end = model.get_end()

						fakeevent = model.dup()
						fakeevent.real_event = model # Mark this as a fake (recurring) event instance
						fakeevent.set_start(date)
						fakeevent.set_end(date + (event_end - event_start))

						events.append(fakeevent)
		return(events)

	def get_todos(self):
		"""
		Return a list of TodoModel models in the calendar.
		"""
		return(self.get_models(TodoModel))

	def get_alarms(self):
		"""
		Return a list of AlarmModel models in the calendar.
		"""
		alarms = []
		for model in self.__models:
			if hasattr(model, 'get_alarms'):
				alarms.extend(model.get_alarms())
		return(alarms)

	def get_vcalendar(self):
		return(self.__vcalendar)

	def add(self, model):
		"""
		Add a model to the calendar.
		"""
		self.__vcalendar.add_component(model.get_vcomponent())
		self.__models.append(model)
		self.modified = True
		
	def delete(self, model, recursive = False):
		"""
		Delete a model from the calendar. If `recursive` is set, also delete
		all models that are related to the model that is to be removed.
		"""
		if recursive:
			models = self.get_models_related_by_uid(model.get_uid())
			while models:
				self.delete(models.pop(0), True)

		self.__vcalendar.subcomponents.remove(model.get_vcomponent())
		self.__models.remove(model)
		self.modified = True

	def modified_inmem(self):
		models_modified = [model for model in self.__models if model.modified]
		if self.modified:
			models_modified.append(self)
		return(models_modified)
