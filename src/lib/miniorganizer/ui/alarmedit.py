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
import datetime
import miniorganizer.models
from kiwi.ui.delegates import GladeDelegate

# FIXME: This doesn't use dialogs in the right way. It should return a response
# and the parent should keep an old copy of the alarm and not update it.
class AlarmEditUI(GladeDelegate):
	offset_type_to_index = {
		'days': 2,
		'hours': 1,
		'minutes':0,
		'unknown': 0,
	}

	def __init__(self, mo, alarm, start_time):
		self.mo = mo
		self.alarm = alarm
		self.start_time = start_time
		self.old_delta = self.alarm.get_delta()

		GladeDelegate.__init__(self, gladefile="mo_alarm_edit", toplevel_name='dialog_main')

		days, hours, minutes, seconds = self.alarm.get_offset()
		self.entry_days.set_text(str(days))
		self.entry_hours.set_text(str(hours))
		self.entry_minutes.set_text(str(minutes))
		self.entry_days.connect('changed', self.trigger_on_update)
		self.entry_hours.connect('changed', self.trigger_on_update)
		self.entry_minutes.connect('changed', self.trigger_on_update)

		self.trigger_on_update()

	def run(self):
		self.show_all()
		gtk.main()
		return(self.alarm)

	def get_delta(self):
		delta = datetime.timedelta(
			days=-int(self.entry_days.get_text()),
			hours=-int(self.entry_hours.get_text()),
			minutes=-int(self.entry_minutes.get_text())
		)
		return(delta)
		
	def trigger_on_update(self, *args):
		try:
			delta = self.get_delta()
			text = "Triggers on: %s" % (self.start_time - delta)
			self.label_trigger_on.set_text(text)
		except ValueError, e:
			pass
		
	def on_button_ok__clicked(self, *args):
		delta = self.get_delta()
		self.alarm.set_delta(delta)
		self.quit()

	def on_button_cancel__clicked(self, *args):
		self.alarm.set_delta(self.old_delta)
		self.alarm = None
		self.quit()

	def quit(self):
		self.view.hide()
		gtk.main_quit()

