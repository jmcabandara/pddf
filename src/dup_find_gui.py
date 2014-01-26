try:
    import tkinter
except:
    import Tkinter as tkinter

import gui.main_frame


if __name__ == '__main__':
    root = tkinter.Tk()
    root.title("Duplicate file finder")
    app = gui.main_frame.DupFinderWindow(master=root)
    app.mainloop()
