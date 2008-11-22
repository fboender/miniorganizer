#!/bin/sh

INSTALLDIR='/usr/local/lib/miniorganizer'
BINDIR='/usr/local/bin'
MANDIR='/usr/local/man'
MENUDIR='/usr/local/share/applications/'

if [ `whoami` != 'root' ]; then
	echo "You are not root. Aborting..."
	exit 2
fi

echo "Removing MiniOrganizer"
rm -rf $INSTALLDIR 2>/dev/null
rm $BINDIR/miniorganizer 2>/dev/null
rm $BINDIR/miniorganizer-alarm 2>/dev/null
rm $MENUDIR/miniorganizer.desktop 2>/dev/null
rm $MANDIR/man1/miniorganizer*
