import ctypes
import ctypes.wintypes

class DEVMODE(ctypes.Structure):
    _fields_ = [
        ("dmDeviceName", ctypes.c_wchar * 32),
        ("dmSpecVersion", ctypes.c_ushort),
        ("dmDriverVersion", ctypes.c_ushort),
        ("dmSize", ctypes.c_ushort),
        ("dmDriverExtra", ctypes.c_ushort),
        ("dmFields", ctypes.c_ulong),
        ("dmPositionX", ctypes.c_long),
        ("dmPositionY", ctypes.c_long),
        ("dmDisplayOrientation", ctypes.c_ulong),
        ("dmDisplayFixedOutput", ctypes.c_ulong),
        ("dmColor", ctypes.c_short),
        ("dmDuplex", ctypes.c_short),
        ("dmYResolution", ctypes.c_short),
        ("dmTTOption", ctypes.c_short),
        ("dmCollate", ctypes.c_short),
        ("dmFormName", ctypes.c_wchar * 32),
        ("dmLogPixels", ctypes.c_ushort),
        ("dmBitsPerPel", ctypes.c_ulong),
        ("dmPelsWidth", ctypes.c_ulong),
        ("dmPelsHeight", ctypes.c_ulong),
        ("dmDisplayFlags", ctypes.c_ulong),
        ("dmDisplayFrequency", ctypes.c_ulong),
        ("dmICMMethod", ctypes.c_ulong),
        ("dmICMIntent", ctypes.c_ulong),
        ("dmMediaType", ctypes.c_ulong),
        ("dmDitherType", ctypes.c_ulong),
        ("dmReserved1", ctypes.c_ulong),
        ("dmReserved2", ctypes.c_ulong),
        ("dmPanningWidth", ctypes.c_ulong),
        ("dmPanningHeight", ctypes.c_ulong)
    ]

def list_supported_resolutions():
    user32 = ctypes.windll.user32
    devmode = DEVMODE()
    devmode.dmSize = ctypes.sizeof(DEVMODE)
    mode_num = 0
    resolutions = []

    while user32.EnumDisplaySettingsW(None, mode_num, ctypes.byref(devmode)):
        resolutions.append((devmode.dmPelsWidth, devmode.dmPelsHeight, devmode.dmDisplayFrequency))
        mode_num += 1

    return resolutions

def set_resolution(width, height):
    user32 = ctypes.windll.user32
    devmode = DEVMODE()
    devmode.dmSize = ctypes.sizeof(DEVMODE)
    
    if not user32.EnumDisplaySettingsW(None, 0, ctypes.byref(devmode)):
        raise ctypes.WinError()
    
    devmode.dmPelsWidth = width
    devmode.dmPelsHeight = height
    devmode.dmBitsPerPel = 32  # Assuming 32-bit color depth
    devmode.dmDisplayFrequency = 60  # Assuming 60Hz refresh rate
    devmode.dmFields = 0x00080000 | 0x00040000 | 0x00800000 | 0x00400000  # DM_PELSWIDTH | DM_PELSHEIGHT | DM_BITSPERPEL | DM_DISPLAYFREQUENCY
    
    result = user32.ChangeDisplaySettingsW(ctypes.byref(devmode), 0)
    
    if result == 0:
        print("Resolution changed successfully.")
    elif result == 1:
        print("The computer must be restarted for the graphics mode to work.")
    elif result == -1:
        print("The display driver failed the specified graphics mode.")
    elif result == -2:
        print("The graphics mode is not supported.")
    elif result == -3:
        print("Unable to write settings to the registry.")
    elif result == -4:
        print("An error was detected in the current settings.")
    else:
        raise ctypes.WinError(result)

if __name__ == "__main__":
    resolutions = list_supported_resolutions()
    print("Supported Resolutions:")
    for res in resolutions:
        print(f"{res[0]}x{res[1]} @ {res[2]}Hz")

    try:
        # Replace with a supported resolution
        set_resolution(1024, 768)
    except Exception as e:
        print(f"Failed to change resolution: {e}")
