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

# Main interface
from main import MiniOrganizerUI

# Dialogs
from about import AboutUI
from reminder import ReminderUI

# Tabs
from event import EventUI
from todo import TodoUI
from notes import NotesUI

# Edit dialogs
from eventedit import EventEditUI
from todoedit import TodoEditUI
from alarmedit import AlarmEditUI
from alarmsedit import AlarmsEditUI
from recurrenceedit import RecurrenceEditUI
from datetimeedit import DateTimeEditUI

# Misc dialogs
from error import ErrorUI

# Because we don't want to polute the namespace with stuff, delete some things
# here.
del main, about, reminder, event, todo, notes, eventedit, todoedit
del alarmedit, alarmsedit, recurrenceedit, datetimeedit, error
