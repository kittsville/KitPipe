#!python3
'''
Name:           KitPipe
Description:    A crappy little assets minifier I created to make minifying WP-Librarian assets easier
Author:         Kittsville
Contact:        kittsville [at] gmail.com
Python:         3.4.3
License:        GPL2
'''

from cssmin import cssmin   # For CSS
from slimit import minify   # For JS
import os                   # For file/directory interaction
import hashlib              # Checking if a file has changed
import sys

watchedDirectories = ['C:/xampp/apps/wordpress/htdocs/wp-content/plugins/WP-Librarian/scripts','C:/xampp/apps/wordpress/htdocs/wp-content/plugins/WP-Librarian/styles']

def validDirectory(path):
    return os.path.exists(os.path.dirname(path))

# Holds shared minifying logic for JS/CSS assets
class Asset:
    # Generates checksum of file contents
    def genChecksum(self):
        # Generates checksum of file and returns first 128 bits
        return hashlib.sha256(open(self.file, 'rb').read()).digest()[:16]
    
    # Checks if the asset has been changed since the script last looked at it
    # Updates checksum if file has been modified
    def changed(self):
        newChecksum = genChecksum()
        
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
        return minify(open(self.file, 'r').read(), mangle=True, mangle_toplevel=True)

class CSSAsset(Asset):
    # Generates and returns minified version of CSS asset
    def minify(self):
        return cssmin(open(self.file, 'r').read())

# All assets found by the script
assets  = []
jsCount = 0
cssCount= 0

# Indexing stage
print('Building Asset Index...')
for directory in watchedDirectories:
    # Validates directory exists
    if not validDirectory(directory):
        print('Skipped invalid directory: "' + directory + '"')
    
    # Iterates over files in directory
    for asset in os.listdir(directory):
        if asset.endswith(".js") and not asset.endswith(".min.js"):
            assets.append(JSAsset(asset, directory))
            jsCount += 1
        elif asset.endswith(".css") and not asset.endswith(".min.css"):
            assets.append(CSSAsset(asset, directory))
            cssCount += 1

print("Assets Indexed:\n%s JS\n%s CSS" % (jsCount, cssCount))

# Minifies everything as existing minified assets might not match (could have been updated before script was run)
print('Minifying everything...')
for asset in assets:
    asset.saveMinified(asset.minify())
print('All assets minifed')

while True:
    input('Cave Johnson, we\'re done here. Press Enter to wake me and check for changes')
    
    minifiedCount = 0
    
    print('Checking if any assets need re-minifying...')
    
    for asset in assets:
        if asset.minifyIfChanged():
            minifiedCount += 1
    
    if minifiedCount == 0:
        print('No assets minified')
    elif minifiedCount == 1:
        print('1 asset minified')
    else:
        print("%s assets minified" % minifiedCount)