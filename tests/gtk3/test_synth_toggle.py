import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk

import midisw.gtk3

if __name__== "__main__":
    print("#")
    win = Gtk.Window()

    #btn = midisw.gtk3.SynthToggle()
    #btn = SynthToggle()
    #btn = SynthToggleWithLabel(label="The Toggle\nHellohello")
    # btn = SynthToggleWithLabel(label="The Toggle Hello/hello # # # # # ## # ## ## # ##")

    a = ["tone%02d"%i for i in range(0,64)]
    btnset = midisw.gtk3.SynthToggleBox(label="TheFrame", labels=a)

    win.add(btnset)

    win.set_size_request(320,512)
    win.connect("destroy",Gtk.main_quit)

    win.show_all()
    Gtk.main()
