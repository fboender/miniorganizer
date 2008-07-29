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

import os
import logging
import stat
import string
import datetime
import time
import random
import icalendar
import config
from models import Factory
from socket import gethostname
from models import AlarmModel, TodoModel, EventModel, Factory
from dateutil import rrule
import copy

class MiniOrganizer:
	"""
	This is the main MiniOrganizer interface. All information retrieval and
	manipulation on calendars and other aspects of MiniOrganizer should be done
	through this class.
	"""
	
	def __init__(self, calfile = None):
		self.log = logging.getLogger('MINICAL')

		self.__models = []
		self.factory = Factory(self)
		self.calendar = icalendar.Calendar()
		self.homedir = os.environ['HOME']
		self.confdir = os.path.join(self.homedir, '.miniorganizer')
		self.conffile = os.path.join(self.confdir, 'miniorganizer.ini')

		if not os.path.exists(self.confdir):
			self.first_time = True
			os.mkdir(self.confdir)
		if not os.path.exists(self.conffile):
			f = file(self.conffile, 'w')
			f.close()

		config_defaults = {
			'debug': (int, 30),
			'reminder.lastseen': (int, time.time()),
			'reminder.default_snooze': (int, 10),
			'events.default_show': (str, 'Month'),
			'events.cal_show_weeknr': (bool, 1),
			'miniorganizer.auto_save': (bool, 1),
		}
		self.config = config.Config(self.conffile, defaults=config_defaults)
		self.first_time = False

		if calfile:
			self.calfile = calfile
			self.config['miniorganizer.auto_save'] = False
		else:
			self.calfile = os.path.join(self.confdir, 'miniorganizer.ics')

		if os.path.exists(self.calfile):
			self.load(self.calfile)

		self.modified = False

	def clear(self):
		del self.__models[:]
		self.calendar = icalendar.Calendar()
		self.calfile = None
		self.modified = True
		# FIXME: Change mtime
		
	def load(self, calfile):
		self.clear()

		self.mtime = os.stat(calfile)[stat.ST_CTIME]
		self.log.debug('Loading iCal file \'%s\'.' % (calfile))
		f = file(calfile, 'r')
		contents = f.read()
		f.close()

		self.calendar = icalendar.Calendar.from_string(contents)
		
		for item in self.calendar.subcomponents:
			self.__models.append(self.factory.modelFromVComponent(item))

		self.calfile = calfile
		self.config['miniorganizer.auto_save'] = False

		self.modified = False

	def reload(self):
		del self.__models[:]
		self.load(self.calfile)

	def save(self, filename = None):
		self.log.debug('Saving calendar \'%s\'' % (self.calfile))

		if filename:
			# Save As..
			f = file(filename, 'w')
			f.write(self.calendar.as_string())
			f.close()

			self.calfile = filename
		elif self.calfile:
			# Save..
			f = file(self.calfile, 'w')
			f.write(self.calendar.as_string())
			f.close()
		else:
			raise Exception('No filename specified')

		self.modified = False

	def import_(self, calfile):
		f = file(calfile, 'r')
		contents = f.read()
		f.close()

		calendar = icalendar.Calendar.from_string(contents)
		for item in calendar.subcomponents:
			model = self.factory.modelFromVComponent(item)
			self.add(model)

		self.modified = True
		
	def getEvents(self):
		return([model for model in self.__models if isinstance(model, EventModel)])

	def getRecurEvents(self, dtstart, dtend):
		"""
		Return a list of fake events, and also generate 'fake' events for
		recurring events.
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

	def getTodos(self):
		return([model for model in self.__models if isinstance(model, TodoModel)])

	def getAlarms(self):
		alarms = []
		for model in self.__models:
			if hasattr(model, 'get_alarms'):
				alarms.extend(model.get_alarms())
		return(alarms)
		
	def getComponentByUID(self, uid):
		for model in self.__models:
			if model.get_uid() == uid:
				return(model)
		return(None)

	def getRelatedComponents(self, uid):
		components = []
		for component in self.__models:
			if component.get_related_to() == uid:
				components.append(component)
		return(components)

	def delete(self, model):
		"""
		Remove a component from the calendar.
		"""
		self.calendar.subcomponents.remove(model.get_vcomponent())
		self.__models.remove(model)
		self.modified = True

	def delRelatedTo(self, component):
		"""
		Remove a iCal component and all the items that relate to this component
		recursively.
		"""
		components = [component]
		while components:
			components.extend(self.getRelatedComponents(components[0].get_uid()))
			self.delete(components.pop(0))
		self.modified = True

	def add(self, model):
		"""
		Add a component to the calendar.
		"""
		self.calendar.add_component(model.get_vcomponent())
		self.__models.append(model)
		self.modified = True

	def changed(self):
		"""
		Return True if the calendar has changed on disk since it's last been
		read. False if it hasn't.
		"""
		mtime = os.stat(self.calfile)[stat.ST_CTIME]
		return(mtime > self.mtime)

	@staticmethod
	def genUID():
		"""
		Generate a unique random UID that can be used to uniquely identify
		iCalendar components.
		"""
		chars = list(string.ascii_letters + string.digits)
		uid = time.strftime('%Y%m%dT%H%M%SZ-')
		uid += ''.join([random.choice(chars) for i in range(16)])
		uid += '@' + gethostname()
		return(uid)

