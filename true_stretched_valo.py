import win32api
import win32con
import pywintypes
import ctypes
import time
import tkinter as tk
from tkinter import ttk
 
#* hard coded default values (again will try to change this so the script automaticly gets the defualt reso) 
g_width = 1920
g_height = 1080 
 
#! Function to get all availiable resolutions on the monitor
def get_available_resolutions():
    resolutions = set()  # Use a set to avoid duplicate entries
     
    
    i = 0
    while True:  # Loop through display devices
        try:
            device_name = win32api.EnumDisplayDevices(None, i)  # Get the display device information
            if not device_name.DeviceName:  # If no device name is found, break the loop
                break
            
            mode_num = 0  # Initialize the mode number to start enumerating display settings
            while True:  # Loop through display settings for the current device
                try:
                    mode = win32api.EnumDisplaySettings(device_name.DeviceName, mode_num)  # Get the display settings for the current mode
                    resolution = f"{mode.PelsWidth}x{mode.PelsHeight}"  # Format the resolution as a string
                    resolutions.add(resolution)  # Add the resolution to the set to avoid duplicates
                    mode_num += 1  #   next display setting
                except pywintypes.error:  
                    break
            i += 1  #   next display device
        except pywintypes.error:   
            break

    
    #* Convert resolutions to a list of tuples (width, height)
    resolution_tuples = []
    for res in resolutions:
        width, height = map(int, res.split('x'))
        resolution_tuples.append((width, height))

    #* Sort by area (width * height) in descending order
    sorted_resolutions = sorted(resolution_tuples, key=lambda x: x[0] * x[1], reverse=True)
    
    #* Convert back to formatted strings
    sorted_resolution_strings = [f"{width}x{height}" for width, height in sorted_resolutions]

    return sorted_resolution_strings

#! Function to set the selected resolution
def set_resolution(width, height):
    devmode = pywintypes.DEVMODEType()
    devmode.PelsWidth = width
    devmode.PelsHeight = height
    devmode.Fields = win32con.DM_PELSWIDTH | win32con.DM_PELSHEIGHT

    result = win32api.ChangeDisplaySettings(devmode, 0)
    #if result == win32con.DISP_CHANGE_SUCCESSFUL:
    #   print("Resolution changed successfully.")
    #elif result == win32con.DISP_CHANGE_RESTART:
    #    print("You need to restart your computer for the changes to take effect.")
    #else:
    #    print("Failed to change resolution.")

#! Function for when user selects a resolution from drop down       
def on_select(event, combo):
    global g_width, g_height
    selected_resolution = combo.get()
    #print(f"Selected resolution: {selected_resolution}")
    
    
    
    # Split the selected_resolution into parts
    #width, height = map(int, selected_resolution.split('x'))
    
    # Store the results in an array
    #reslo = [width, height]
    
    # Split the selected_resolution into parts
    parts = selected_resolution.split(' x ')
    if len(parts) == 1:
        #device_name = parts[0]
        resolution = parts[0]
        
         
        # Split resolution into width and height
        width, height = resolution.split('x')
        
        # Store the results in an array
       # reslo = [device_name, int(width), int(height)]
        
      #  print(f"Device Name: {device_name}")
        #print(f"Width: {width}")
        #print(f"Height: {height}")
       # print(f"Resulting Array: {reslo}")
        g_width = int(width)
        g_height = int(height)
        
        #print(g_height)
        #print(g_width)
        #set_resolution(int(width), int(height))
    #set_resolution()
        
#! Function to apply the selected resolution and hide the window
def apply_changes(lbl_status):
    global g_width, g_height
    window_title = "VALORANT  "
    global original_style
    window_handle = ctypes.windll.user32.FindWindowW(None, window_title) # look for the window title of valorant
    if window_handle == 0:
        lbl_status.config(text="Valorant not found")
    else:
        #* change monitor resolution
        set_resolution(g_width, g_height)
        #print(f"width = {g_width}")
        #print(f"height = {g_height}")
        
        time.sleep(1) #delay for 2 seconds
        #( make windowed application fullscreen)
        original_style = ctypes.windll.user32.GetWindowLongW(window_handle, ctypes.c_int(-16))
        new_style = original_style & ~0x00800000 & ~0x00040000
        ctypes.windll.user32.SetWindowLongW(window_handle, ctypes.c_int(-16), new_style)
        ctypes.windll.user32.ShowWindow(window_handle, ctypes.c_int(3))
        lbl_status.config(text="True stretched applied")
     
#! Function to return monitor resolution to 1920x1080 and to show valorants window
#TODO: update this so the user can input there own default resoloution or add a slight function to get the monitor defualt reso
def unapply_changes(lbl_status, combobox):
    window_title = "VALORANT  "
    window_handle = ctypes.windll.user32.FindWindowW(None, window_title)

    if window_handle == 0:
        lbl_status.config(text="Valorant not found")
    else:
        #unapply changes
        ctypes.windll.user32.SetWindowLongW(window_handle, ctypes.c_int(-16), original_style)
        lbl_status.config(text="True stretch removed") 
        
        #set monitor resolution to default of (1920 x 1080):
        #maybe in a future update i'll make it so the user can first set there defualt values
        time.sleep(1) # sleep for 2 seconds
        
        set_resolution(1920, 1080) # default resolution
        
        #change the combobox defualt selected resolution
        default_resolution = "1920x1080"
        combobox.set(default_resolution)
        
        
        
#! Function to create the GUI
#TODO: At a later time update this so it is in a seperate py file       
def gui():
    root = tk.Tk()
    root.title("ValorantTS_HI") # window lalbel
    root.geometry("300x300") # window size

    root.configure(bg="#2e2e2e")

    frame = ttk.Frame(root, padding="10")
    frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    frame.grid(row=0, column=0, padx=10, pady=10)
    
    lbl_title = ttk.Label(frame, text="Apply TS", font=("Arial", 16))
    lbl_title.grid(row=0, columnspan=2, pady=(0, 10)) 

    lbl_status = ttk.Label(frame, text="")
    lbl_status.grid(row=3, columnspan=2, pady=(10, 0))  # Adjust padding if needed

    combobox = ttk.Combobox(frame, values=get_available_resolutions())
    combobox.bind("<<ComboboxSelected>>",lambda event: on_select(event, combobox)) 
    combobox.grid(row=1, column=0, columnspan=2, pady=10)  # Place combobox in row 1
    #* default resolution
    default_resolution = "1920x1080"
    combobox.set(default_resolution)
    
    #combobox.pack(pady=10, padx=10)
    btn_apply = ttk.Button(frame, text="Apply", compound=tk.LEFT, command=lambda: apply_changes(lbl_status))
    btn_apply.grid(row=2, column=0, pady=(10, 0))  # Place Apply button in row 2
    
    btn_unapply = ttk.Button(frame, text="Unapply", compound=tk.LEFT, command=lambda: unapply_changes(lbl_status, combobox))
    btn_unapply.grid(row=2, column=1, pady=(10, 0))  # Place Unapply button in row 2
    
   

    root.mainloop()

#! main loop
if __name__ == "__main__":
    #print(get_available_resolutions())
    #set_resolution(1920, 1080)
    gui()