import win32api
import win32con
import pywintypes
import tkinter as tk
from tkinter import ttk

def get_available_resolutions():
    resolutions = set()  # Use a set to avoid duplicate entries
    display_device = win32api.EnumDisplayDevices()
    
    i = 0
    while True:
        try:
            device_name = win32api.EnumDisplayDevices(None, i)
            if not device_name.DeviceName:
                break
            
            mode_num = 0
            while True:
                try:
                    mode = win32api.EnumDisplaySettings(device_name.DeviceName, mode_num)
                    resolution = f"{mode.PelsWidth}x{mode.PelsHeight}"
                    resolutions.add(resolution)
                    mode_num += 1
                except pywintypes.error:
                    break
            i += 1
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
        
def gui():
    root = tk.Tk()
    root.title("ValorantTS_HI")
    root.geometry("300x300")

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
    btn_apply = ttk.Button(frame, text="Apply", compound=tk.LEFT )# command=apply_changes)
    btn_apply.grid(row=2, column=0, pady=(10, 0))  # Place Apply button in row 2
    
    btn_unapply = ttk.Button(frame, text="Unapply", compound=tk.LEFT)# command=unapply_changes)
    btn_unapply.grid(row=2, column=1, pady=(10, 0))  # Place Unapply button in row 2
    
   

    root.mainloop()


if __name__ == "__main__":
    #print(get_available_resolutions())
    #set_resolution(1920, 1080)
    gui()