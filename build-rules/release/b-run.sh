#!/bin/sh

VERSION=$1

if [ -z $VERSION ]; then
	echo "Version required for this build rule" >&2
	exit
fi

if [ -d 'releases' ]; then
	rm -rf releases
fi

# Create the release directory structure.
mkdir releases
mkdir releases/miniorganizer-$VERSION
mkdir releases/miniorganizer-$VERSION/docs
mkdir releases/miniorganizer-$VERSION/man
mkdir releases/miniorganizer-$VERSION/bin
mkdir releases/miniorganizer-$VERSION/desktop

# Copy the source to the release directory structure.
cp src/* releases/miniorganizer-$VERSION/bin/ -ar
cp data/install.sh releases/miniorganizer-$VERSION/ 
cp data/uninstall.sh releases/miniorganizer-$VERSION/ 
cp docs/userguide/userguide.html releases/miniorganizer-$VERSION/docs/
cp -r docs/manpages/man1 releases/miniorganizer-$VERSION/docs/man
cp data/desktop/miniorganizer.desktop releases/miniorganizer-$VERSION/desktop
cp data/desktop/miniorganizer-alarm.desktop releases/miniorganizer-$VERSION/desktop

# Remove unneeded stuff from the release dir
find ./releases/miniorganizer-$VERSION/ -name ".svn" -type d -print0 | xargs -0 /bin/rm -rf
find ./releases/miniorganizer-$VERSION/ -name "*.pyc" -type f -print0 | xargs -0 /bin/rm -rf

# Version bump
replace.py ./releases/miniorganizer-$VERSION/ %%VERSION%% $VERSION

cd releases
tar -czf miniorganizer-$VERSION.tar.gz miniorganizer-$VERSION/
cd ..

rm -rf releases/miniorganizer-$VERSION
