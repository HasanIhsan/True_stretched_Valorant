import win32api
import win32con
import pywintypes
import ctypes
import tkinter as tk
from tkinter import ttk
 
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

    
    # Convert resolutions to a list of tuples (width, height)
    resolution_tuples = []
    for res in resolutions:
        width, height = map(int, res.split('x'))
        resolution_tuples.append((width, height))

    # Sort by area (width * height) in descending order
    sorted_resolutions = sorted(resolution_tuples, key=lambda x: x[0] * x[1], reverse=True)
    
    # Convert back to formatted strings
    sorted_resolution_strings = [f"{width}x{height}" for width, height in sorted_resolutions]

    return sorted_resolution_strings


def set_resolution(width, height):
    devmode = pywintypes.DEVMODEType()
    devmode.PelsWidth = width
    devmode.PelsHeight = height
    devmode.Fields = win32con.DM_PELSWIDTH | win32con.DM_PELSHEIGHT

    result = win32api.ChangeDisplaySettings(devmode, 0)
    if result == win32con.DISP_CHANGE_SUCCESSFUL:
        print("Resolution changed successfully.")
    elif result == win32con.DISP_CHANGE_RESTART:
        print("You need to restart your computer for the changes to take effect.")
    else:
        print("Failed to change resolution.")
        
def on_select(event, combo):
    selected_resolution = combo.get()
    print(f"Selected resolution: {selected_resolution}")
    
    
    
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
        print(f"Width: {width}")
        print(f"Height: {height}")
       # print(f"Resulting Array: {reslo}")
        
        set_resolution(int(width), int(height))
    #set_resolution()
        
# apply button
def apply_changes(lbl_status):
    window_title = "VALORANT  "
    global original_style
    window_handle = ctypes.windll.user32.FindWindowW(None, window_title)
    if window_handle == 0:
        lbl_status.config(text="Valorant not found")
    else:
        original_style = ctypes.windll.user32.GetWindowLongW(window_handle, ctypes.c_int(-16))
        new_style = original_style & ~0x00800000 & ~0x00040000
        ctypes.windll.user32.SetWindowLongW(window_handle, ctypes.c_int(-16), new_style)
        ctypes.windll.user32.ShowWindow(window_handle, ctypes.c_int(3))
        lbl_status.config(text="True stretched applied")
     
   
        
#gui        
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
    #combobox.pack(pady=10, padx=10)
    btn_apply = ttk.Button(frame, text="Apply", compound=tk.LEFT, command=lambda: apply_changes(lbl_status))
    btn_apply.grid(row=2, column=0, pady=(10, 0))  # Place Apply button in row 2
    
    btn_unapply = ttk.Button(frame, text="Unapply", compound=tk.LEFT)# command=unapply_changes)
    btn_unapply.grid(row=2, column=1, pady=(10, 0))  # Place Unapply button in row 2
    
   

    root.mainloop()

# main loop
if __name__ == "__main__":
    #print(get_available_resolutions())
    #set_resolution(1920, 1080)
    gui()