<h1>About</h1>

<h2>General</h2>
<p>MiniOrganizer is a small no-nonsense personal digital organizer written in
GTK2, featuring appointments, todos and notes. It uses iCalendar files as its
native back-end, supports multiple alarms per appointment/todo and has recursive
todos.</p>

<h2>Features</h2>
<p>MiniOrganizer currently features:</p>
<ul>
<li> <p> Appointments.  </p> </li>
<li> <p> Hierarchical Todos.  </p> </li>
<li> <p> Multiple alarms per appointment and todo.  </p> </li>
<li> <p> Alarm notification.  </p> </li>
<li> <p> (Gnome) Panel docking.  </p> </li>
</ul>

<h2>Intended features</h2>
<p>Here's a list of features that are intended to be implemented in MiniOrganizer,
just to give you an idea of where this thing is supposed to be heading:</p>
<ul>
<li> <p> Notes (Wiki-like, Recursive and WYSIWYG editing with headings, etc) </p> </li>
<li> <p> Linking Appointments, Todos and Notes.  </p> </li>
<li> <p> Sending and receiving of appointment requests.  </p> </li>
<li> <p> Scanning a local and/or remote mailbox for appointment requests (MS Outlook 'integration').  </p> </li>
<li> <p> Syncing with OpenSync servers </p> </li>
<li> <p> Various additional personal planning features.  </p> </li>
</ul>

<h2>Installation</h2>
<h3>Requirements</h3>
<p>MiniOrganizer requires the following software in order to run properly:</p>
<ul>
<li> <p> Python (v2.4+) (<a href="http://python.org/download/">http://python.org/download/</a>) </p> </li>
<li> <p> Python GTK-2 bindings (<a href="http://www.pygtk.org/downloads.html">http://www.pygtk.org/downloads.html</a>) </p> </li>
<li> <p> Python DateUtil </p> </li>
<li> <p> Python Glade2 </p> </li>
</ul>

<h3>Instructions - Ubuntu / Debian</h3>

<p>In order to install MiniOrganizer on an Ubuntu or Debian system, follow these steps:</p>
<p>Python should already be installed on your system. If you're using a reasonably up-to-date system, it should also be the correct version (v2.4 or higher). So the first thing to do is install the required Python libraries.</p>
<p>Use your package manager to install the following Ubuntu/Debian packages:</p>
<ul>
<li> <p> python-gtk2 </p> </li>
<li> <p> python-glade2 </p> </li>
<li> <p> python-dateutil </p> </li>
</ul>
<p>For the commandline based Aptitude, this would be:</p>
<pre>sudo aptitude install python-gtk2 python-glade2 python-dateutil</pre>
<p>Now follow the general instructions mentioned below.</p>
<h3>Instructions - General</h3>
<p>Now download the MiniOrganizer tarball from the MiniOrganizer homepage and unpack it using your archive manager. For the commandline:</p>
<pre>tar -vxzf miniorganizer-0.1.tar.gz</pre>
<p>Change to the unarchived directory, and run <em>setup.sh</em>:</p>
<pre>cd miniorganizer-0.1/
./setup.sh</pre>
<p>This will install MiniOrganizer in the <em>/usr/local/share/miniorganizer</em>
directory. Links to the binaries will be installed in <em>/usr/local/bin/</em>.</p>

<h2>Legal</h2>
<p><em>MiniOrganizer</em> is Copyright 2008 by Ferry Boender and is released under the
GNU General Public License v3 or higher. See the LICENSE file for more
information.</p>
<p><em>Kiwi</em>, which is distributed with MiniOrganizer, is Copyright 2003-2006 by
Async Open Source and is released under the GNU Lesser General Public License
v2.1 or higher. See the lib/kiwi/LICENSE.txt file for more information.</p>
<p><em>iCalendar</em>, which is distributed with MiniOrganizer, is Copyright 2008 by Max
M et al and is released under the GNU Lesser General Public License v2.1. See
lib/icalendar/LICENSE.txt for more information.</p>
