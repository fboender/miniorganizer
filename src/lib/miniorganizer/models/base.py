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

from kiwi.model import Model

class BaseModel(Model):
	"""
	Base Model class which provides commonly required modules, etc to the other
	models.
	"""
	
	def __init__(self):
		# Deferred importing of modules to avoid circularly importing modules.
		self.models = __import__('miniorganizer.models', fromlist=['models'])
		self.factory = self.models.Factory()

	def __setattr__(self, key, value):
		"""
		When a model is updated from Kiwi, Kiwi directly sets an attribute on
		the class instance. It should, however, go through the set_ methods.
		This method intercepts direct attribute setting and re-routes the
		setting of the attribute to the set_ method of the instance.
		"""
		f = getattr(self, 'set_%s' % (key), None)
		if f:
			f(value)
		else:
			self.__dict__[key] = value
		Model.__setattr__(self, key, value)
