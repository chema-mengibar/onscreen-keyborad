import Tkinter as tk
import ttk
import time
import win32gui
import win32api
import win32con
import re
from functools import partial

VK_CODE = {
  'shift':0x10,
  'ctrl':0x11,
  'alt':0x12,
  'enter':0x0D,
  'left_arrow':0x25,
  'up_arrow':0x26,
  'right_arrow':0x27,
  'down_arrow':0x28,
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
  'x':0x58,
  'y':0x59,
  'v':0x56,
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
  '+':0xBB,
  ',':0xBC,
  '-':0xBD,
  '.':0xBE,
  '/':0xBF,
  '[':0xDB,
  ']':0xDD,
}


class WindowMgr:

  def __init__ (self):
    self._handle = None
  
  def getHandle(self):
    return self._handle

  def _window_enum_callback(self, hwnd, wildcard):
    """Pass to win32gui.EnumWindows() to check all the opened windows"""
    if re.match(wildcard, str(win32gui.GetWindowText(hwnd))) is not None:
        self._handle = hwnd

  def find_window_wildcard(self, wildcard):
    self._handle = None
    win32gui.EnumWindows(self._window_enum_callback, wildcard)

  def set_foreground(self):
    win32gui.SetForegroundWindow(self._handle)

# -------------------------------------------------------------

root = tk.Tk()
w = WindowMgr()
w.find_window_wildcard(".*Affini.*")

# -------------------------------------------------------------
#  
class Panel:
  def __init__ (self):
    self.starte = True

  def action_back(self):
    w.set_foreground()
    win32api.keybd_event(VK_CODE['ctrl'], 0,0,0)
    time.sleep(0.1)
    win32api.keybd_event(VK_CODE['z'], 0,0,0)

  def action_repeat(self):
    w.set_foreground()
    win32api.keybd_event(VK_CODE['ctrl'], 0,0,0)
    time.sleep(0.1)
    win32api.keybd_event(VK_CODE['y'], 0,0,0)

  def action_brush_inc(self):
    w.set_foreground()
    win32api.keybd_event(VK_CODE['up_arrow'], 0,0,0)

  def action_brush_inc_10(self):
    w.set_foreground()
    for i in range(0,10):
      win32api.keybd_event(VK_CODE['up_arrow'], 0,0,0)
      time.sleep(0.01)

  def action_brush_dec(self):
    w.set_foreground()
    win32api.keybd_event(VK_CODE['down_arrow'], 0,0,0)

  def action_brush_dec_10(self):
    w.set_foreground()
    for i in range(0,10):
      win32api.keybd_event(VK_CODE['down_arrow'], 0,0,0)
      time.sleep(0.01)
      
  def action_num(self, num ):
    w.set_foreground()
    win32api.keybd_event(VK_CODE['numpad_' + str(num)], 0,0,0)
    self.enter_event()
      
  def action_value(self, num ):
    w.set_foreground()
    # win32api.SendMessage(w.getHandle(),win32con.WM_SETTEXT,None, num) 
    letters = list(str(num))
    for l in letters:
      win32api.keybd_event(VK_CODE[l], 0,0,0)
      time.sleep(0.05)
    self.enter_event()

  def enter_event(self):
    win32api.keybd_event( VK_CODE['enter'], 0, win32con.KEYEVENTF_EXTENDEDKEY, 0) #press
    win32api.Sleep(50)
    win32api.keybd_event( VK_CODE['enter'], 0, win32con.KEYEVENTF_EXTENDEDKEY | win32con.KEYEVENTF_KEYUP, 0) 

  def click(self, key):
    win32api.keybd_event(VK_CODE[key], 0,0,0)

# -------------------------------------------------------------

p = Panel()

# -------------------------------------------------------------


buttons = [
  {'label':'Back', 'click': p.action_back },
  {'label':'Repeat', 'click': p.action_repeat },
  {'label':'Brush +1', 'click': p.action_brush_inc },
  {'label':'Brush +10', 'click': p.action_brush_inc_10 },
  {'label':'Brush -1', 'click': p.action_brush_dec },
  {'label':'Brush -10', 'click': p.action_brush_dec_10 },
]


lf = tk.LabelFrame(root, text=" keypad ", bd=3)
lf.pack(padx=100, pady=10)

# Panel Buttons: actions

idx = 0
col = 0
row = 1

buttonsPanel = []
for item in buttons:
  cmd = partial( buttons[idx]['click'])
  btn =  tk.Button(lf, text=buttons[idx]['label'], width=5, takefocus = 0, command= cmd )
  buttonsPanel.append( btn )
  buttonsPanel[idx].grid(row=row, column=col)
  idx += 1
  col += 1


# Panel Buttons: Numpad

col = 0
row = 2

for item in range(1,10):
  cmd = partial( p.action_num, item)
  btn =  tk.Button(lf, text=item, width=5, takefocus = 0, command= cmd )
  buttonsPanel.append( btn )
  buttonsPanel[idx].grid(row=row, column=col)
  idx += 1
  col += 1

# Panel Buttons: Numpad

col = 0
row = 3

for item in range(10,110,10):
  cmd = partial( p.action_value, item)
  btn =  tk.Button(lf, text=item, width=5, takefocus = 0, command= cmd )
  buttonsPanel.append( btn )
  buttonsPanel[idx].grid(row=row, column=col)
  idx += 1
  col += 1


# Ext Buttons: Numpad

col = 0
row = 4
idxB = 0

buttons_ext = [
  {'label':'Ctrl', 'key': 'ctrl', 'click': p.click },
  # {'label':'Shift', 'key': 'shift', 'click': p.click },
  {'label':'Alt', 'key': 'shift', 'click': p.click },
]
for item in buttons_ext:
  cmd = partial( buttons_ext[idxB]['click'], buttons_ext[idxB]['key'] )
  btn =  tk.Button(lf, text=buttons_ext[idxB]['label'], width=5, takefocus=0, command=cmd )
  buttonsPanel.append( btn )
  buttonsPanel[idx].grid(row=row, column=col)
  idx += 1
  idxB += 1
  col += 1


for b in buttonsPanel:
  b.config( height =2, width = 20 )

root.mainloop()