import Tkinter as tk
import ttk
from functools import partial
from ctypes import *
import win32gui
import win32api
import win32con
import re
import time
import win32com.client as comclt

VK_CODE = {
    'backspace':0x08,
    'tab':0x09,
    'clear':0x0C,
    'enter':0x0D,
    'shift':0x10,
    'ctrl':0x11,
    'alt':0x12,
    'pause':0x13,
    'caps_lock':0x14,
    'esc':0x1B,
    'spacebar':0x20,
    'page_up':0x21,
    'page_down':0x22,
    'end':0x23,
    'home':0x24,
    'left_arrow':0x25,
    'up_arrow':0x26,
    'right_arrow':0x27,
    'down_arrow':0x28,
    'select':0x29,
    'print':0x2A,
    'execute':0x2B,
    'print_screen':0x2C,
    'ins':0x2D,
    'del':0x2E,
    'help':0x2F,
    '0':0x30,
    '1':0x31,
    '2':0x32,
    '3':0x33,
    '4':0x34,
    '5':0x35,
    '6':0x36,
    '7':0x37,
    '8':0x38,
    '9':0x39,
    'a':0x41,
    'b':0x42,
    'c':0x43,
    'd':0x44,
    'e':0x45,
    'f':0x46,
    'g':0x47,
    'h':0x48,
    'i':0x49,
    'j':0x4A,
    'k':0x4B,
    'l':0x4C,
    'm':0x4D,
    'n':0x4E,
    'o':0x4F,
    'p':0x50,
    'q':0x51,
    'r':0x52,
    's':0x53,
    't':0x54,
    'u':0x55,
    'v':0x56,
    'w':0x57,
    'x':0x58,
    'y':0x59,
    'z':0x5A,
    'numpad_0':0x60,
    'numpad_1':0x61,
    'numpad_2':0x62,
    'numpad_3':0x63,
    'numpad_4':0x64,
    'numpad_5':0x65,
    'numpad_6':0x66,
    'numpad_7':0x67,
    'numpad_8':0x68,
    'numpad_9':0x69,
    'multiply_key':0x6A,
    'add_key':0x6B,
    'separator_key':0x6C,
    'subtract_key':0x6D,
    'decimal_key':0x6E,
    'divide_key':0x6F,
    'F1':0x70,
    'F2':0x71,
    'F3':0x72,
    'F4':0x73,
    'F5':0x74,
    'F6':0x75,
    'F7':0x76,
    'F8':0x77,
    'F9':0x78,
    'F10':0x79,
    'F11':0x7A,
    'F12':0x7B,
    'F13':0x7C,
    'F14':0x7D,
    'F15':0x7E,
    'F16':0x7F,
    'F17':0x80,
    'F18':0x81,
    'F19':0x82,
    'F20':0x83,
    'F21':0x84,
    'F22':0x85,
    'F23':0x86,
    'F24':0x87,
    'num_lock':0x90,
    'scroll_lock':0x91,
    'left_shift':0xA0,
    'right_shift ':0xA1,
    'left_control':0xA2,
    'right_control':0xA3,
    'left_menu':0xA4,
    'right_menu':0xA5,
    'browser_back':0xA6,
    'browser_forward':0xA7,
    'browser_refresh':0xA8,
    'browser_stop':0xA9,
    'browser_search':0xAA,
    'browser_favorites':0xAB,
    'browser_start_and_home':0xAC,
    'volume_mute':0xAD,
    'volume_Down':0xAE,
    'volume_up':0xAF,
    'next_track':0xB0,
    'previous_track':0xB1,
    'stop_media':0xB2,
    'play/pause_media':0xB3,
    'start_mail':0xB4,
    'select_media':0xB5,
    'start_application_1':0xB6,
    'start_application_2':0xB7,
    'attn_key':0xF6,
    'crsel_key':0xF7,
    'exsel_key':0xF8,
    'play_key':0xFA,
    'zoom_key':0xFB,
    'clear_key':0xFE,
    '+':0xBB,
    ',':0xBC,
    '-':0xBD,
    '.':0xBE,
    '/':0xBF,
    '`':0xC0,
    ';':0xBA,
    '[':0xDB,
    '\\':0xDC,
    ']':0xDD,
    "'":0xDE,
    '`':0xC0
}


user32 = windll.user32
kernel32 = windll.kernel32

class RECT(Structure):
 _fields_ = [
     ("left", c_ulong),
     ("top", c_ulong),
     ("right", c_ulong),
     ("bottom", c_ulong)
 ]

class GUITHREADINFO(Structure):
 _fields_ = [
     ("cbSize", c_ulong),
     ("flags", c_ulong),
     ("hwndActive", c_ulong),
     ("hwndFocus", c_ulong),
     ("hwndCapture", c_ulong),
     ("hwndMenuOwner", c_ulong),
     ("hwndMoveSize", c_ulong),
     ("hwndCaret", c_ulong),
     ("rcCaret", RECT)
 ]

def GetCaretWindowText(hWndCaret, Selected = False): # As String

    startpos =0
    endpos =0

    txt = ""

    if hWndCaret:

        buf_size = 1 + win32gui.SendMessage(hWndCaret, win32con.WM_GETTEXTLENGTH, 0, 0)
        if buf_size:
            buffer = win32gui.PyMakeBuffer(buf_size)
            win32gui.SendMessage(hWndCaret, win32con.WM_GETTEXT, buf_size, buffer)
            txt = buffer[:buf_size]

        if Selected and buf_size:
            selinfo  = win32gui.SendMessage(hWndCaret, win32con.EM_GETSEL, 0, 0)
            endpos   = win32api.HIWORD(selinfo)
            startpos = win32api.LOWORD(selinfo)
            return txt[startpos: endpos]

    return txt

def get_selected_text_from_front_window(): # As String
    ''' vb6 to python translation '''

    gui = GUITHREADINFO(cbSize=sizeof(GUITHREADINFO))
    txt=''
    ast_Clipboard_Obj=None
    Last_Clipboard_Temp = -1


    user32.GetGUIThreadInfo(0, byref(gui))

    txt = GetCaretWindowText(gui.hwndCaret, True)

    '''
    if Txt = "" Then
        LastClipboardClip = ""
        Last_Clipboard_Obj = GetClipboard
        Last_Clipboard_Temp = LastClipboardFormat
        SendKeys "^(c)"
        GetClipboard
        Txt = LastClipboardClip
        if LastClipboardClip <> "" Then Txt = LastClipboardClip
        RestoreClipboard Last_Clipboard_Obj, Last_Clipboard_Temp
        print "clbrd: " + Txt
    End If
    '''    
    return txt


class WindowMgr:
    """Encapsulates some calls to the winapi for window management"""

    def __init__ (self):
        """Constructor"""
        self._handle = None

    def find_window(self, class_name, window_name=None):
        """find a window by its class_name"""
        self._handle = win32gui.FindWindow(class_name, window_name)

    def _window_enum_callback(self, hwnd, wildcard):
        """Pass to win32gui.EnumWindows() to check all the opened windows"""
        if re.match(wildcard, str(win32gui.GetWindowText(hwnd))) is not None:
            self._handle = hwnd

    def find_window_wildcard(self, wildcard):
        """find a window whose title matches the wildcard regex"""
        self._handle = None
        win32gui.EnumWindows(self._window_enum_callback, wildcard)

    def set_foreground(self):
        """put the window in the foreground"""
        win32gui.SetForegroundWindow(self._handle)

    def send_message(self, msg):
        """put the window in the foreground"""
        win32api.keybd_event(VK_CODE['ctrl'], 0,0,0)
        time.sleep(0.1)
        win32api.keybd_event(VK_CODE['n'], 0,0,0)

    def send_hello(self, msg):
        letters = list(msg)
        for l in letters:
            if l == ' ':
                l = 'spacebar'
            win32api.keybd_event(VK_CODE[l], 0,0,0)
            time.sleep(0.1)
        # win32api.keybd_event(VK_CODE['enter'], 0,0,0)
        # win32api.keybd_event( ord('\r') , 0,0,0)

        win32api.keybd_event( VK_CODE['enter'], 0, win32con.KEYEVENTF_EXTENDEDKEY, 0) #press
        win32api.Sleep(50)
        win32api.keybd_event( VK_CODE['enter'], 0, win32con.KEYEVENTF_EXTENDEDKEY | win32con.KEYEVENTF_KEYUP, 0) 

        time.sleep(0.5)

    def get_text(self):
        print(win32gui.GetWindowText(self._handle) )

def click(btn):

    w = WindowMgr()

    # w.find_window_wildcard(".*Affinity.*")
    w.find_window_wildcard(".*Whats.*")
    w.set_foreground()

    # time.sleep(1)
    # w.send_hello( 'hola')
    
    # time.sleep(5)
    w.get_text()
    print( get_selected_text_from_front_window() )



    # wsh= comclt.Dispatch("WScript.Shell")
    # wsh.AppActivate("Notepad") # select another application
    # wsh.SendKeys("a") # send the keys you want

    # win32api.PostMessage( w,win32con.WM_CHAR, ord('x'), 0)
    # win32gui.SendMessage(self._handle, win32con.WM_KEYUP,0,0) 
    # win32gui.SendMessage(self._handle, win32con.VK_RETURN,0,0) 

    # s = "Button %s clicked" % btn
    # root.title(s)
    
root = tk.Tk()
root['bg'] = 'green'
# create a labeled frame for the keypad buttons
# relief='groove' and labelanchor='nw' are default
lf = tk.LabelFrame(root, text=" keypad ", bd=3)
lf.pack(padx=1, pady=10)
# typical calculator button layout
btn_list = [
'7',  '8',  '9',  '*',  'C',
'4',  '5',  '6',  '/',  'M->',
'1',  '2',  '3',  '-',  '->M',
'0',  '.',  '=',  '+',  'neg' ]
# create and position all buttons with a for-loop
# r, c used for row, column grid values
r = 1
c = 0
n = 0
# list(range()) needed for Python3
btn = list(range(len(btn_list)))
for label in btn_list:
    # partial takes care of function and argument
    cmd = partial(click, label)
    # create the button
    btn[n] = tk.Button(lf, text=label, width=5, takefocus = 0, command=cmd)
    # position the button
    btn[n].grid(row=r, column=c)
    # increment button index
    n += 1
    # update row/column position
    c += 1
    if c > 4:
        c = 0
        r += 1
        
root.mainloop()
