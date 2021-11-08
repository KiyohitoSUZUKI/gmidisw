#!/usr/bin/env python3

# Gtk related libraries
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk

import midisw.mididefs
import midisw.gtk3.piano
import midisw.gtk3.dial
import midisw.gtk3.synth_toggle
import midisw.gtk3.synth_xy_pad

# MIDI Libs.
import rtmidi2

#######################################################################
#######################################################################
class TheMidiOut(object):
    def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)
        #
        # setup event hndler
        #
        self.midi_out = rtmidi2.MidiOut().open_virtual_port("mstkbd")
        self.virt_out_port = self.midi_out.open_port()

THE_MIDI_OUT = TheMidiOut().virt_out_port

#######################################################################
#######################################################################
class ThePiano(midisw.gtk3.PianoNoteSelector):
    def __init__(self, *args, **kwargs):
        super().__init__(*args,**kwargs)

        self.last_pressed = None
        self.connect("button_press_event", self.button_press_event)
        self.connect("motion_notify_event", self.motion_notify_event)
        self.connect("button_release_event", self.button_release_event)
        self.set_size_request(1280,120)

    def button_press_event(self,widget,event):
        note = self.get_note()            
        THE_MIDI_OUT.send_noteon(0,note,127)
        self.last_pressed = note

    def motion_notify_event(self,widget,event):
        note = self.get_note();
        if self.last_pressed != note:
            THE_MIDI_OUT.send_noteoff(0,self.last_pressed)
        THE_MIDI_OUT.send_noteon(0,note,127)
        self.last_pressed = note

    def button_release_event(self,widget,event):
        THE_MIDI_OUT.send_noteoff(0,self.last_pressed)
        self.last_pressed = None

#######################################################################
class TheXYPad(midisw.gtk3.SynthXYPad):
    def __init__(self,*args,**kwargs):
        super().__init__(*args, **kwargs)
        self.set_size_request(120,120)
        

#######################################################################
#######################################################################
class MstKbdWin(Gtk.Window):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        #
        # bottom widgets
        #
        self.vbox = Gtk.VBox()
        self.add(self.vbox)
        ## basic widgets
        self.hbox1 = Gtk.HBox()
        self.hbox1_widgets = {
            "TheXYPad" : TheXYPad(),
            "ThePiano" : ThePiano(),
            "sustain" : midisw.gtk3.SynthToggle(),
            "all_note_off" : Gtk.Button(label="Panic")
        }
        for w in self.hbox1_widgets.values():
            self.hbox1.add(w)

        self.vbox.add(self.hbox1)
            
        ## ToDO: need add port/bank/prg/selectorbox

        self.connect("destroy",Gtk.main_quit)
        self.show_all()
#######################################################################
#######################################################################

if __name__== "__main__":
    mkw = MstKbdWin(title="TheMIDIMaster")
    #mkw.set_size_request(1024,240)
    Gtk.main()
