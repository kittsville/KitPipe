#!python3
'''
Name:           KitPipe
Description:    A crappy little assets minifier I created to make minifying WP-Librarian assets easier
Author:         Kittsville
Contact:        kittsville [at] gmail.com
Python:         2.7.9
License:        GPL2
'''

from __future__ import print_function   # To make it easier for people who get Slimit working on Python 3
from cssmin import cssmin               # For CSS
from slimit import minify               # For JS
import os                               # For file/directory interaction
import hashlib                          # Checking if a file has changed
import sys                              # For quitting

# Holds shared minifying logic for JS/CSS assets
class Asset:
    # Generates checksum of file contents
    def genChecksum(self):
        # Generates checksum of file and returns first 128 bits
        return hashlib.sha256(open(self.file, 'rb').read()).digest()[:16]
    
    # Checks if the asset has been changed since the script last looked at it
    # Updates checksum if file has been modified
    def changed(self):
        newChecksum = self.genChecksum()
        
        if newChecksum == self.checksum:
            return False
        else:
            self.checksum = newChecksum
            return True
    
    # Minifies asset if file has changed since check
    def minifyIfChanged(self):
        if self.changed():
            self.saveMinified(self.minify())
            return True
        else:
            return False
    
    # Saves minified JS/CSS
    def saveMinified(self, minifiedAsset):
        with open(self.minFile, 'w+') as minFile:
            print(minifiedAsset, file=minFile)
    
    def __init__(self, name, directory):
        self.file       = os.path.join(directory, name)         # Full path to file
        
        # Because I don't trust you misusing this class
        if not os.path.isfile(self.file):
            sys.exit('This ain\'t an asset: ' + self.file)
        
        fileParts       = os.path.splitext(self.file)
        self.minFile    = fileParts[0] + '.min' + fileParts[1]  # Path to minified version of asset
        self.checksum   = self.genChecksum()
        self.name       = name                                  # File name (end of path) e.g. derp.js
        
        print('Loaded ' + name)

class JSAsset(Asset):
    # Generates and returns minified version of JS asset
    def minify(self):
        return minify(open(self.file, 'r').read(), mangle=True)

class CSSAsset(Asset):
    # Generates and returns minified version of CSS asset
    def minify(self):
        return cssmin(open(self.file, 'r').read())

# ==========
# Step 1: Load directories
# ==========
print('==========\nLoading Directories\n==========')

watchedDirectories = []

directoryConfigPath = os.path.realpath('directories.txt')

if os.path.exists(directoryConfigPath):
    with open(directoryConfigPath, 'r') as directoryConfigFile:
        for directory in directoryConfigFile:
            directory = directory.strip()
            
            # Ignores commented lines
            if directory.startswith("#"):
                continue
            
            # Standardises '/' '\' differences
            directory = directory.replace('\\', '/')
            
            # Fixes directories missing a trailing slash
            if not directory.endswith('/'):
                directory += '/'
            
            directory = os.path.dirname(directory)
            
            # Adds directory if it exists and has not already been added, informs user if otherwise
            if os.path.isdir(directory):
                if directory not in watchedDirectories:
                    watchedDirectories.append(directory)
                    print('Loaded directory ' + directory)
                else:
                    print('I\'ve already loaded this directory ' + directory)
                    continue
            elif os.path.exists(directory):
                print('Not a directory ' + directory)
            else:
                print('Failed to load directory (doesn\'t exist) ' + directory)
else:
    print('I need a directories.txt file that lists directories to watch')
    sys.exit()

if len(watchedDirectories) == 0:
    print('No valid directories in directories.txt to watch. Quitting')
    sys.exit()

# ==========
# Step 2: Load files to skip
# ==========
print('==========\nLoading Files to Skip\n==========')

skipFiles = []

skipFilesPath = os.path.realpath('skip.txt')

if os.path.exists(skipFilesPath):
    with open(skipFilesPath, 'r') as skipFilesFile:
        for skipFile in skipFilesFile:
            skipFile = skipFile.strip()
            
            # Ignores commented lines
            if skipFile.startswith("#"):
                continue
            
            # Standardises '/' '\' differences
            skipFile = skipFile.replace('\\', '/')
            
            if os.path.isfile(skipFile):
                skipFiles.append(skipFile)
                print('Will skip ' + skipFile)
            else:
                print('Invalid file ' + skipFile)
    
    if len(skipFiles) == 0:
        print('No files to skip found')
else:
    print('No skipfile.txt found. Continuing as it\'s non-essential')

# ==========
# Step 3: Load assets
# ==========
print('==========\nLoading Assets\n==========')

# All assets found by the script
assets      = []
jsCount     = 0
cssCount    = 0
skipcount   = 0

for directory in watchedDirectories:
    # Iterates over files in directory
    for asset in os.listdir(directory):
        # Checks if user wants file skipped
        if directory + '/' + asset in skipFiles:
            print('Skipping ' + asset)
            skipcount += 1
            continue
        
        if asset.endswith(".js") and not asset.endswith(".min.js"):
            assets.append(JSAsset(asset, directory))
            jsCount += 1
        elif asset.endswith(".css") and not asset.endswith(".min.css"):
            assets.append(CSSAsset(asset, directory))
            cssCount += 1

print("\n%s JS and %s CSS Loaded" % (jsCount, cssCount))

if skipcount > 0:
    print("%s Skipped" % skipcount)

# Only variable needed from on is the assets array
del jsCount, cssCount, skipcount, watchedDirectories, directoryConfigPath, skipFilesPath

# ==========
# Step 4: Minify all assets
# ==========
print('==========\nMinifying Assets\n==========')

for asset in assets:
    asset.saveMinified(asset.minify())
print('All assets minifed')

# ==========
# Step 5: Re-minifies any assets that have changed (each time I'm woken)
# ==========

while True:
    raw_input('Cave Johnson, we\'re done here. Press Enter to wake me and check for changes')
    
    print('==========\nRe-minifying Changed Assets\n==========')
    
    minifiedCount = 0
    
    print('Checking if any assets need re-minifying...')
    
    for asset in assets:
        if asset.minifyIfChanged():
            minifiedCount += 1
            print("%s has changed and been re-minified" % asset.name)
    
    if minifiedCount == 0:
        print('No assets changed since last check')