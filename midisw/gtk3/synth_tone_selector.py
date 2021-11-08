import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk

import midisw.mididefs

###############################################################

class ToneSelector(Gtk.Frame):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.port_name = ""
        self.port_num = 0
        self.curr_bank = 0
        self.curr_prg = 0

        
###############################################################
