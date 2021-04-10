
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk

import midisw.gtk3

if __name__=="__main__":
    def print_note(widget, ev):
        print("#get_note_number = %d"%widget.get_note())
        print("#get_note_range = %d,%d"%widget.get_note_range())

    top = Gtk.Window()
    top2 = Gtk.Window()

    p1 = midisw.gtk3.PianoNoteRangeSelector(octave = 4, octave_offset = 3)
    p1.connect("button_press_event",print_note)

    p2 = midisw.gtk3.PianoNoteRangeSelector(octave = 2, octave_offset = 0,orientation=Gtk.Orientation.VERTICAL)
    p2.connect("button_press_event",print_note)


    top.add(p1)
    top.set_size_request(720,120)
    top.connect("destroy",Gtk.main_quit)

    top2.add(p2)
    top2.set_size_request(120,720)
    top2.connect("destroy",Gtk.main_quit)

    top.show_all()
    top2.show_all()
    Gtk.main()
