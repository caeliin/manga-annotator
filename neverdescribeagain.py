from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter.scrolledtext import ScrolledText
from PIL import Image, ImageTk
import os

#to do:
#image movement
#translation object things

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
    if page.find_all() == ():
        current_image = page.create_image(page.winfo_width() / 2, page.winfo_height() / 2, image = page.image)
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
        global pages_list
        folder_contents = os.listdir(page_folder.get())
        file_extension = page_name.get()[page_name.get().find("."):]
        pages_list = []
        for file in folder_contents:
            if file_extension in file:
                pages_list.append(file)
        
        #update list of pages
        page_listbox.delete(0, END)
        for file in pages_list:
            page_listbox.insert(END, file)
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
    return

#resizes the page when scrolled on
def zoom(event):
    global zoom_factor
    if event.delta < 0:
        zoom_factor /= 1.1
    if event.delta > 0:
        zoom_factor *= 1.1
    
    resize(int(width * zoom_factor), int(height * zoom_factor))
    return    

#fits the page to the current size
def fit_to_canvas(*args):
    max_width = page.winfo_width()
    max_height = page.winfo_height()
    zoom_factor = min(max_width / width, max_height / height)
    
    resize(int(width * zoom_factor), int(height * zoom_factor))
    return

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
height = 0
width = 0
current_image = ""

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
page_listbox = Listbox(menu_frame, selectmode = SINGLE, height = 10, width = 15)
page_listbox.grid(row = 3, column = 1, columnspan = 3, sticky = (N, S, E, W))
page_listbox.bind("<Double-Button-1>", listbox_change_page)

#Prev and Next buttons
ttk.Button(menu_frame, text = "<", width = 5, command = prev_page).grid(row = 4, column = 1, sticky = (S, E))
ttk.Button(menu_frame, text = ">", width = 5, command = next_page).grid(row = 4, column = 2, sticky = (S, W))

#Initialize the page image
canvas_frame = ttk.Frame(frame)
canvas_frame.grid(row = 1, column = 1, sticky=(N, S, E, W))
page = Canvas(canvas_frame)
page.pack(fill = BOTH, expand = YES)

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
page.bind("<MouseWheel>", zoom) #zoom using the mouse wheel
page.bind("<Configure>", fit_to_canvas)


root.mainloop()