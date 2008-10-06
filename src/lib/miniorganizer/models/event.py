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
from base import BaseModel
from copy import copy

class EventModel(BaseModel):
	
	def __init__(self, vevent):
		BaseModel.__init__(self)

		self.__vevent = vevent
		self.__alarms = []
		self.modified = False
		for valarm in self.__vevent.walk('VALARM'):
			self.__alarms.append(self.factory.alarm_from_vcomponent(valarm, self))

	def get_summary(self):
		return(self.__vevent.get('SUMMARY', ''))

	def set_summary(self, summary):
		self.__vevent.set('SUMMARY', summary)
		self.modified = True

	def get_summaryformat(self):
		now = datetime.datetime.now()
		if self.get_end() < now:
			fmt = '<s>%s</s>'
		elif self.get_start() < now and self.get_end() > now:
			fmt = '<b>%s</b>'
		else:
			fmt = '%s'
		return(fmt % (self.get_summary()))
		
	def get_description(self):
		return(self.__vevent.get('DESCRIPTION', '').replace('\\n', '\n'))

	def set_description(self, description):
		self.__vevent.set('DESCRIPTION', description.replace('\n', '\\n'))
		self.modified = True

	def get_descriptionformat(self):
		return(self.get_description())

	def get_start(self):
		dt = self.__vevent['DTSTART'].dt
		dt = datetime.datetime(*(dt.timetuple()[:-3]))
		return(dt)

	def set_start(self, start):
		self.__vevent.set('DTSTART', start)
		self.modified = True

	def get_end(self):
		dt = self.__vevent['DTEND'].dt
		dt = datetime.datetime(*(dt.timetuple()[:-3]))
		return(dt)

	def set_end(self, end):
		self.__vevent.set('DTEND', end)
		self.modified = True

	def get_endformat(self):
		end = self.__vevent.get('DTEND', None)
		if end:
			end = datetime.datetime(*end.dt.timetuple()[:-3])
		return(end)
		
	def get_duration(self):
		return(self.get_end() - self.get_start())

	def set_duration(self, duration):
		self.set_end(self.get_start() + duration)
		self.modified = True
		
	def get_durationformat(self):
		return(str(self.get_duration()))

	def get_location(self):
		return(self.__vevent.get('LOCATION', ''))

	def set_location(self, location):
		self.__vevent.set('LOCATION', location)
		self.modified = True

	def get_alarms(self):
		return(self.__alarms)

	def add_alarm(self, alarm):
		self.__vevent.add_component(alarm.get_valarm())
		self.__alarms.append(alarm)
		self.modified = True

	def del_alarm(self, alarm):
		self.__vevent.subcomponents.remove(alarm.get_valarm())
		self.__alarms.remove(alarm)
		self.modified = True

	def get_vcomponent(self):
		return(self.__vevent)

	def get_uid(self):
		return(self.__vevent.get('UID', None))

	def get_related_to(self):
		return(self.__vevent.get('REALTED-TO', None))
			
	def get_recur(self):
		return(self.__vevent.get('RRULE', None))

	def set_recur(self, recur):
		self.__vevent.set('RRULE', recur)
		self.modified = True
		
	def __cmp__(self, x):
		if not isinstance(x, EventModel):
			return(-1)

		xstart = x.get_start()
		sstart = self.get_start()

		if xstart < sstart:
			return(1)
		elif xstart > sstart:
			return(-1)
		else:
			return(0)

	def dup(self):
		# FIXME: Move to BaseModel?
		vevent = copy(self.__vevent)
		event = self.factory.event_from_vcomponent(vevent)
		return(event)
