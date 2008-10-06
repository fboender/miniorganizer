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

import string
import time
import random
from socket import gethostname

def gen_uid():
	"""
	Generate a unique random UID that can be used to uniquely identify
	iCalendar components.
	"""
	chars = list(string.ascii_letters + string.digits)
	uid = time.strftime('%Y%m%dT%H%M%SZ-')
	uid += ''.join([random.choice(chars) for i in range(16)])
	uid += '@' + gethostname()
	return(uid)
