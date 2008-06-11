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
		<a href='?page=download'>Coming Soon</a>
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
<p>No news yet</p>
<!--
<h3>Fri May 16 2008</h3>
<p>Released version 0.1. This is kind of a pre-release, and so it might still be a little rough around the edges, since there hasn't been any user feedback so far. Please report any installation and configuration problems, as well as User Interface issues, feature requests or anything else that's on your mind!</p>
<p><a href='?page=news'>More news &rarr;</a></p>
-->
<p><a href='?page=news'>More news &rarr;</a></p>
