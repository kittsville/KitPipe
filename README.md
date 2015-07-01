# KitPipe

**Asset minification for WP-Librarian is now handled by the [WP-Librarian Dev Kit](https://github.com/kittsville/WP-Librarian-Dev-Kit)**

A retired little asset pipeline in Python for CSS/JS. Created for [WP-Librarian](https://github.com/kittsville/WP-Librarian) but also so I'd use Python more.

###Requirements
- Python 2.7.9: If you can get Slimit working on Python 3 then remove 'import from futures' from KPipe and you're good to go
- Slimit
- CSSMin

###Known Issues
Script breaks if you delete a file it has indexed. Note that indexes are temporary to the script's existence so you only need to worry about this if you delete a file between Cave Johnson difference checking cycles.

###Usage
1. Add every directory you want minified to `directories.txt`
2. Add any files you don't want minified to `skip.txt`
3. Run script. Every JS and CSS file found in the given directories will be minified<sup>1</sup>
4. Press enter every time you want KitPipe to re-minify any files that have changed

---

1 - Besides assets whose names end in `.min.css` or `.min.js`
