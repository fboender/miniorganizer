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

#import datetime
from base import BaseModel
from cgi import escape

class JournalModel(BaseModel):
	
	def __init__(self, vjournal):
		BaseModel.__init__(self)

		self.__vjournal = vjournal
		self.modified = False

	def get_summary(self):
		return(self.__vjournal.get('SUMMARY', ''))

	def get_summaryformat(self):
		return(escape(self.__vjournal.get('SUMMARY', '')))

	def set_summary(self, summary):
		self.__vjournal.set('SUMMARY', summary)
		self.modified = True

	def get_description(self):
		return(self.__vjournal.get('DESCRIPTION', ''))
		
	def get_descriptionformat(self):
		return(escape(self.__vjournal.get('DESCRIPTION', '')))
		
	def set_description(self, description):
		self.__vjournal.set('DESCRIPTION', description)
		self.modified = True

	def get_uid(self):
		return(self.__vjournal.get('UID', None))

	def get_related_to(self):
		return(self.__vjournal.get('RELATED-TO', None))
			
	def get_vcomponent(self):
		return(self.__vjournal)

