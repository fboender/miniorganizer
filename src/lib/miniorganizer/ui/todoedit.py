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
from kiwi.ui.delegates import GladeDelegate
import miniorganizer.ui

class TodoEditUI(GladeDelegate):

	def __init__(self, mo, todo):
		self.mo = mo
		self.todo = todo
		self.old_alarms = self.todo.get_alarms()
		self.new_alarms = self.old_alarms[:]

		GladeDelegate.__init__(self, gladefile="mo_todo_edit", toplevel_name='dialog_main')

		# Set up the user interface
		self.alarms_edit_ui = miniorganizer.ui.AlarmsEditUI(self.mo, self.new_alarms, self.todo)
		self.vbox_alarms.pack_start(self.alarms_edit_ui.listcontainer_alarms)
		self.dateedit_due = miniorganizer.ui.DateTimeEditUI(todo.get_due())
		self.attach_slave("eventbox_due", self.dateedit_due)
		if self.old_alarms:
			self.expander_alerts.set_expanded(True)

		# Fill the user interface with information
		self.summary.set_text(todo.get_summary())
		self.priority.set_value(float(todo.get_priority()))
		c_buffer = self.description.get_buffer()
		c_inspos = c_buffer.get_insert()
		c_insiter = c_buffer.get_iter_at_mark(c_inspos)
		self.description.get_buffer().insert(c_insiter, todo.get_description())
		if todo.get_due():
			self.dateedit_due.set_datetime(todo.get_due())
			self.checkbutton_due.set_active(True)
		else:
			self.checkbutton_due.set_active(False)
		self.on_checkbutton_due__toggled(self.checkbutton_due)

	def run(self):
		self.show_all()
		gtk.main()
		return(self.todo)

	def dateedit_due__changed(self, dateedit_due, dt):
		self.todo.set_due(dt)

	def on_checkbutton_due__toggled(self, toggle):
		state = toggle.get_active()
		self.dateedit_due.set_sensitive(state)
		self.alarms_edit_ui.set_sensitive(state)
		if state:
			self.dateedit_due__changed(self.dateedit_due, self.dateedit_due.dt)

	def on_button_ok__clicked(self, *args):
		c_buffer = self.description.get_buffer()
		c_startpos = c_buffer.get_iter_at_offset(0)
		c_endpos = c_buffer.get_iter_at_offset(-1)
		description = c_buffer.get_text(c_startpos, c_endpos)
		has_due = self.checkbutton_due.get_active()
		due_dt = self.dateedit_due.dt

		if has_due:
			self.todo.set_due(due_dt)

			for alarm in self.old_alarms:
				if alarm not in self.new_alarms:
					self.todo.del_alarm(alarm)

			# Any alarms that weren't previously in the list, but are now, are new.
			# Add them to the event.
			for i in range(len(self.new_alarms)):
				alarm = self.new_alarms[i]
				if not alarm in self.old_alarms:
					self.todo.add_alarm(alarm)
		else:
			self.todo.set_due(None)
			for alarm in self.old_alarms:
				self.todo.del_alarm(alarm)
			
		self.todo.set_summary(self.summary.get_text())
		self.todo.set_priority(int(self.priority.get_value()))
		self.todo.set_description(description)
			
		self.quit()
	
	def on_button_cancel__clicked(self, *args):
		self.todo = None
		self.quit()

	def on_dialog_main__delete_event(self, *args):
		self.quit()
		
	def quit(self):
		self.view.hide()
		gtk.main_quit()
