import rtmidi2

print("##------------------------------ initialize-ports")

midi_in = rtmidi2.MidiIn().open_virtual_port("test-In-port")
midi_out = rtmidi2.MidiOut().open_virtual_port("test-Out-port")

print("#in-ports: ",rtmidi2.MidiIn().ports)
print("#out-ports: ",rtmidi2.MidiOut().ports)


print("##----------------------- import custom modules")
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk

import midisw.mididefs
import midisw.gtk3.piano

print("##------------------------------------ open port")

virt_out_port = midi_out.open_port()
last_pressed = None

print("##------------------------------------ def GUI and loop")

def do_note_on(widget,ev):
    global virt_out_port, last_pressed

    note = widget.get_note()

    print("##noteon!:%d"%note)
    virt_out_port.send_noteon(0,note,127)
    last_pressed = note


def do_motion_notified(widget,ev):
    global virt_out_port, last_pressed

    note = widget.get_note()

    if last_pressed != note:
        print("##noteoff:%d"%last_pressed)
        virt_out_port.send_noteoff(0,last_pressed)
        print("##noteon!:%d"%note)
        virt_out_port.send_noteon(0,note,127)

        last_pressed = note
    else:
        pass

def do_note_off(widget,ev):
    global virt_out_port, last_pressed

    print("##noteoff:%d"%last_pressed)
    virt_out_port.send_noteoff(0,last_pressed)


piano = midisw.gtk3.PianoNoteSelector()
piano.connect("button_press_event",do_note_on)
piano.connect("motion_notify_event",do_motion_notified)
piano.connect("button_release_event",do_note_off)

win = Gtk.Window()

win.set_size_request(1024,120)

win.add(piano)
win.show_all()
win.connect("destroy",Gtk.main_quit)

Gtk.main()

