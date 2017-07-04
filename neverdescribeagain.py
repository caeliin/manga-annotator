from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter.scrolledtext import ScrolledText
from PIL import Image, ImageTk
import os

#to do:
#translation object scroll over
#saving to file
#loading from file
#click off from textbox focus - probably need break
#deactivate active translation on escape key

class Annotation(object):
    
    def __init__(self, event): #does not add to list
        self.text = "" #translation text - begins blank
        self.active = False
        self.target_colour = "red"
        self.active_colour = "black"
        self.outline_colour = "white"
        self.x = int(page.canvasx(event.x) / zoom_factor) #true x
        self.y = int(page.canvasy(event.y) / zoom_factor) #true y
        self.effective_x = int(self.x * zoom_factor) #displayed x
        self.effective_y = int(self.y * zoom_factor) #displayed y
        
        #inner background
        self.inner_circle_inner_liner = page.create_oval(self.effective_x - 4, self.effective_y - 4, self.effective_x + 4, self.effective_y + 4, outline = self.outline_colour, tags = (self, "translation"))
        self.inner_circle_outer_liner = page.create_oval(self.effective_x - 6, self.effective_y - 6, self.effective_x + 6, self.effective_y + 6, outline = self.outline_colour, tags = (self, "translation"))
        
        #outer background
        self.outer_circle_inner_liner = page.create_oval(self.effective_x - 9, self.effective_y - 9, self.effective_x + 9, self.effective_y + 9, outline = self.outline_colour, tags = (self, "translation"))
        self.outer_circle_outer_liner = page.create_oval(self.effective_x - 11, self.effective_y - 11, self.effective_x + 11, self.effective_y + 11, outline = self.outline_colour, tags = (self, "translation"))
        
        #vertical background
        self.vline_back = page.create_rectangle(self.effective_x - 1, self.effective_y - 16, self.effective_x + 1, self.effective_y + 16, outline = self.outline_colour, tags = (self, "translation"))
        
        #horizontal background
        self.hline_back = page.create_rectangle(self.effective_x - 16, self.effective_y - 1, self.effective_x + 16, self.effective_y + 1, outline = self.outline_colour, tags = (self, "translation"))
        
        #actual target
        self.inner_circle = page.create_oval(self.effective_x - 5, self.effective_y - 5, self.effective_x + 5, self.effective_y + 5, outline = self.target_colour, tags = (self, "translation"))
        self.outer_circle = page.create_oval(self.effective_x - 10, self.effective_y - 10, self.effective_x + 10, self.effective_y + 10, outline = self.target_colour, tags = (self, "translation"))
        self.vline = page.create_line(self.effective_x, self.effective_y - 15, self.effective_x, self.effective_y + 15, fill = self.target_colour, tags = (self, "translation"))
        self.hline = page.create_line(self.effective_x - 15, self.effective_y, self.effective_x + 15, self.effective_y, fill = self.target_colour, tags = (self, "translation"))
        return
    
    #redraw the items when page loads
    def redraw(self):
        #inner background
        self.inner_circle_inner_liner = page.create_oval(self.effective_x - 4, self.effective_y - 4, self.effective_x + 4, self.effective_y + 4, outline = self.outline_colour, tags = (self, "translation"))
        self.inner_circle_outer_liner = page.create_oval(self.effective_x - 6, self.effective_y - 6, self.effective_x + 6, self.effective_y + 6, outline = self.outline_colour, tags = (self, "translation"))
        
        #outer background
        self.outer_circle_inner_liner = page.create_oval(self.effective_x - 9, self.effective_y - 9, self.effective_x + 9, self.effective_y + 9, outline = self.outline_colour, tags = (self, "translation"))
        self.outer_circle_outer_liner = page.create_oval(self.effective_x - 11, self.effective_y - 11, self.effective_x + 11, self.effective_y + 11, outline = self.outline_colour, tags = (self, "translation"))
        
        #vertical background
        self.vline_back = page.create_rectangle(self.effective_x - 1, self.effective_y - 16, self.effective_x + 1, self.effective_y + 16, outline = self.outline_colour, tags = (self, "translation"))
        
        #horizontal background
        self.hline_back = page.create_rectangle(self.effective_x - 16, self.effective_y - 1, self.effective_x + 16, self.effective_y + 1, outline = self.outline_colour, tags = (self, "translation"))
        
        #actual target
        self.inner_circle = page.create_oval(self.effective_x - 5, self.effective_y - 5, self.effective_x + 5, self.effective_y + 5, outline = self.target_colour, tags = (self, "translation"))
        self.outer_circle = page.create_oval(self.effective_x - 10, self.effective_y - 10, self.effective_x + 10, self.effective_y + 10, outline = self.target_colour, tags = (self, "translation"))
        self.vline = page.create_line(self.effective_x, self.effective_y - 15, self.effective_x, self.effective_y + 15, fill = self.target_colour, tags = (self, "translation"))
        self.hline = page.create_line(self.effective_x - 15, self.effective_y, self.effective_x + 15, self.effective_y, fill = self.target_colour, tags = (self, "translation"))
        return
    
    #redraw the items when the page zooms    
    def move_zoom(self):
        #change displayed coordinates for canvas
        self.effective_x = int(self.x * zoom_factor)
        self.effective_y = int(self.y * zoom_factor)
        
        #update coordinates
        
        #inner background
        page.coords(self.inner_circle_inner_liner, self.effective_x - 4, self.effective_y - 4, self.effective_x + 4, self.effective_y + 4)
        page.coords(self.inner_circle_outer_liner, self.effective_x - 6, self.effective_y - 6, self.effective_x + 6, self.effective_y + 6)
        
        #outer background
        page.coords(self.outer_circle_inner_liner, self.effective_x - 9, self.effective_y - 9, self.effective_x + 9, self.effective_y + 9)
        page.coords(self.outer_circle_outer_liner, self.effective_x - 11, self.effective_y - 11, self.effective_x + 11, self.effective_y + 11)
        
        #vertical background
        page.coords(self.vline_back, self.effective_x - 1, self.effective_y - 16, self.effective_x + 1, self.effective_y + 16)
        
        #horizontal background
        page.coords(self.hline_back, self.effective_x - 16, self.effective_y - 1, self.effective_x + 16, self.effective_y + 1)
        
        #actual target
        page.coords(self.inner_circle, self.effective_x - 5, self.effective_y - 5, self.effective_x + 5, self.effective_y + 5)
        page.coords(self.outer_circle, self.effective_x - 10, self.effective_y - 10, self.effective_x + 10, self.effective_y + 10)
        page.coords(self.vline, self.effective_x, self.effective_y - 15, self.effective_x, self.effective_y + 15)
        page.coords(self.hline, self.effective_x - 15, self.effective_y, self.effective_x + 15, self.effective_y)
        return
    
    #activates the current object
    def activate(self):
        assert self.active == False, "attempted to activate already active object"
        page.itemconfig(self.inner_circle, outline = self.active_colour)
        page.itemconfig(self.outer_circle, outline = self.active_colour)
        page.itemconfig(self.vline, fill = self.active_colour)
        page.itemconfig(self.hline, fill = self.active_colour)
        self.active = True
        display_translation(self.text) #display own text
        translation_textbox.focus_set()
        global active_translation
        active_translation = self
        return    
    
    #deactivates the current object. 
    #WARNING: do not deactivate all objects!
    def deactivate(self):
        assert self.active, "attempted to deactivate inactive object"
        page.itemconfig(self.inner_circle, outline = self.target_colour)
        page.itemconfig(self.outer_circle, outline = self.target_colour)
        page.itemconfig(self.vline, fill = self.target_colour)
        page.itemconfig(self.hline, fill = self.target_colour)
        self.active = False
        self.text = read_translation() #put textbox text in self
        global active_translation
        active_translation = None        
        if self.text == "": #delete self if no text entered
            self.delete()
        return     
    
    #remove objects from page, but don't delete information.
    #object must be inactive
    def remove(self):
        assert self.active == False, "attempted to remove active object"
        page.delete(self)
        return
    
    #delete object
    def delete(self):
        assert active_translation is not self, "attempted to delete active object"
        page.delete(self)
        translations[current_page_name.get()].remove(self)
        return
        
# # # # # # # # # # # # # # # # # # # # # # # # End class declaration # # # # # # # # # # # # # # # # # # # # # # #

#
# Page loading functions
#

#load image and update location strings. Assumes path is valid.
def load_page(full_path):
    assert os.path.exists(full_path), "load_page encountered invalid path"
    global height, width, current_image
    
    #set location strings
    page_path.set(full_path)
    page_folder.set(os.path.dirname(full_path))
    current_page_name.set(os.path.basename(full_path))
#kind of inefficient to load then fit - consider streamlining later    
    #load image
    page.image = ImageTk.PhotoImage(Image.open(page_path.get()))
    if current_image == None:
        current_image = page.create_image(0, 0, anchor = NW, image = page.image)
    else:
        page.itemconfig(current_image, image = page.image)        
    
    #set sizes
    width = page.image.width()
    height = page.image.height()
    fit_to_canvas()
    return

#open a file
def set_filepath(*args):
    path = filedialog.askopenfilename()        
    if os.path.exists(path): #if file actually selected
        
        load_page(path)
        
        #load other files in folder
        folder_contents = os.listdir(page_folder.get())
        file_extension = current_page_name.get()[current_page_name.get().find("."):]
        
        global pages_list
        pages_list = [] #reset list of pages
        for file in folder_contents:
            if file_extension in file: #only add file if same extension as selected file (exclude save and other files)
                pages_list.append(file)
        
        #update listbox of pages
        page_listbox.delete(0, END)
        for file in pages_list:
            page_listbox.insert(END, file)
        
        global translations
        translations = {} #reset translation objects dictionary
        for file in pages_list: #add each page as key to translation dictionary
            translations[file] = []
    return
    
#load the previous page in the folder
def prev_page(*args):
    #find the previous page
    assert (current_page_name.get() in pages_list), "current page not in page list!"
    
    save_page_progress()
    
    page_index = pages_list.index(current_page_name.get())
    page_index = (page_index - 1) % len(pages_list) #prev page
    prev_page = pages_list[page_index]
    
    load_page(os.path.join(page_folder.get(), prev_page))
    load_translations()
    return

#load the next page in the folder
def next_page(*args):
    #find the next page
    assert (current_page_name.get() in pages_list), "current page not in page list!"
    
    save_page_progress()
    
    page_index = pages_list.index(current_page_name.get())
    page_index = (page_index + 1) % len(pages_list) #next page
    next_page = pages_list[page_index]
    
    load_page(os.path.join(page_folder.get(), next_page))
    load_translations()
    return

#change active page based on list selection
def listbox_change_page(*args):
    save_page_progress()
    selected_index = page_listbox.curselection() #get current selected name
    load_page(os.path.join(page_folder.get(), pages_list[selected_index[0]])) #load the selected page
    load_translations()
    return

#
# Image manipulation functions
#

#resize the image to zoom in
def resize(new_width, new_height):
    temp_image = Image.open(page_path.get())
    temp_image = temp_image.resize((new_width, new_height), Image.ANTIALIAS) #resize
    page.image = ImageTk.PhotoImage(temp_image)
    page.itemconfig(current_image, image = page.image) #set image
    page.config(scrollregion = page.bbox("all")) #resize canvas to image
    return

#resize the page when scrolled on
def zoom(event):
    global zoom_factor
    if event.delta < 0: #scroll down
        zoom_factor /= 1.1
    if event.delta > 0: #scroll up
        zoom_factor *= 1.1
    
    min_zoom = min((page.winfo_height() - 4) / height, (page.winfo_width() - 4) / width)
    if zoom_factor < min_zoom: #cannot zoom out past at least two opposite edges touching edges of canvas
        zoom_factor = min_zoom
    
    resize(int(width * zoom_factor), int(height * zoom_factor))
    
    for item in translations[current_page_name.get()]: #redraw all translation objects
        item.move_zoom()
    return    

#fit the page to the current window size
def fit_to_canvas(*args):
    global zoom_factor
    max_width = page.winfo_width()
    max_height = page.winfo_height()
    zoom_factor = min((max_width - 4) / width, (max_height - 4) / height)
    
    resize(int(width * zoom_factor), int(height * zoom_factor))
    return

#returns the true coordinates of the image from displayed coordinates
def true_coordinates(screen_x, screen_y):
    return (int(page.canvasx(screen_x) / zoom_factor), int(page.canvasx(screen_y) / zoom_factor))

#
# Translation object functions
#

#find a translation or list of translations in the current page
def find_translations(list_of_ids):
    matches = []
    for search_query in list_of_ids:
        for item in translations[current_page_name.get()]:
            if search_query == str(item):
                matches.append(item)
                break
    return matches

#identify whether canvas click is on existing object or not and calls correct function
def canvas_click(event):
    overlapping = page.find_enclosed(page.canvasx(event.x) - 15, page.canvasx(event.y) - 15, page.canvasx(event.x) + 15, page.canvasx(event.y) + 15)
    results = []
    for item in overlapping:
        tags = page.gettags(item)
        if len(tags) == 2 and tags[0] not in results:
            results.append(tags[0])
    if results == []:
        new_translation(event)
    else:
        select_translation(find_translations(results), event)
    return 

#create a new translation object and add it to the translations dictionary
def new_translation(event):
    new = Annotation(event)
    translations[current_page_name.get()].append(new)
    activate_translation(new)
    return

def activate_translation(new_active_translation):
    if active_translation is not new_active_translation: #do not reactivate active translation
        #deactivate previously active translation    
        if active_translation is not None:    
            active_translation.deactivate()    
        
        #activate selected translation
        new_active_translation.activate()
    return

#activates the translation closest to click
def select_translation(translations, event):
    assert len(translations) > 0, "activate_translations encountered empty results list"
    
    if len(translations) > 1: #if more than one result, find the one that's closest
        distances = [] #same order as translations
        x, y = true_coordinates(event.x, event.y)
        for result in translations:
            distances.append((result.x - x) ** 2 + (result.y - y) ** 2)
        closest = translations[distances.index(min(distances))]
    else:
        closest = translations[0]
    
    activate_translation(closest)
    return

#
# Textbox functions
#

def display_translation(text):
    translation_textbox.delete("1.0", END)
    translation_textbox.insert("1.0", text)
    return

def read_translation():
    translation_text = translation_textbox.get("1.0", "end-1c")
    translation_textbox.delete("1.0", END)
    return translation_text

#
# Saving and loading functions
#

#save all translation progress before moving pages
def save_page_progress(*args):
    for item in translations[current_page_name.get()]: #remove items from screen
        if item.active: #reset all active objects before changing pages
            item.deactivate()
        item.remove()
    return

def load_translations(*args):
    for item in translations[current_page_name.get()]:
        item.redraw()
    return

#save all translations to file
def save(*args):
    save_page_progress() #deactivates active translation and stores textbox text
    #WRITE_ME()
    return
    
#
# There's a problem if this is still used somewhere.
#

#Temporary function
def WRITE_ME(*args):
    pass

#App basics
root = Tk()
root.title("Visual Translator - Never Use Sheets Again")

#File things
page_path = StringVar() #full path of the current page
page_folder = StringVar() #path to the directory
current_page_name = StringVar() #file name of the current page
pages_list = [] #list of all files in the folder

#other (global) variables
zoom_factor = 1 #zoom into the page
height = 1 #image true height
width = 1 #image true width
current_image = None #becomes int when image
active_translation = None #the selected translation
translations = {} #holds translation objects for the entire folder

#App frame and settings
frame = ttk.Frame(root)
frame.grid(row = 0, column = 0, sticky = (N, S, E, W))
frame['padding'] = 2
frame['borderwidth'] = 2
frame['relief'] = 'ridge'

#Menu frame
menu_frame = ttk.Frame(frame)
menu_frame.grid(row = 1, column = 2, sticky = (N, S))

#Open file
ttk.Button(menu_frame, text = "Open", command = set_filepath).grid(row = 1, column = 1, columnspan = 2, sticky = (N, E, W))

#Save
ttk.Button(menu_frame, text = "Save", command = WRITE_ME).grid(row = 2, column = 1, columnspan = 2, sticky = (N, E, W))

#List of pages
listbox_frame = ttk.Frame(menu_frame) #frame for the box
listbox_frame.grid(row = 3, column = 1, columnspan = 3, sticky = (N, S, E, W))

page_listbox = Listbox(listbox_frame, selectmode = SINGLE, height = 10, width = 15) #Listbox itself
page_listbox.pack(side = LEFT, fill = BOTH, expand = YES)

listbox_scrollbar = Scrollbar(listbox_frame, orient = VERTICAL) #scrollbar for the listbox
listbox_scrollbar.pack(side = RIGHT, fill = Y)

listbox_scrollbar.config(command = page_listbox.yview) #connect the two
page_listbox.config(yscrollcommand = listbox_scrollbar.set)

#Prev and Next buttons
ttk.Button(menu_frame, text = "<", width = 5, command = prev_page).grid(row = 4, column = 1, sticky = (S, E)) #prev
ttk.Button(menu_frame, text = ">", width = 5, command = next_page).grid(row = 4, column = 2, sticky = (S, W)) #next

#create page image (canvas)
canvas_frame = ttk.Frame(frame) #frame to hold canvas
canvas_frame.grid(row = 1, column = 1, sticky=(N, S, E, W))
page = Canvas(canvas_frame, width = 300, height = 600) #create canvas

#canvas vertical scrollbar
canvas_vbar = Scrollbar(canvas_frame, orient = VERTICAL)
canvas_vbar.pack(side = RIGHT, fill = Y)
canvas_vbar.config(command = page.yview)

#canvas horizontal scrollbar
canvas_hbar = Scrollbar(canvas_frame, orient = HORIZONTAL)
canvas_hbar.pack(side = BOTTOM, fill = X)
canvas_hbar.config(command = page.xview)

#connect canvas to scrollbars
page.config(xscrollcommand = canvas_hbar.set, yscrollcommand = canvas_vbar.set)
page.pack(side = LEFT, fill = BOTH, expand = YES) #canvas takes up rest of space

#Text box for translations
translation_textbox = ScrolledText(frame, wrap = 'word', height = 5)
translation_textbox.grid(row = 2, column = 1, columnspan = 2, sticky = (W, E))

#Stretch configurations
root.columnconfigure(0, weight = 1) #main window
root.rowconfigure(0, weight = 1) #main window
frame.columnconfigure(1, weight = 1, minsize = 300) #canvas frame
frame.rowconfigure(1, weight = 1, minsize = 600) #canvas frame
menu_frame.rowconfigure(3, weight = 1) #listbox

#Event bindings
page_listbox.bind("<Double-Button-1>", listbox_change_page) #change active page by listbox
page.bind("<MouseWheel>", zoom) #zoom using the mouse wheel
page.bind("<Button-1>", canvas_click) #create a new object

root.mainloop()