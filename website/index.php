<?php

error_reporting(E_ALL);

$menu = array(
	"home" => "Home",
	"about" => "About",
	"news" => "News",
	"download" => "Download",
	"screenshots" => "Screenshots"
);

// Client side vars
$page = 'home';
if (array_key_exists('page', $_GET)) {
	$page = $_GET['page'];
} 

// Check if the $page is in $menu
if (!array_key_exists($page, $menu)) {
	print("ERROR");
	exit;
}
?>
<html>
	<head>
		<link href="css/index.css" rel="stylesheet" type="text/css">
	</head>
	<body>
		<div id='header'>
			<div id='header_logo_img'>
				<img src='images/logo_img.png' alt='' />
			</div>
			<div id='header_logo_text'>
				<img src='images/logo_text.png' alt='MINIORGANIZER: The no-nonsense personal digital assistant.' />
			</div>
		</div>
		<div id='menu'>
			<div id='menu_l'>
			</div>
			<div id='menu_r'>
			</div>
			<div id='menu_c'>
				<?php
				$menuItems = array();
				foreach ($menu as $item => $title) {
					$menuItems[] = '<a href="?page='.$item.'">'.$title.'</a>';
				}
				$menu = implode("<img  class='menu_sep' src='images/menu_sep.png' alt='|' />", $menuItems);
				print ($menu);
				?>
			</div>
		</div>
		<div id='contents'>
			<?php
			include('pages/'.$page.'.php');
			?>
		</div>
		<div id='footer'>
		</div>
	</body>
</html>
