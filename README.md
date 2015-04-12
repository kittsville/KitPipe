# KitPipe
A crappy little asset pipeline in Python for CSS/JS. Created for [WP-Librarian](https://github.com/kittsville/WP-Librarian) but also so I'd use Python more.

###Requirements
- Python 2.7.9: If you can get Slimit working on Python 3 then remove 'import from futures' from KPipe and you're good to go
- Slimit
- CSSMin

###Usage
1. Add every directory you want minified to `directories.txt`
2. Run script. Every JS and CSS file found in the given directories will be minified<sup>1</sup>
3. Press enter every time you want KitPipe to re-minify any files that have changed

---

1 - Besides assets whose names end in `.min.css` or `.min.js`
