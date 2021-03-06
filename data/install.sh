#!/bin/sh

INSTALLDIR='/usr/local/lib/miniorganizer'
BINDIR='/usr/local/bin'
MANDIR='/usr/local/man'
MENUDIR='/usr/local/share/applications/'

#
# Do some checks to make sure we can install Miniorganizer on the system and
# actually run it.
#
if [ ! -d 'bin' -o ! -d 'docs' ]; then
	echo "'bin' or 'docs' directory does not exist. Can't install. Aborting..."
	exit 1
fi

if [ `whoami` != 'root' ]; then
	echo "You are not root. Aborting..."
	exit 2
fi

python -c "import dateutil" 2>/dev/null
if [ "$?" -eq '1' ]; then
	echo "You don't have the python package 'dateutil' installed. Please install it."
	exit 3
fi

python -c "import gobject" 2>/dev/null
if [ "$?" -eq '1' ]; then
	echo "You don't have the python package 'gobject' installed. Please insall it."
	exit 3
fi

python -c "import gtk" 2>/dev/null
if [ "$?" -eq '1' ]; then
	echo "You don't have the python package 'gtk' installed. Please install it."
	exit 3
fi

#
# Install Miniorganizer
#
echo "Installing MiniOrganizer in $INSTALLDIR"
mkdir -p $INSTALLDIR
mkdir -p $MANDIR/man1
cp -r bin $INSTALLDIR
cp -r docs/userguide.html $INSTALLDIR
cp -r docs/man/* $MANDIR/man1
chmod 755 $INSTALLDIR/bin/miniorganizer
chmod 755 $INSTALLDIR/bin/miniorganizer-alarm

echo "Putting executable symlink in $BINDIR"
rm $BINDIR/miniorganizer 2>/dev/null
rm $BINDIR/miniorganizer-alarm 2>/dev/null
ln -s $INSTALLDIR/bin/miniorganizer $BINDIR/miniorganizer
ln -s $INSTALLDIR/bin/miniorganizer-alarm $BINDIR/miniorganizer-alarm

if [ -d "$MENUDIR" ]; then
	echo "Installing desktop menu icon"
	cp desktop/miniorganizer.desktop $MENUDIR
fi

echo "--"
echo
echo "MiniOrganizer succesfully installed. Run with 'miniorganizer' on the"
echo "commandline. Run 'miniorganizer-alarm' to start the Alarm notifier. If you are"
echo "running a recent GNOME desktop, you can copy the"
echo "'desktop/miniorganizer-alarm.desktop' file to your '~/.config/autostart/'"
echo "directory to have the Alarm notifier start automatically."
