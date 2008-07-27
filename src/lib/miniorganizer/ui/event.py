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
import re
import miniorganizer.models
import miniorganizer.ui
from dateutil.relativedelta import relativedelta
from kiwi.ui.delegates import GladeSlaveDelegate
from kiwi.ui.objectlist import ObjectTree, Column, ColoredColumn

class EventUI(GladeSlaveDelegate):
	
	show_ranges = ['day', 'week', 'month', 'year']

	def __init__(self, parent, mo):
		self.parent = parent
		self.mo = mo

		self.__stop_auto_highlight = False # Disable automatic highlighting of events.
		self.__stop_auto_dayjump = False   # Disable automatically jumping to the start of the event on selection.
		self.__stop_auto_treeview_update = False   # FIXME

		GladeSlaveDelegate.__init__(self, gladefile='mo_tab_events', toplevel_name='window_main')

		# Set up the user interface
		eventColumns = [
			Column('start', title='Start', data_type=datetime.datetime, sorted=True),
			Column('end', title='End', data_type=datetime.datetime),
			Column('summaryformat', title='Summary', use_markup=True),
			Column('duration', title='Duration', justify=gtk.JUSTIFY_RIGHT)
		]
		self.treeview_event = ObjectTree(eventColumns)
		self.vbox_eventslist.add(self.treeview_event)
		self.combobox_display_range.set_active(self.show_ranges.index(self.mo.config['events.default_show'].lower()))
		cal_options = gtk.CALENDAR_WEEK_START_MONDAY
		if self.mo.config['events.cal_show_weeknr']:
			cal_options |= gtk.CALENDAR_SHOW_WEEK_NUMBERS
		self.calendar.set_display_options((self.calendar.get_display_options() | cal_options))

		# Connect signals
		self.treeview_event.connect('selection-changed', self.treeview_event__selection_changed)
		self.treeview_event.connect('row-activated', self.treeview_event__row_activated)
		self.treeview_event.connect('key-press-event', self.treeview_event__key_press_event)

		self.on_toolbutton_today__clicked()
	
	def refresh(self):
		"""
		Refresh the entire events tab. This clears everything and rebuilds it.
		Call this when events are removed outside of this class.
		"""
		self.treeview_event.clear()
		self.calendar.clear_marks()
		self.on_calendar__month_changed(self.calendar)
		self.treeview_event__update()

	def on_toolbutton_add__clicked(self, *args):
		now = datetime.datetime.now()
		sel_day = self.calendar.get_date()
		start = datetime.datetime(sel_day[0], sel_day[1]+1, sel_day[2], now.hour, now.minute)
		end = start + datetime.timedelta(hours=+1)

		event = self.mo.factory.event(start, end)
		if miniorganizer.ui.EventEditUI(self.mo, event):
			self.mo.add(event)
			self.treeview_event.append(None, event)
			self.on_calendar__month_changed(self.calendar)
			self.on_calendar__day_selected(self.calendar)
			self.parent.menuitem_save.set_sensitive(True)

	def on_toolbutton_remove__clicked(self, *args):
		sel_event = self.treeview_event.get_selected()
		if sel_event:
			self.mo.delete(sel_event)
			self.treeview_event.remove(sel_event)
			self.on_calendar__month_changed(self.calendar)
			self.on_calendar__day_selected(self.calendar)
			self.parent.menuitem_save.set_sensitive(True)

	def on_toolbutton_edit__clicked(self, *args):
		sel_event = self.treeview_event.get_selected()
		self.treeview_event__row_activated(self.treeview_event, sel_event)

	def on_toolbutton_today__clicked(self, *args):
		today_dt = datetime.date.today()
		self.calendar.select_month(today_dt.month - 1, today_dt.year)
		self.calendar.select_day(today_dt.day)

	def on_calendar__month_changed(self, calendar, *args):
		self.calendar.clear_marks()
		sel_date = self.calendar.get_date()

		month_start = datetime.datetime(sel_date[0], sel_date[1]+1, 1)
		month_end = month_start + relativedelta(months=+1, seconds=-1)

		events = self.mo.getEvents() + self.mo.getRecurEvents(month_start, month_end)
		for event in events:
			event_start = event.get_start()
			event_end = event.get_end()

			# If the event falls in the month, mark the days the event spans in
			# the calendar.
			if (month_start >= event_start and month_start <= event_end) or \
               (month_end >= event_start and month_end <= event_end) or \
               (event_start >= month_start and event_end <= month_end):
				# Walk through the days of the event, marking them.
				delta_iter = datetime.datetime(*event_start.timetuple()[0:3])
				while True:
					if delta_iter.year == month_start.year and delta_iter.month == month_start.month:
						self.calendar.mark_day(delta_iter.day)
					delta_iter = delta_iter + datetime.timedelta(days=+1)
					if delta_iter >= event_end:
						break

	def on_calendar__day_selected(self, calendar, *args):
		# Make sure the correct display range is shown.
		self.on_combobox_display_range__changed()

		# Retrieve the day the user selected.
		sel_day = self.calendar.get_date()
		day_start = datetime.datetime(sel_day[0], sel_day[1]+1, sel_day[2])
		day_end = day_start + datetime.timedelta(days=+1)

		display_month = datetime.datetime(day_start.year, day_start.month, 1)

		# Highlight an event if it starts on the selected day.
		highlight_events = []
		events = [event for event in self.treeview_event]
		for event in events:
			event_start = event.get_start()
			event_end = event.get_end()

			# If this is the first event that starts on the day the user
			# selected, highlight the item in the list of events.
			if event_start >= day_start and event_start < day_end:
				highlight_events.insert(0, event)
			# If the selected day occurs during an event, highlight it. We
			# append it to the list of events to be highlighted, so it'll only
			# be highlighted if no event actually starts on that day.
			elif (day_start > event_start and day_start < event_end) or \
                 (day_end > event_start and day_end < event_end) or \
                 (event_start > day_start and event_end < day_end): 
				highlight_events.append(event)

		# Highlight the first event on the day the user selected, unless the
		# user manually selected an event.
		if not self.__stop_auto_highlight:
			if highlight_events and highlight_events[0] in self.treeview_event:
				self.__stop_auto_dayjump = True
				self.treeview_event.select(highlight_events[0], True)
				self.__stop_auto_dayjump = False
			else:
				self.treeview_event.unselect_all()
			
	def on_combobox_display_range__changed(self, *args):
		# Get the currently selected date in the calendar.
		sel_date = self.calendar.get_date()
		sel_dt_start = datetime.datetime(sel_date[0], sel_date[1]+1, sel_date[2])
		sel_dt_end = sel_dt_start + datetime.timedelta(days=+1)

		# Determine the start and end of the period that needs to be shown.
		display_range = self.combobox_display_range.get_active_text()
		if display_range == 'Day':
			display_start = sel_dt_start 
			display_end = display_start + datetime.timedelta(days=+1, seconds=-1)
			text = '%s' % (display_start.strftime('%a %b %d %Y'))
		elif display_range == 'Week':
			display_start = sel_dt_start + datetime.timedelta(days=-sel_dt_start.weekday())
			display_end = display_start + datetime.timedelta(weeks=+1, seconds=-1)
			text = '%s - %s' % (display_start.strftime('%a %b %d %Y'), display_end.strftime('%a %b %d %Y'))
		elif display_range == 'Month':
			display_start = sel_dt_start + datetime.timedelta(days=-(sel_dt_start.day - 1))
			display_end = display_start + relativedelta(months=+1, seconds=-1)
			text = '%s' % (display_start.strftime('%b %Y'))
		elif display_range == 'Year':
			display_start = datetime.datetime(sel_dt_start.year, 1, 1)
			display_end = display_start + relativedelta(years=+1, seconds=-1)
			text = '%s' % (display_start.strftime('%Y'))
		else:
			raise Exception('No selected display range!')
			
		# Update the displayed range
		self.displayed_range.set_text(text)

		self.display_start = display_start
		self.display_end = display_end

		self.treeview_event__update()

	def treeview_event__update(self):
		if self.__stop_auto_treeview_update:
			return

		# First, remove all the recurring events, because they're generated on
		# the fly, so we can't know which ones in the list we need to remove.
		# Therefor we remove them every time.
		events_rm = []
		for event in self.treeview_event:
			if hasattr(event, 'real_event'):
				events_rm.append(event)
		for event in events_rm:
			self.treeview_event.remove(event)

		# Add the events for the displayed range to the list
		events = self.mo.getEvents() + self.mo.getRecurEvents(self.display_start, self.display_end)
		for event in events:
			event_start = event.get_start()
			event_end = event.get_end()

			# If the currently displayed range includes an event, add it to the list.
			if (self.display_start >= event_start and self.display_start < event_end) or \
               (self.display_end >= event_start and self.display_end < event_end) or \
               (event_start >= self.display_start and event_end < self.display_end):
				if not event in self.treeview_event:
					self.treeview_event.append(None, event)
			# Otherwise, we remove it from the list, if it's present.
			else:
				if event in self.treeview_event:
					self.treeview_event.remove(event)
		
	def treeview_event__row_activated(self, list, object):
		sel_event = self.treeview_event.get_selected()
		sel_event = getattr(sel_event, 'real_event', sel_event) # Edit real event instead of recurring event
		miniorganizer.ui.EventEditUI(self.mo, sel_event)
		self.on_calendar__month_changed(self.calendar)
		self.on_calendar__day_selected(self.calendar)
		if sel_event in self.treeview_event:
			self.treeview_event.select(sel_event, True)
		self.parent.menuitem_save.set_sensitive(True)

	def treeview_event__selection_changed(self, list, selection):
		# Stop the treeview from automatically updating itself because that
		# will remove the recurring events and regenerate them (with different
		# instance IDs) which means the selection may be invalid.
		self.__stop_auto_treeview_update = True

		sel_event = self.treeview_event.get_selected()
		has_selection = sel_event is not None

		# Enable / disable toolbuttons
		self.toolbutton_remove.set_sensitive(has_selection)
		self.toolbutton_edit.set_sensitive(has_selection)

		# Do not jump to the day of the event. This is needed because an event
		# can be automatically selected even if it doesn't start on a
		# particular day.
		if self.__stop_auto_dayjump:
			self.__stop_auto_treeview_update = False
			return

		# Stop this selection from being overwritten.
		self.__stop_auto_highlight = True

		if has_selection:
			# Make the calendar jump to the day on which this event begins.
			sel_event_start = sel_event.get_start()
			self.calendar.select_month(sel_event_start.month - 1, sel_event_start.year)
			self.calendar.select_day(sel_event_start.day)

		# Enable automatic highlighting of items
		self.__stop_auto_highlight = False
		self.__stop_auto_treeview_update = False
	
	def treeview_event__key_press_event(self, treeview, event):
		if event.keyval == gtk.keysyms.Delete:
			self.on_toolbutton_remove__clicked()
