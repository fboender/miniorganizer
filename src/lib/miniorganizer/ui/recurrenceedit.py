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
import miniorganizer.models
from kiwi.ui.delegates import GladeDelegate
import icalendar
import re

import pdb

weekdays = ['MO', 'TU', 'WE', 'TH', 'FI', 'SA', 'SU']

class RecurrenceEditUI(GladeDelegate):

	def __init__(self, mo, recur):
		self.mo = mo
		self.recur = recur

		GladeDelegate.__init__(self, gladefile="mo_recurrence_edit", toplevel_name='dialog_main')

		self.on_radio_daily__toggled(self.radio_daily)
		self.combobox_monthly_recur_mday.set_active(0)
		self.combobox_monthly_recur_week_nr.set_active(0)
		self.combobox_monthly_recur_week_day.set_active(0)
		self.combobox_yearly_recur_dom_month.set_active(0)
		self.combobox_yearly_recur_wom_nr.set_active(0)
		self.combobox_yearly_recur_wom_dow.set_active(0)
		self.combobox_yearly_recur_wom_month.set_active(0)

		if recur and 'FREQ' in recur:

			# Recurs daily
			if recur['FREQ'] == ['DAILY']:
				self.on_radio_daily__toggled(self.radio_daily)
				if 'INTERVAL' in recur:
					# Recurs every .. day
					self.spinbutton_daily_interval.set_value(recur['INTERVAL'][0])

			# Recurs weekly
			elif recur['FREQ'] == ['WEEKLY']:
				self.radio_weekly.set_active(True)
				if 'INTERVAL' in recur:
					# Recurs every .. week
					self.spinbutton_weekly_interval.set_value(recur['INTERVAL'][0])

				# Recurs on which weekdays?
				if 'BYDAY' in recur:
					if 'MO' in recur['BYDAY']: self.checkbutton_weekly_mon.set_active(True)
					if 'TU' in recur['BYDAY']: self.checkbutton_weekly_tue.set_active(True)
					if 'WE' in recur['BYDAY']: self.checkbutton_weekly_wed.set_active(True)
					if 'TH' in recur['BYDAY']: self.checkbutton_weekly_thu.set_active(True)
					if 'FR' in recur['BYDAY']: self.checkbutton_weekly_fri.set_active(True)
					if 'SA' in recur['BYDAY']: self.checkbutton_weekly_sat.set_active(True)
					if 'SU' in recur['BYDAY']: self.checkbutton_weekly_sun.set_active(True)

			# Recurs monthly
			elif recur['FREQ'] == ['MONTHLY']:
				self.radio_monthly.set_active(True)
				if 'INTERVAL' in recur:
					# Recurs every .. months
					self.spinbutton_monthly_interval.set_value(recur['INTERVAL'][0])

				if 'BYMONTHDAY' in recur:
					# Recurs on the .. day of the month
					self.radiobutton_monthly_recur_mday.set_active(True)
					bmd_index = recur['BYMONTHDAY'][0] - 1
					if bmd_index < 0:
						bmd_index = 29 - bmd_index
					self.combobox_monthly_recur_mday.set_active(bmd_index)
				elif 'BYDAY' in recur:
					# Recurs on the .. weekday in the month (e.g. second tuesday)
					self.radiobutton_monthly_recur_week.set_active(True)
					m = re.match('(-?\d+)(.*)', recur['BYDAY'][0])
					bd_index = int(m.groups()[0]) - 1
					if bd_index < 0:
						bd_index = 3 - bd_index
					wd_index = weekdays.index(m.groups()[1])
					self.combobox_monthly_recur_week_nr.set_active(bd_index)
					self.combobox_monthly_recur_week_day.set_active(wd_index)

			# Recurs yearly
			elif recur['FREQ'] == ['YEARLY']:
				self.radio_yearly.set_active(True)
				if 'INTERVAL' in recur:
					self.spinbutton_yearly_interval.set_value(recur['INTERVAL'][0])

				if 'BYMONTHDAY' in recur and 'BYMONTH' in recur:
					# Recurs on the .. day of month ..
					self.radiobutton_yearly_recur_dom.set_active(True)
					self.spinbutton_yearly_recur_dom_nr.set_value(recur['BYMONTHDAY'][0])
					self.combobox_yearly_recur_dom_month.set_active(recur['BYMONTH'][0] - 1)
					pass
				elif 'BYDAY' in recur and 'BYMONTH' in recur:
					# Recurs on ..nd weekday of month ..
					self.radiobutton_yearly_recur_wom.set_active(True)
					m = re.match('(-?\d+)(.*)', recur['BYDAY'][0])
					bd_index = int(m.groups()[0]) - 1
					if bd_index < 0:
						bd_index = 3 - bd_index
					wd_index = weekdays.index(m.groups()[1])
					self.combobox_yearly_recur_wom_nr.set_active(bd_index)
					self.combobox_yearly_recur_wom_dow.set_active(wd_index)
					self.combobox_yearly_recur_wom_month.set_active(recur['BYMONTH'][0] - 1)
				elif 'BYYEARDAY' in recur:
					self.radiobutton_yearly_recur_doy.set_active(True)
					self.spinbutton_yearly_recur_doy_nr.set_value(recur['BYYEARDAY'][0])

	def run(self):
		self.show_all()
		gtk.main()
		return(self.recur)
		
	def on_radio_once__toggled(self, radiobutton):
		pass

	def on_radio_daily__toggled(self, radiobutton):
		state = radiobutton.get_active()
		self.alignment_daily.set_sensitive(state)

	def on_radio_weekly__toggled(self, radiobutton):
		state = radiobutton.get_active()
		self.alignment_weekly.set_sensitive(state)

	def on_radio_monthly__toggled(self, radiobutton):
		state = radiobutton.get_active()
		self.alignment_monthly.set_sensitive(state)

	def on_radio_yearly__toggled(self, radiobutton):
		state = radiobutton.get_active()
		self.alignment_yearly.set_sensitive(state)

	def on_button_ok__clicked(self, *args):
		new_recur = icalendar.vRecur()
		if self.radio_once.get_active():
			new_recur = {}
		elif self.radio_daily.get_active():
			new_recur['FREQ'] = ['DAILY']
			new_recur['INTERVAL'] = [self.spinbutton_daily_interval.get_value()]
		elif self.radio_weekly.get_active():
			new_recur['FREQ'] = ['WEEKLY']
			new_recur['INTERVAL'] = [self.spinbutton_weekly_interval.get_value()]
			byday = []
			if self.checkbutton_weekly_mon.get_active(): byday.append('MO')
			if self.checkbutton_weekly_tue.get_active(): byday.append('TU')
			if self.checkbutton_weekly_wed.get_active(): byday.append('WE')
			if self.checkbutton_weekly_thu.get_active(): byday.append('TH')
			if self.checkbutton_weekly_fri.get_active(): byday.append('FR')
			if self.checkbutton_weekly_sat.get_active(): byday.append('SA')
			if self.checkbutton_weekly_sun.get_active(): byday.append('SU')
			if byday:
				new_recur['BYDAY'] = byday
		elif self.radio_monthly.get_active():
			new_recur['FREQ'] = ['MONTHLY']
			new_recur['INTERVAL'] = [self.spinbutton_monthly_interval.get_value()]
			if self.radiobutton_monthly_recur_mday.get_active():
				bmd_index = self.combobox_monthly_recur_mday.get_active()
				if bmd_index > 30:
					bmd_index = 29 - bmd_index
				bmd_index += 1
				new_recur['BYMONTHDAY'] = [bmd_index]
			elif self.radiobutton_monthly_recur_week.get_active():
				bd_index = self.combobox_monthly_recur_week_nr.get_active()
				if bd_index > 4:
					bd_index = 3 - bd_index
				bd_index += 1
				wd_index = self.combobox_monthly_recur_week_day.get_active()
				new_recur['BYDAY'] = ['%i%s' % (bd_index, weekdays[wd_index])]
		elif self.radio_yearly.get_active():
			new_recur['FREQ'] = ['YEARLY']
			new_recur['INTERVAL'] = [self.spinbutton_yearly_interval.get_value()]
			if self.radiobutton_yearly_recur_dom.get_active():
				new_recur['BYMONTHDAY'] = [self.spinbutton_yearly_recur_dom_nr.get_value()]
				new_recur['BYMONTH'] = [self.combobox_yearly_recur_dom_month.get_active() + 1]
			elif self.radiobutton_yearly_recur_wom.get_active():
				bd_index = self.combobox_yearly_recur_wom_nr.get_active()
				if bd_index > 4:
					bd_index = 3 - bd_index
				bd_index += 1
				dow_index = self.combobox_yearly_recur_wom_dow.get_active()
				new_recur['BYDAY'] = ['%i%s' % (bd_index, weekdays[dow_index])]
				new_recur['BYMONTH'] = [self.combobox_yearly_recur_wom_month.get_active() + 1]
			elif self.radiobutton_yearly_recur_doy.get_active():
				new_recur['BYYEARDAY'] = [self.spinbutton_yearly_recur_doy_nr.get_value()]
		self.recur = new_recur
		self.quit()

	def on_button_cancel__clicked(self, *args):
		self.recur = None
		self.quit()

	def quit(self):
		self.view.hide()
		gtk.main_quit()

