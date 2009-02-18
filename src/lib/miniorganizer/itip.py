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

"""
The ITIP library takes care of the exchange of iCalendar information such as 
meeting requests, etc. 
"""

import icalendar

class ITIP(object):
	def __init__(self, base_cal, remote_cal):
		self.base_cal = base_cal
		self.remote_cal = remote_cal
		self.events = []

		# Check if the remote cal has anything we need to act upon.  In there
		# is something we need to act upon, we place an event in the event
		# queue so that the UI can show information about it.
		method = self.remote_cal.get_method()
		if method.upper() == 'REQUEST':
			self.events.append( ('REQUEST', self.remote_cal) )
