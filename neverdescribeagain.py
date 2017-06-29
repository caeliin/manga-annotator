from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter.scrolledtext import ScrolledText
from PIL import Image, ImageTk
import os

#load an image
def set_filepath(*args):
    global page_image
    try:
        path = filedialog.askopenfilename()        
        if path != "":
            #set location strings
            page_path.set(path)
            page_folder.set(os.path.dirname(path))
            page_name.set(os.path.basename(path))
            
            #load the other files
            folder_contents = os.listdir(page_folder.get())
            file_extension = page_name.get()[page_name.get().find("."):]
            other_pages = []
            for file in folder_contents:
                if file_extension in file:
                    other_pages.append(file)
            
            #load image
            page_image = ImageTk.PhotoImage(Image.open(page_path.get()))
            page.image = page_image
            page.configure(image = page_image)
            
            #update list of pages
            page_list.delete(0, END)
            for file in other_pages:
                page_list.insert(END, file)
    except:
        pass
    return

#load the previous page in the folder
def prev_page(*args):
    #file and folder info
    folder_contents = os.listdir(page_folder.get())
    current_page = page_name.get()
    file_extension = page_name.get()[page_name.get().find("."):]
    other_pages = []
    for file in folder_contents: #only interested in images
        if file_extension in file:
            other_pages.append(file)
    
    #find the prev page    
    page_index = other_pages.index(current_page)
    page_index = (page_index - 1) % len(other_pages)
    current_page = other_pages[page_index]
    
    #update everything
    new_path = os.path.join(page_folder.get(), current_page) #new path
    page_name.set(current_page) #set current page name
    page_path.set(new_path) #set the full page path 
    
    #reload the image
    page_image = ImageTk.PhotoImage(Image.open(page_path.get()))
    page.image = page_image
    page.configure(image = page_image)
    return

#load the next page in the folder
def next_page(*args):
    #file and folder info
    folder_contents = os.listdir(page_folder.get())
    current_page = page_name.get()
    file_extension = page_name.get()[page_name.get().find("."):]
    other_pages = []
    for file in folder_contents: #only interested in images
        if file_extension in file:
            other_pages.append(file)
    
    #find the next page    
    page_index = other_pages.index(current_page)
    page_index = (page_index + 1) % len(other_pages)
    current_page = other_pages[page_index]
    
    #update everything
    new_path = os.path.join(page_folder.get(), current_page) #new path
    page_name.set(current_page) #set current page name
    page_path.set(new_path) #set the full page path 
    
    #reload the image
    page_image = ImageTk.PhotoImage(Image.open(page_path.get()))
    page.image = page_image
    page.configure(image = page_image)
    return

#Temporary function for buttons
def WRITE_ME(*args):
    pass

#App basics
root = Tk()
root.title("Visual Translator - Never Use Sheets Again")

#Location of the current image
page_path = StringVar()
page_path.set("") #Initially set to blank

page_folder = StringVar()
page_name = StringVar()

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
page_list = Listbox(menu_frame, selectmode = SINGLE, height = 10, width = 15)
page_list.grid(row = 3, column = 1, columnspan = 3, sticky = (N, S, E, W))

#Prev and Next buttons
ttk.Button(menu_frame, text = "<", width = 5, command = prev_page).grid(row = 4, column = 1, sticky = (S, E))
ttk.Button(menu_frame, text = ">", width = 5, command = next_page).grid(row = 4, column = 2, sticky = (S, W))

#Initialize the page image
page = ttk.Label(frame)
page.grid(row = 1, column = 1)
page.image = ""

#Text box
translation_text = ScrolledText(frame)
translation_text["height"] = 5
translation_text.grid(row = 2, column = 1, columnspan = 2, sticky = (W, E))

#Stretch configurations
root.columnconfigure(0, weight = 1)
root.rowconfigure(0, weight = 1)
frame.columnconfigure(1, weight = 1)
frame.rowconfigure(1, weight = 1)
menu_frame.rowconfigure(3, weight = 1)

root.mainloop()