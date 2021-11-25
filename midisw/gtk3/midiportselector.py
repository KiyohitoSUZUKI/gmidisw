import logging

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk

import midisw.util

########################################################

class PortSelector(Gtk.ComboBoxText):
    def __init__(self, port_type="jack", **kwargs):
        super().__init__(**kwargs)
        self.port_type = port_type
        self.set_entry_text_column(0)
        self.refresh_list()

    def refresh_list(self):
        self.remove_all()
        for p in midisw.util.lsport(self.port_type):
            self.append_text(p)
        self.set_active(0)

########################################################
if __name__=="__main__":
    def on_changed(widget):
        print("## midisw.gtk3.PortSelector selected value="+widget.get_active_text() )
        
    top = Gtk.Window()
#    cb = PortSelector(port_type="jack/midi")
    cb = PortSelector(port_type="jack/midi/output")
    cb.connect("changed", on_changed)
    top.add(cb)
    top.connect("destroy", Gtk.main_quit)

    top.show_all()
    Gtk.main()
    pass

        
