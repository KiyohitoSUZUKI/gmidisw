import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk

import midisw.gtk3

##########################################################################
class Layer(Gtk.VBox):
    PIANO_WIDTH = 480
    PIANO_HEIGHT = 32
    def __init__(self,  **kwargs):
        super().__init__(**kwargs)

        self.portinfof = Gtk.HBox()
        self.pack_start(self.portinfof, False, False, 0)

        # dismissbutton
        self.dismiss_button = Gtk.Button()
        self.dismiss_button.set_label("X")
        self.dismiss_button.connect("clicked", self.on_dismiss_button_clicked)
        self.portinfof.pack_start(self.dismiss_button, False, False, 0)

        # port selection/portprofile information
        self.portsel = midisw.gtk3.PortSelector(port_type="jack/midi/input")
        self.portinfof.pack_start(self.portsel, True, True, 0)

        self.portlabel = Gtk.Label()
        self.portlabel.set_text("port-information")
        self.portinfof.pack_start(self.portlabel, True, True, 0)

        # channel
        self.chf = Gtk.VBox()
        self.chlabel = Gtk.Label()
        self.chlabel.set_text("channel")
        self.chadj = Gtk.Adjustment(value=0, lower=0, upper=15, step_increment=1)
        self.ch = Gtk.SpinButton()
        self.ch.set_adjustment(self.chadj)
        self.ch.set_wrap(True)
        self.ch.set_size_request(32,16)

        self.chf.add(self.chlabel)
        self.chf.add(self.ch)
        self.portinfof.pack_start(self.chf, False, False, 2)

        #
        # port parameters
        #
        params={"volume":96, "pan": 64,
                "cutoff": 64, "resonance": 32,
                "reverb": 64, "chorus": 64}
        self.portparamf = Gtk.HBox()
        self.pack_start(self.portparamf, False, False, 0)

        self.param_widget={}
        for k in params.keys():
            self.param_widget[k] = self.volume = midisw.gtk3.DialWithSpin(label=k, initial_value=params[k])
            self.param_widget[k].set_size_request(64,128)
            self.portparamf.pack_start(self.param_widget[k], True, True, 0)

        # tone-select

        #
        # range selection 
        #
        self.piano = midisw.gtk3.PianoNoteRangeSelector()
        self.piano.set_size_request(self.PIANO_WIDTH,self.PIANO_HEIGHT)
        self.pack_start(self.piano, False,False,0)

    def on_dismiss_button_clicked(self, widget):
        self.destroy()
##########################################################################
class LayerStack(Gtk.VBox):
    WIDTH = 640
    HEIGHT = 768

    def __init__(self,  **kwargs):
        super().__init__(**kwargs)

        self.add_button = Gtk.Button()
        self.add_button.set_label("Create New Layer")
        self.add_button.connect("clicked", self.on_add_button_clicked)
        self.pack_start(self.add_button, False, True, 0)        
        self.scrollw = Gtk.ScrolledWindow()
        self.pack_start(self.scrollw, True, True, 0)
        self.layervbox = Gtk.VBox()
        self.scrollw.add(self.layervbox)

        self.set_size_request(self.WIDTH, self.HEIGHT)

    def on_add_button_clicked(self, widget):
        new_layer = Layer()
        self.layervbox.pack_start(new_layer, False, False, 0)
        self.show_all()

##########################################################################
if __name__=="__main__":
    top = Gtk.Window()
    layer_stack = LayerStack()

    top.add(layer_stack)
    
    top.connect("destroy", Gtk.main_quit)
    top.show_all()
    Gtk.main()
    pass
    
