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

class MiniOrganizer:
	"""
	This is the main MiniOrganizer interface. All information retrieval and
	manipulation on calendars and other aspects of MiniOrganizer should be done
	through this class.
	"""
	
	def __init__(self):
		self.log = logging.getLogger('MINICAL')

		self.__models = []
		self.factory = Factory(self)
		self.calendar = icalendar.Calendar()
		self.homedir = os.environ['HOME']
		self.confdir = os.path.join(self.homedir, '.miniorganizer')
		self.conffile = os.path.join(self.confdir, 'miniorganizer.ini')
		self.calfile = os.path.join(self.confdir, 'miniorganizer.ics')
		self.first_time = False

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
		}
		self.config = config.Config(self.conffile, defaults=config_defaults)

		if not os.path.exists(self.calfile):
			self.save()
		else:
			self.load()

	def load(self):
		self.mtime = os.stat(self.calfile)[stat.ST_CTIME]
		self.log.debug('Loading iCal file \'%s\'.' % (self.calfile))
		f = file(self.calfile, 'r')
		contents = f.read()
		f.close()

		self.calendar = icalendar.Calendar.from_string(contents)
		
		for item in self.calendar.subcomponents:
			self.__models.append(self.factory.modelFromVComponent(item))

	def reload(self):
		self.__models = []
		self.load()

	def save(self):
		self.log.debug('Saving the calendar')

		# Save the calendar
		f = file(self.calfile, 'w')
		f.write(self.calendar.as_string())
		f.close()

		# Save the configuration
		self.config.save()

	def getEvents(self):
		return([model for model in self.__models if isinstance(model, EventModel)])

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

	def delRelatedTo(self, component):
		"""
		Remove a iCal component and all the items that relate to this component
		recursively.
		"""
		components = [component]
		while components:
			components.extend(self.getRelatedComponents(components[0].get_uid()))
			self.delete(components.pop(0))

	def add(self, model):
		"""

		Add a component to the calendar.
		"""
		self.calendar.add_component(model.get_vcomponent())
		self.__models.append(model)

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
