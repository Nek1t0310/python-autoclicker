# python-autoclicker
autoclicker on python, different implementations

simple autoclicker which might come in handy in minecraft pvp :)

## Controls

* **`=`** — Toggle the clicker on/off (Pause).
* **`-`** — Stop the clicker and return to the console to change settings.
* **`Home`** — Exit the program completely.

## Technical tricks

* using WinApi function from ctypes for setting a time quantum:
  winmm = ctypes.windll.winmm
  winmm.timeBeginPeriod(1)
  winmm.timeEndPeriod(1)

## In plans

  * gradually create a convenient, customizable autoclicker and also make a GUI for it
