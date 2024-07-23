import win32api
import win32con
import pywintypes

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
                    resolution = f"{mode.DeviceName} - {mode.PelsWidth}x{mode.PelsHeight}"
                    resolutions.add(resolution)
                    mode_num += 1
                except pywintypes.error:
                    break
            i += 1
        except pywintypes.error:
            break

    return list(resolutions)


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
        
        
if __name__ == "__main__":
    print(get_available_resolutions())
    set_resolution(1920, 1080)