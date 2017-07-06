# manga-annotator
Loads loose (non-zipped) manga files in a folder and allows placing of translations on the image by position. Translations are saved in the same folder as the images.

Created with tkinter.

Loading files
- Uses PIL's Image module to load the images. The list of supported file formats can be found here: http://pillow.readthedocs.io/en/3.4.x/handbook/image-file-formats.html
- Click "Open" to browse for a file. Selecting an image will load it onto the display area. Other images of the same file type will be loaded for browsing.
- If a save file is found in the directory, it will be loaded automatically.

Navigating
- Double click a file name in the list on the right to load it onto the display area.
- Click the "<" and ">" buttons below the list of pages to navigate to the previous and next pages, respectively.

Changing the view
- Scroll up with the mouse wheel to zoom into the image, and scroll down to zoom out of the image.
- Use the scrollbars to the right and below the image to move around a zoomed-in image.

Creating translations
- Click on the display area to create a new translation. Type the translation into the textbox at the bottom of the screen. The translation text is associated with the newly created translation.

Editing translations
- Click a translation to make it active and view / edit its text.
- To deselect the active translation, hit "Esc" on the keyboard or click elsewhere on the program.
- With a translation active, click one of the colours below the list of pages to change its display colour.

Reading translations
- When no translations are active, move the mouse over translations to display their text in the textbox.
- Click on a translation to activate it and load its text to the textbox until deselected.

Deleting translations
- Empty translations (without text) are auto-deleted once deselected.
- With a translation active, click the "Delete" button below the list of pages to delete it.
- Check the checkbox beside the "Delete" button to disable the confirmation popup.

Saving
- The program auto-saves when creating new translations, deleting translations, changing pages, or loading a new file.
