# uniparser-morph-editor

This is a simple web-based editor for grammatical dictionaries in the UniParser format. The idea is to look at one lemma at a time and use the keyboard as much as possible to speed up manual processing. To start working with it, you have to edit ``settings.txt``, run ``morph_edit_interface.py`` as a server and open http://127.0.0.1:5500/ in your browser.


Keyboard shortcuts:

* Arrows: previous or next lemma.

* Enter: save the dictionary and current settings. (Warning: there is no autosave!)

* 1: Delete everything but the first segment in the translation field.

* 2: Delete everything but the second segment in the translation field.

* - (minus): Mark lemma for removal (by adding a minus sign to it).

* other keys: add/remove grammatical tags (defined in ``settings.txt``).