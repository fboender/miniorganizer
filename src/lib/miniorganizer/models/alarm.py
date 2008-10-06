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

class AlarmModel(BaseModel):

	def __init__(self, valarm, parent_model):
		BaseModel.__init__(self)

		self.__valarm = valarm
		self.__parent_model = parent_model
		self.modified = False

	def get_delta(self):
		return(self.__valarm['TRIGGER'].dt)

	def set_delta(self, delta):
		self.__valarm.set('TRIGGER', delta)
		self.modified = True

	def get_offset(self):
		delta = self.__valarm['TRIGGER'].dt

		if delta.days > 0:
			raise NotImplementedError('Triggers after the appointment are not supported')
		else:
			# Invert it so we can find the days, hours and minutes.
			delta = -delta

		days = delta.days
		minutes, seconds = divmod(delta.seconds, 60)
		hours, minutes = divmod(minutes, 60)

		offset = (days, hours, minutes, seconds)
		return(offset)

	def set_offset(self, days=0, hours=0, minutes=0, seconds=0):
		delta = datetime.timedelta(
			days=-(days),
			hours=-(hours),
			minutes=-(minutes),
			seconds=-(seconds),
		)
		self.__valarm.set('TRIGGER', delta)
		self.modified = True

	def get_offsetformat(self):
		days, hours, minutes, seconds = self.get_offset()
		return('%i days, %i hours, %i minutes' % (days, hours, minutes))

	def get_type(self):
		types = {
			'DISPLAY': 'Show dialog',
			'EMAIL': 'Send an email',
			'AUDIO': 'Play a sound',
			'PROCEDURE': 'Run a program',
		}
		return(types[self.__valarm.get('ACTION')])

	def get_trigger_dt(self):
		return(self.__parent_model.get_start() + self.__valarm['TRIGGER'].dt)

	def get_valarm(self):
		return(self.__valarm)
		
	def get_uid(self):
		return(self.__valarm.get('UID', None))

	def get_parent_model(self):
		return(self.__parent_model)

	def __cmp__(self, x):
		xtrigger = x.get_trigger_dt()
		strigger = self.get_trigger_dt()

		if xtrigger < strigger:
			return(1)
		elif xtrigger > strigger:
			return(-1)
		else:
			return(0)
