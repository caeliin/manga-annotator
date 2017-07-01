from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter.scrolledtext import ScrolledText
from PIL import Image, ImageTk
import os

#to do:
#translation object things

class Annotation(object):
    
    def __init__(self, event): #does not add to list
        self.text = ""
        self.x = int(page.canvasx(event.x) / zoom_factor)
        self.y = int(page.canvasy(event.y) / zoom_factor)
        self.effective_x = int(self.x * zoom_factor)
        self.effective_y = int(self.y * zoom_factor)
        self.inner_circle = page.create_oval(self.effective_x - 5, self.effective_y - 5, self.effective_x + 5, self.effective_y + 5, outline = "red", tags = "translation")
        self.outer_circle = page.create_oval(self.effective_x - 10, self.effective_y - 10, self.effective_x + 10, self.effective_y + 10, outline = "red", tags = "translation")
        self.vline = page.create_line(self.effective_x, self.effective_y - 15, self.effective_x, self.effective_y + 15, fill = "red", tags = "translation")
        self.hline = page.create_line(self.effective_x - 15, self.effective_y, self.effective_x + 15, self.effective_y, fill = "red", tags = "translation")
        return
    
    #redraw the items when the page zooms    
    def redraw(self):
        #page.coords(self.item, new_xy) #change coordinates
        self.effective_x = int(self.x * zoom_factor)
        self.effective_y = int(self.y * zoom_factor)
        page.coords(self.inner_circle, self.effective_x - 5, self.effective_y - 5, self.effective_x + 5, self.effective_y + 5)
        page.coords(self.outer_circle, self.effective_x - 10, self.effective_y - 10, self.effective_x + 10, self.effective_y + 10)
        page.coords(self.vline, self.effective_x, self.effective_y - 15, self.effective_x, self.effective_y + 15)
        page.coords(self.hline, self.effective_x - 15, self.effective_y, self.effective_x + 15, self.effective_y)
        return
    
    #delete object if no longer needed
    def delete(self):
        WRITE_ME()
        return
        
#load image and update location strings. Assumes path is valid.
def load_page(full_path):
    assert os.path.exists(full_path) == True #assert path is valid
    global height, width, hw_ratio, current_image
    
    #set location strings
    page_path.set(full_path)
    page_folder.set(os.path.dirname(full_path))
    page_name.set(os.path.basename(full_path))
    
    #load image
    page.image = ImageTk.PhotoImage(Image.open(page_path.get()))
    if type(current_image) != int:
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
    if os.path.exists(path):
        
        load_page(path)
        
        #load the other files
        folder_contents = os.listdir(page_folder.get())
        file_extension = page_name.get()[page_name.get().find("."):]
        
        global pages_list
        pages_list = []
        for file in folder_contents:
            if file_extension in file:
                pages_list.append(file)
        
        #update list of pages
        page_listbox.delete(0, END)
        for file in pages_list:
            page_listbox.insert(END, file)
        
        global translations
        translations = {}    
        for file in pages_list:
            translations[file] = []
    return

#load the previous page in the folder
def prev_page(*args):
    #find the previous page
    page_index = pages_list.index(page_name.get())
    page_index = (page_index - 1) % len(pages_list) #prev page
    prev_page = pages_list[page_index]
    
    load_page(os.path.join(page_folder.get(), prev_page))
    return

#load the next page in the folder
def next_page(*args):
    #find the next page
    page_index = pages_list.index(page_name.get())
    page_index = (page_index + 1) % len(pages_list) #next page
    next_page = pages_list[page_index]
    
    load_page(os.path.join(page_folder.get(), next_page))
    return

#changes active page based on list selection
def listbox_change_page(*args):
    selected_index = page_listbox.curselection() #get current selected
    load_page(os.path.join(page_folder.get(), pages_list[selected_index[0]]))
    return

#changes the page size
def resize(new_width, new_height):
    
    temp_image = Image.open(page_path.get())
    temp_image = temp_image.resize((new_width, new_height), Image.ANTIALIAS)
    page.image = ImageTk.PhotoImage(temp_image)
    page.itemconfig(current_image, image = page.image)
    page.config(scrollregion = page.bbox("all"))
    return

#resizes the page when scrolled on
def zoom(event):
    global zoom_factor
    if event.delta < 0:
        zoom_factor /= 1.1
    if event.delta > 0:
        zoom_factor *= 1.1
    
    min_zoom = min((page.winfo_height() - 4) / height, (page.winfo_width() - 4) / width)
    if zoom_factor < min_zoom:
        zoom_factor = min_zoom
    
    resize(int(width * zoom_factor), int(height * zoom_factor))
    
    for item in translations[page_name.get()]:
        item.redraw()
    return    

#fits the page to the current size
def fit_to_canvas(*args):
    global zoom_factor
    max_width = page.winfo_width()
    max_height = page.winfo_height()
    zoom_factor = min((max_width - 4) / width, (max_height - 4) / height)
    
    resize(int(width * zoom_factor), int(height * zoom_factor))
    return

def new_translation(event):
    translations[page_name.get()].append(Annotation(event))
    return

def page_size(*args):
    #page.config(width = min(, height = )
    pass

#Temporary function for buttons
def WRITE_ME(*args):
    pass

#App basics
root = Tk()
root.title("Visual Translator - Never Use Sheets Again")

#File paths
page_path = StringVar() #full path of the current image
page_folder = StringVar() #path to the directory
page_name = StringVar() #name of the currently displayed page
pages_list = [] #list of all files in the folder

#other variables
zoom_factor = 1
height = 1
width = 1
current_image = ""
translations = {}

#App frame
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
ttk.Button(menu_frame, text = "<", width = 5, command = prev_page).grid(row = 4, column = 1, sticky = (S, E))
ttk.Button(menu_frame, text = ">", width = 5, command = next_page).grid(row = 4, column = 2, sticky = (S, W))

#page image (canvas)
canvas_frame = ttk.Frame(frame)
canvas_frame.grid(row = 1, column = 1, sticky=(N, S, E, W))
page = Canvas(canvas_frame, width = 300, height = 600)

#canvas horizontal scrollbar
canvas_hbar = Scrollbar(canvas_frame, orient = HORIZONTAL)
canvas_hbar.pack(side = BOTTOM, fill = X)
canvas_hbar.config(command = page.xview)

#canvas vertical scrollbar
canvas_vbar = Scrollbar(canvas_frame, orient = VERTICAL)
canvas_vbar.pack(side = RIGHT, fill = Y)
canvas_vbar.config(command = page.yview)

#connect canvas to scrollbar and pack page
page.config(xscrollcommand = canvas_hbar.set, yscrollcommand = canvas_vbar.set)
page.pack(side = LEFT, fill = BOTH, expand = YES)

#Text box
translation_text = ScrolledText(frame)
translation_text["height"] = 5
translation_text.grid(row = 2, column = 1, columnspan = 2, sticky = (W, E))

#Stretch configurations
root.columnconfigure(0, weight = 1) #main window
root.rowconfigure(0, weight = 1) #main window
frame.columnconfigure(1, weight = 1, minsize = 300) #canvas frame
frame.rowconfigure(1, weight = 1, minsize = 600) #canvas frame
menu_frame.rowconfigure(3, weight = 1) #listbox

#Event bindings
page_listbox.bind("<Double-Button-1>", listbox_change_page) #change active page by listbox
page.bind("<MouseWheel>", zoom) #zoom using the mouse wheel
page.bind("<Button-1>", new_translation) #create a new object

root.mainloop()