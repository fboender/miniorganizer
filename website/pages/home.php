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
		<a href='/releases/miniorganizer-%%VERSION%%.tar.gz'>Release %%VERSION%%</a>
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
<h3>Wed Nov 12 22:06:33 CEST 2008</h3>
<p>Version <a href="/download">0.3</a>! Features and bugfixes include:</p>
<ul>
	<li>Feature added: Rudimentary notes.</li>
	<li>Bug fixed: Multi-line pieces of text with newlines are now properly read and written from calendar files.</li>
	<li>Bug fixed: After loading a different calendar, changes to that calendar are now saved to the correct calendar.</li>
	<li>Bug fixed: Alarms for recurring events are now alerted for.</li>
	<li>Bug fixed: Loading a different calendar now works correctly.</li>
</ul>

<h3>Tue Oct 14 20:32:08 CEST 2008</h3>
<p>Version <a href="/download">0.2.1</a> released! This is a bugfix release for v0.2 with the following fixes:</p>
<ul>
	<li>Bug fixed: Adding/modifying a todo now shows the Todo Editor again.</li>
	<li>Bug fixed: Removing a todo with no sub-todos no longer complains about sub-todos which will be deleted.</li>
</ul>

<h3>Sat Oct 11 18:39:41 CEST 2008</h3>
<p>Version <a href="/download">0.2</a> has been released. Changes in this release include:</p>
<ul>
	<li>Bug fixed: The alarm notifier would sometimes display alarms multiple times.</li>
	<li>Bug fixed: Various dialog resize problems were fixed.</li>
	<li>Bug fixed: Various problems with the installer script were fixed.</li>
	<li>Bug fixed: When hitting 'Cancel' in the event add or alarm edit dialog, the event and alarm would still be added/changed. This has been fixed.</li>
	<li>Feature added: Locations for events.</li>
	<li>Feature added: Icalendar files can now be imported using the File - Import menu, or the <tt>-i</tt> commandline switch.</li>
	<li>Feature added: File menu items (save, save as) now work.</li>
	<li>Feature added: Delete key now removes selected events and todos from the list.</li>
	<li>Feature added: Recurring events can now be added.</li>
	<li>Feature added: The installer script now installs a desktop entry and an automatic start entry for Gnome.</li>
	<li>Feature added: The alarm notification pop-up will now appear above all the other windows and on all the desktops if your window manager supports it.</li>
	<li>Feature added: Double-clicking on a day in the calander will add a new event for that day.</li>
</ul>
<h3>Mon Jun 23 16:37:19 CEST 2008</h3>
<p>Version 0.1 of MiniOrganizer is out! This is the first released version, so there will probably be some installation and other bugs in it. Please try it out and let me know what you think. You can mail me at <tt>ferry DOT boender (@) gmail . com</tt>.</p>
<p><a href='?page=news'>More news &rarr;</a></p>
