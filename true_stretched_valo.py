import win32api
import win32con
import pywintypes
import time
import json
import os

import tkinter as tk
from tkinter import ttk
from tkinter import filedialog 
 
#* hard coded default values (again will try to change this so the script automaticly gets the defualt reso) 
g_width = 1920
g_height = 1080 
g_folderPathGameSettings = ""

#!Function to create and update the JSON file
def cu_JSON(file_location, width=g_width, height=g_height):
    #* Define the path to the settings file
    settings_file = "settings.json"

    #* Check if settings.json exists in the current directory
    if not os.path.exists(settings_file):
        #* Create the JSON file with default values
        data = {
            "file_location": file_location,
            "width": width,
            "height": height
        }
        with open(settings_file, "w") as f:
            json.dump(data, f, indent=4)
            
        print("settings.json created with default values.")
    else:
        # Load the existing settings
        with open(settings_file, "r") as f:
            data = json.load(f)
        
        # Update the settings with new values
        data["file_location"] = file_location
        data["width"] = width
        data["height"] = height

        # Save the updated settings back to the file
        with open(settings_file, "w") as f:
            json.dump(data, f, indent=4)
            
        print("settings.json updated.")
    
 
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

 
   
        
#! Function to apply the selected resolution and hide the window
def apply_changes(lbl_status):
    global g_width, g_height
    
    
    #* change monitor resolution
    set_resolution(g_width, g_height)
    #print(f"width = {g_width}")
    #print(f"height = {g_height}")
    
    time.sleep(1) #delay for 2 seconds
    #( make windowed application fullscreen)
    lbl_status.config(text="Changed Monitor resolution to stretched")
    
#! Function to return monitor resolution to 1920x1080 and to show valorants window
#TODO: update this so the user can input there own default resoloution or add a slight function to get the monitor defualt reso
def unapply_changes(lbl_status):
  
    lbl_status.config(text="Change Monitor resolution to default") 
    
    #set monitor resolution to default of (1920 x 1080):
    #maybe in a future update i'll make it so the user can first set there defualt values
    time.sleep(1) # sleep for 2 seconds
    
    set_resolution(1920, 1080) # default resolution
    
    #change the combobox defualt selected resolution
    #default_resolution = "1920x1080"
    #combobox.set(default_resolution)

#! Function which holds the settings gui/ functions
 #TODO: so i will add a JSON file for settings to modify this so it will get the settings from the json file
def settings_Button():
    
    
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
            
    
            g_width = int(width)
            g_height = int(height)
            
            print(g_height)
            print(g_width)
            #set_resolution(int(width), int(height))
        return width, height
            
            
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


    #! Function for the modify button
    def modify_btn(lbl_status):
        lbl_status.config(text="File modified")
        
        #TODO: on start up create a JSON file with defualt settings
        #* the file will hold
        # settingsLocation :directorypath
        # rWidth: the stretched width
        # rHeight: the stretched width 
        cu_JSON(g_folderPathGameSettings, g_width, g_height)
        
        
        
        
    # Create the main window
    root = tk.Tk()
    root.title("Settings")
    root.geometry("400x200")

    # Label for the main title
    title_label = tk.Label(root, text="Settings", font=("Arial", 14))
    title_label.pack(pady=5)

    # Frame for settings file location
    file_frame = tk.Frame(root)
    file_frame.pack(pady=5)

    file_label = tk.Label(file_frame, text="Settings file location:")
    file_label.grid(row=0, column=0, padx=5, sticky="w")

    file_entry = tk.Entry(file_frame, width=30)
    file_entry.grid(row=0, column=1, padx=5)

    # Function to open file dialog
    def select_file():
        global g_folderPathGameSettings
        
        folder_path = filedialog.askdirectory()
        file_entry.delete(0, tk.END)
        file_entry.insert(0, folder_path)
        
        g_folderPathGameSettings = folder_path
        
        

    file_button = tk.Button(file_frame, text="...", command=select_file)
    file_button.grid(row=0, column=2, padx=5)

    # Frame for preferred resolution
    resolution_frame = tk.Frame(root)
    resolution_frame.pack(pady=5)

    resolution_label = tk.Label(resolution_frame, text="Preferred resolution:")
    resolution_label.grid(row=0, column=0, padx=5, sticky="w")


    # Combo box for selecting resolution
    resolution_combo = ttk.Combobox(resolution_frame, values=get_available_resolutions())
    resolution_combo.bind("<<ComboboxSelected>>",lambda event: on_select(event, resolution_combo)) 
    resolution_combo.grid(row=0, column=2, padx=5)
    
    # default resolution
    default_resolution = "1920x1080"
    resolution_combo.set(default_resolution)
    
    lbl_status = ttk.Label(resolution_frame, text="")
    lbl_status.grid(row=1, column=0, padx=10)
    
    # Modify button
    modify_button = tk.Button(root, text="Modify", command=lambda: modify_btn(lbl_status))
    modify_button.pack(pady=10)

    root.mainloop()
        
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

    
    btn_settings = ttk.Button(frame, text="Settings", compound=tk.CENTER, command=lambda: settings_Button())
    btn_settings.grid(row=1, column=0, pady=(10, 0))  # Place Apply button in row 1
       
    btn_apply = ttk.Button(frame, text="Apply", compound=tk.LEFT, command=lambda: apply_changes(lbl_status))
    btn_apply.grid(row=2, column=0, pady=(10, 0))  # Place Apply button in row 2
    
    btn_unapply = ttk.Button(frame, text="Unapply", compound=tk.LEFT, command=lambda: unapply_changes(lbl_status))
    btn_unapply.grid(row=2, column=1, pady=(10, 0))  # Place Unapply button in row 2
    
   

    root.mainloop()
 

#! main loop
if __name__ == "__main__":
    gui()