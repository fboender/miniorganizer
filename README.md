MiniOrganizer
=============

![Activity: Abandoned](https://img.shields.io/badge/activity-abandoned-red.svg)


About
-----

MiniOrganizer is a small no-nonsense personal digital organizer written in
GTK2, featuring appointments, todos and notes. It uses iCalendar files as its
native back-end, supports multiple alarms per appointment/todo and has
recursive todos.

### Features

*   One-time and recurring appointments.
*   Hierarchical Todos.
*   Multiple alarms per appointment and todo.
*   Basic notes.
*   Alarm notification with snooze.
*   (Gnome) Panel docking.
*   Uses universal iCalendar files as storage format.

### Screenshots

You can find some screenshots here:

* [Calendar](https://raw.githubusercontent.com/fboender/miniorganizer/master/docs/screenshots/calendar.png)
* [Calendar Add](https://raw.githubusercontent.com/fboender/miniorganizer/master/docs/screenshots/calendar_add.png)
* [Todo](https://raw.githubusercontent.com/fboender/miniorganizer/master/docs/screenshots/todo.png)
* [Todo Add](https://raw.githubusercontent.com/fboender/miniorganizer/master/docs/screenshots/todo_add.png)

Installation
------------

### Requirements

MiniOrganizer requires the following software in order to run properly:

*   [Python (v2.4+)](http://python.org/download/)
*   [Python GTK-2 bindings](http://www.pygtk.org/downloads.html)
*   Python DateUtil
*   Python Glade2

Most modern Linux/BSD desktops (Debian, Ubuntu, OpenBSD confirmed) usually have
binary packages for these dependencies, allowing for easy installation on those
platforms.

For Debian-based systems (Debian, Ubuntu, Mint):

    sudo aptitude install python-gtk2 python-glade2 python-dateutil

For OpenBSD:

    sudo pkg_add py-gobject py-gtk2 py-dateutil

Next, unpack the archive:

    tar -vxzf miniorganizer-*.tar.gz

Change to the unarchived directory and run setup.sh:

    cd miniorganizer-*/
    ./setup.sh

This will install MiniOrganizer in the /usr/local/share/miniorganizer
directory. Links to the binaries will be installed in /usr/local/bin/.

Usage
-----

MiniOrganizer comes with two programs:

*   *miniorganizer*, which is the graphical frontend.
*   *miniorganizer-alarm*, which is the alarm notifier that sits in your dock.

### MiniOrganizer

MiniOrganizer (The miniorganizer executable) is the main MiniOrganizer
interface. Running it will start MiniOrganizer, which will show you the
Appointment/Todo/Notes interface.

Commandline options:

    Usage: ./miniorganizer [option] [ICAL]

    Small no-nonsense personal digital assistant

    Options:
      --version             show program's version number and exit
      -h, --help            show this help message and exit
      -i FILE, --import=FILE
                            Import FILE into the calendar.
      -d DEBUG, --debug=DEBUG
                            Debug level (1-50).

### MiniOrganizer Alarm Notifer

The MiniOrganizer Alarm daemon (The miniorganizer-daemon executable) is the
MiniOrganizer alarm notifier. When run, it docks in your desktop's notification
area and shows alerts when an appointment or todo's alarm goes off. Clicking
the icon in the notification area of your desktop will launch the main
MiniOrganizer interface.

The MiniOrganizer Alarm daemon currently only alerts for a single Icalendar
file, namely the .miniorganizer/miniorganizer.ics in your home directory.

    Usage: miniorganizer-alarm [option]

    Options:
      -h, --help            show this help message and exit
      -d DEBUG, --debug=DEBUG
                            Debug level (1-50).

Legal
-----

MiniOrganizer is Copyright 2008 by Ferry Boender et al (see Copyright section)
and is released under the GNU General Public License v3. See the LICENSE file
for more information.

Kiwi, which is distributed with MiniOrganizer, is Copyright 2003-2006 by Async
Open Source and is released under the GNU Lesser General Public License v2.1 or
higher. See the lib/kiwi/LICENSE.txt file for more information.

iCalendar, which is distributed with MiniOrganizer, is Copyright 2008 by Max M
et al and is released under the GNU Lesser General Public License v2.1. See
lib/icalendar/LICENSE.txt for more information.

MiniOrganizer contains code and contributions (and is thus copyright) by the
following persons:

*   Ferry Boender

*   Michiel van Baak
