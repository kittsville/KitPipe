#!python3
'''
Name:           KitPipe
Description:    A crappy little assets minifier I created to make minifying WP-Librarian assets easier
Author:         Kittsville
Contact:        kittsville [at] gmail.com
Requires:       cssmin, slimit, Python 3.4.3
License:        GPL2
'''

from cssmin import cssmin   # For CSS
from slimit import minify   # For JS
import os                   # For file/directory interaction

watchedDirectories = ['C:/xampp/apps/wordpress/htdocs/wp-content/plugins/WP-Librarian/scripts','C:/xampp/apps/wordpress/htdocs/wp-content/plugins/WP-Librarian/styles']

def validDirectory(path):
    return os.path.exists(os.path.dirname(path))

# Indexing stage
print('Indexing Assets')
for directory in watchedDirectories:
    # Validates directory exists
    if not validDirectory(directory):
        print('Skipped invalid directory: "' + directory + '"')
        continue
    
    # Iterates over files in directory
    for asset in os.listdir(directory):
        if asset.endswith(".js"):
            print('Found JS file!')
        elif asset.endswith(".css"):
            print('Found CSS file!')
        else:
            print('Dunno what this is')