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

import gtk
from kiwi.ui.delegates import GladeDelegate

class EventRequestUI(GladeDelegate):

	def __init__(self, mo, event):
		self.mo = mo
		self.event = event
		self.response = None

		GladeDelegate.__init__(self, gladefile="mo_event_request", toplevel_name='dialog_main')

		# Fill the user interface with information
		organizer = event.get_organizer()
		organizer_cn = organizer.params.get('CN', '')
		if organizer.upper().startswith('MAILTO:'):
				organizer_val = organizer[7:]
		else:
				organizer_val = organizer

		self.label_organizer.set_text('%s <%s>' % (organizer_cn, organizer_val))
		self.label_summary.set_text(event.get_summary())
		self.label_location.set_text(event.get_location())
		self.label_from.set_text(event.get_start().ctime())
		self.label_to.set_text(event.get_end().ctime())
		self.label_description.set_text(event.get_description())

	def run(self):
		self.show_all()
		gtk.main()
		return({'choice': self.response, 'notify': self.checkbutton_notify.get_active()})

	def on_button_accept__clicked(self, *args):
		self.response = 'ACCEPT'
		self.quit()

	def on_button_decline__clicked(self, *args):
		self.response = 'DECLINE'
		self.quit()
	
	def on_button_tentative__clicked(self, *args):
		self.response = 'TENTATIVE'
		self.quit()

	def on_dialog_main__delete_event(self, *args):
		self.quit()
		
	def on_button_cancel__clicked(self, *args):
		self.quit()

	def quit(self):
		self.view.hide()
		gtk.main_quit()
