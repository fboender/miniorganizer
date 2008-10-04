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
import gtk
from kiwi.ui.delegates import GladeDelegate

class ReminderUI(GladeDelegate):

	widgets = []

	def __init__(self, mo, event):
		self.mo = mo
		self.event = event
		self.snooze_delta = None

		label_text = "<b>%s</b>\n%s" % (event.get_summary(), event.get_description())
		GladeDelegate.__init__(self, gladefile="mo_reminder", toplevel_name='dialog_main')
		self.get_toplevel().set_modal(True)
		self.get_toplevel().stick()
		self.get_toplevel().set_keep_above(True)

		self.entry_snoozetime.set_text(str(mo.config['reminder.default_snooze']))
		self.label_summary.set_label('<span size=\'large\'><b>%s</b></span>' % (event.get_summary()))
		self.label_from.set_text(event.get_start().ctime())
		self.label_to.set_text(event.get_end().ctime())
		self.label_description.set_text('%s' % (event.get_description()))
		if getattr(event, 'get_location'):
			self.label_location.set_text(event.get_location())

	def run(self):
		self.show_all()
		gtk.main()

		return(self.snooze_delta)

	def on_dialog_main__delete_event(self, *args):
		self.quit()
		
	def on_button_dismiss__clicked(self, *args):
		self.quit()
		
	def on_button_snooze__clicked(self, *args):
		snooze_time = int(self.entry_snoozetime.get_text())
		now = datetime.datetime.now()
		self.snooze_delta = datetime.timedelta(minutes=snooze_time)

		self.quit()

	def quit(self):
		self.view.hide()
		gtk.main_quit()

