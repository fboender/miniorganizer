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
import miniorganizer.models
import miniorganizer.ui
from kiwi.ui.delegates import GladeDelegate
from kiwi.ui import dialogs

class EventEditUI(GladeDelegate):

	def __init__(self, mo, event):
		self.mo = mo
		self.event = event
		self.end_changed = False # To keep track of wether the user has modified the To: date. 
		self.old_alarms = self.event.get_alarms()
		self.new_alarms = self.old_alarms[:]

		GladeDelegate.__init__(self, gladefile="mo_event_edit", toplevel_name='dialog_main')

		# Set up the user interface
		self.alarms_edit_ui = miniorganizer.ui.AlarmsEditUI(self.mo, self.new_alarms, self.event)
		self.vbox_alarms.pack_start(self.alarms_edit_ui.listcontainer_alarms)
		self.dateedit_start = miniorganizer.ui.DateTimeEditUI(event.get_start())
		self.dateedit_end = miniorganizer.ui.DateTimeEditUI(event.get_end())
		self.attach_slave("eventbox_start", self.dateedit_start)
		self.attach_slave("eventbox_end", self.dateedit_end)

		# Connect signals
		self.dateedit_start.entry_date.connect('changed', self.dateedit_start__changed)
		self.dateedit_end.entry_date.connect('changed', self.dateedit_end__changed)

		# Fill the user interface with information
		notime = datetime.time(0, 0)
		if event.get_start().time() == notime and event.get_end().time() == notime:
			self.checkbutton_wholeday.set_active(True)
		self.summary.set_text(self.event.get_summary())
		c_buffer = self.description.get_buffer()
		c_inspos = c_buffer.get_insert()
		c_insiter = c_buffer.get_iter_at_mark(c_inspos)
		self.description.get_buffer().insert(c_insiter, event.get_description())

		self.show_all()
		gtk.main()

	def dateedit_start__changed(self, *args):
		if not self.end_changed:
			self.dateedit_end.entry_date.set_date(self.dateedit_start.entry_date.get_date())

	def dateedit_end__changed(self, *args):
		self.end_changed = True

	def on_checkbutton_wholeday__toggled(self, toggle):
		state = toggle.get_active()

		self.dateedit_start.entry_time.set_sensitive(not state)
		self.dateedit_end.entry_time.set_sensitive(not state)

		if state:
			self.dateedit_start.entry_time.update(datetime.time(0, 0))
			self.dateedit_end.entry_time.update(datetime.time(0, 0))

	def on_button_ok__clicked(self, *args):
		c_buffer = self.description.get_buffer()
		c_startpos = c_buffer.get_iter_at_offset(0)
		c_endpos = c_buffer.get_iter_at_offset(-1)
		description= c_buffer.get_text(c_startpos, c_endpos)

		start_dt = self.dateedit_start.dt
		end_dt = self.dateedit_end.dt

		if end_dt <= start_dt:
			dialogs.error('The event starts before it has begon. Please change the Start or End date/time.')
			return
		# FIXME: Check for valid date/time.

		# Any alarms that were previously in the list but not anymore have been
		# removed. Delete them from the event.
		for alarm in self.old_alarms:
			if alarm not in self.new_alarms:
				self.event.del_alarm(alarm)

		# Any alarms that weren't previously in the list, but are now, are new.
		# Add them to the event.
		for i in range(len(self.new_alarms)):
			alarm = self.new_alarms[i]
			if not alarm in self.old_alarms:
				self.event.add_alarm(alarm)
			
		self.event.set_summary(self.summary.get_text())
		self.event.set_description(description)
		self.event.set_start(start_dt)
		self.event.set_end(end_dt)

		self.quit()
	
	def on_button_cancel__clicked(self, *args):
		self.quit()

	def on_dialog_main__delete_event(self, *args):
		self.quit()
		
	def quit(self):
		self.view.hide()
		gtk.main_quit()
