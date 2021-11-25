import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk

import midisw.gtk3

if __name__== "__main__":
    win = Gtk.Window()

    pad = midisw.gtk3.XYPad()

    win.add(pad)

    win.set_size_request(128,128)
    win.connect("destroy",Gtk.main_quit)

    win.show_all()
    Gtk.main()
