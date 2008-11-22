<script language='javascript'>
	function change_scr(version, link, img) {
		e_link = document.getElementById('scr_link');
		e_img = document.getElementById('scr_img');
		e_link.href = 'screenshots/'+version+'/' + link;
		e_img.src = 'screenshots/'+version+'/' + img;
	}
</script>

<div id='sidebar'>
	<h2>Download</h2>
	<div id='download'>
		<a href='/releases/miniorganizer-0.3.1.tar.gz'>Release 0.3.1</a>
	</div>

	<h2>Screenshots</h2>
	<div id='screenshots'>
		<a class='tab' href='#' onClick='change_scr("0.1", "calendar.png", "th_calendar.png");'>Calendar</a>
		<a class='tab' href='#' onClick='change_scr("0.1", "todo.png", "th_todo.png");'>Todo</a>
		<a class='tab' href='#' onClick='change_scr("0.1", "notes.png", "th_notes.png");'>Notes</a>
		<a id='scr_link' href='screenshots/0.1/calendar.png'><img id='scr_img' src='screenshots/0.1/th_calendar.png' border='0' /></a>
		<a href='?page=screenshots'>More screenshots &rarr;</a>
	</div>
</div>

<h1>Home</h1>

<h2>About</h2>
<p>MiniOrganizer is a small no-nonsense personal digital organizer written in GTK2, featuring appointments, todos and notes. It uses iCalendar files as its native backend, supports multiple alarms per appointment/todo and has recursive todos.</p>
<p><a href='?page=about'>More information &rarr;</a></p>

<h2>News</h2>
<h3>Sat Nov 22 14:36:08 CET 2008</h3>
<p>Anonymous users can now add comments and patches to <a href="https://svn.electricmonk.nl/trac/miniorganizer/report/1">Bug reports</a>.</p>
<p>In other news, MiniOrganizer 0.3.1 has been prepared to work under OpenBSD. Many thanks to Michiel van Baak for this and various other patches.</p>
<h3>Sat Nov 22 12:00:21 CET 2008</h3>
<p>Version <a href="?page=download">0.3.1</a> is now available! Features and bugfixes include:</p>
<ul>
	<li>Feature added: Manual pages.</li>
	<li>Bug fixed: Installer now checks for all required dependencies.</li>
	<li>Bug fixed: OpenBSD support.</li>
	<li>Bug fixed: Manual updated.</li>
	<li>Bug fixed: Some debugging functions fixed.</li>
	<li>Bug fixed: A bug that occurred when ampersands where included in various input boxes has been fixed.</li>
	<li>Bug fixed: The 'Triggers on' display when editing an alarm has been fixed. It now shows the correct trigger date/time.</li>
	<li>Bug fixed: When canceling a new appointment/todo/note using the window's little X (close) icon, the new appointment/todo/note is no longer added.</li>
	<li>Bug fixed: A new calendar is now automatically created upon first start of MiniOrganizer.</li>
	<li>Bug fixed: Opening a different calendar now correctly refreshes the Todo and Notes tab.</li>
	<li>Other fix: The license was changed from "GPL v3 or later" to "GPL v3".</li>
</ul>

<h3>Wed Nov 12 22:06:33 CEST 2008</h3>
<p>Version <a href="?page=download">0.3</a>! Features and bugfixes include:</p>
<ul>
	<li>Feature added: Rudimentary notes.</li>
	<li>Bug fixed: Multi-line pieces of text with newlines are now properly read and written from calendar files.</li>
	<li>Bug fixed: After loading a different calendar, changes to that calendar are now saved to the correct calendar.</li>
	<li>Bug fixed: Alarms for recurring events are now alerted for.</li>
	<li>Bug fixed: Loading a different calendar now works correctly.</li>
</ul>
<p><a href='?page=news'>More news &rarr;</a></p>
