import sys
import os
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

import tkinter as tk
from gui.main_window import MainWindow

if __name__ == '__main__':
    root = tk.Tk()
    app = MainWindow(root)
    root.mainloop()

