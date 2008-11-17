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
import datetime
import icalendar
import config
import time
from models import Factory, AlarmModel, TodoModel, EventModel, CalendarModel
from dateutil import rrule
import copy
from kiwi.ui import dialogs

class MiniOrganizer:
	"""
	This is the main MiniOrganizer controller. All information retrieval and
	manipulation on calendars and other aspects of MiniOrganizer should be done
	through this class.
	"""
	
	def __init__(self, cal_fname = None):
		self.log = logging.getLogger('MINICAL')
		self.factory = Factory()

		self.cal_modified = False
		self.cal_mtime = 0
		self.cal_fname = None
		self.cal_model = None
		self.homedir = os.environ['HOME']
		self.conf_dir = os.path.join(self.homedir, '.miniorganizer')
		self.conf_fname = os.path.join(self.conf_dir, 'miniorganizer.ini')

		if not os.path.exists(self.conf_dir):
			self.first_time = True
			os.mkdir(self.conf_dir)
		if not os.path.exists(self.conf_fname):
			f = file(self.conf_fname, 'w')
			f.close()

		config_defaults = {
			'debug': (int, 30),
			'reminder.lastseen': (int, time.time()),
			'reminder.default_snooze': (int, 10),
			'events.default_show': (str, 'Month'),
			'events.cal_show_weeknr': (bool, True),
			'miniorganizer.auto_save': (bool, True),
		}
		self.config = config.Config(self.conf_fname, defaults=config_defaults)

		# Load a given calendar or create a new empty one
		if cal_fname:
			self.cal_fname = cal_fname
			self.load(self.cal_fname)
		else:
			cal_fname = os.path.join(self.conf_dir, 'miniorganizer.ics')
			try:
				self.load(cal_fname)
			except (IOError, OSError), e:
				self.new(cal_fname)

		self.first_time = False

	def clear(self):
		raise NotImplementedError()
		
	def new(self, cal_fname = None):
		self.log.debug('Creating new iCal file.')
		self.cal_model = self.factory.calendar()
		self.cal_modified = False
		self.cal_fname = cal_fname
		self.save()
		
	def load(self, cal_fname):
		self.log.debug('Loading iCal file \'%s\'.' % (cal_fname))

		cal_mtime = os.stat(cal_fname)[stat.ST_CTIME]
		f = file(cal_fname, 'r')
		contents = f.read()
		f.close()

		try:
			cal_model = CalendarModel(icalendar.Calendar.from_string(contents))

			self.cal_mtime = cal_mtime
			self.cal_model = cal_model
			self.cal_modified = False
			self.cal_fname = cal_fname
		except ValueError, e:
			dialogs.error('Error in calendar file', str(e))
			
	def reload(self):
		#del self.__models[:]
		self.load(self.cal_fname)

	def save(self, filename = None):
		self.log.debug('Saving calendar \'%s\'' % (self.cal_fname))

		print self.cal_fname
		if filename:
			# Save As..
			f = file(filename, 'w')
			f.write(self.cal_model.get_vcalendar().as_string())
			f.close()

			self.cal_fname = filename
		elif self.cal_fname:
			# Save..
			f = file(self.cal_fname, 'w')
			f.write(self.cal_model.get_vcalendar().as_string())
			f.close()
		else:
			raise Exception('No filename specified')

		self.cal_modified = False

	def import_(self, cal_fname):
		f = file(cal_fname, 'r')
		contents = f.read()
		f.close()

		calendar = icalendar.Calendar.from_string(contents)
		for item in calendar.subcomponents:
			model = self.factory.model_from_vcomponent(item)
			self.calendarModel.add(model)

		self.cal_modified = True
		
	def modified_ondisk(self):
		"""
		Return True if the calendar has changed on disk since it's last been
		read. False if it hasn't.
		"""
		cal_mtime = os.stat(self.cal_fname)[stat.ST_CTIME]
		return(cal_mtime > self.cal_mtime)

