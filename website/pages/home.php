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
		<a href='/releases/miniorganizer-0.1.tar.gz'>Release 0.1</a>
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
<h3>Mon Jun 23 16:37:19 CEST 2008</h3>
<p>Version 0.1 of MiniOrganizer is out! This is the first released version, so there will probably be some installation and other bugs in it. Please try it out and let me know what you think. You can mail me at <tt>ferry DOT boender (@) gmail . com</tt>.</p>
<p><a href='?page=news'>More news &rarr;</a></p>
