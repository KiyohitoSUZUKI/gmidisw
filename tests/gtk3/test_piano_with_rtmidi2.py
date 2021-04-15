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
import sys
print(sys.path)
sys.path.append("/home/kiyohito/lib/python")
import midisw.mididefs
import midisw.gtk3.piano

print("##------------------------------------ open port")

virt_out_port = midi_out.open_port()

print("##------------------------------------ def GUI and loop")

last_pressed = None
last_released = None

def do_note_on(widget,ev):
    global virt_out_port, last_pressed, last_released

    note = widget.get_note()

    print("##noteon!:%d"%note)
    virt_out_port.send_noteon(0,note,127)
    last_pressed = note
    last_released = None


def do_motion_notified(widget,ev):
    global virt_out_port, last_pressed, last_released

    note = widget.get_note()
    note_past = widget.get_note_past()

    if not last_pressed is None:
        if last_pressed != note:
            print("##noteoff:%d"%last_pressed)
            virt_out_port.send_noteoff(0,last_pressed)
            last_pressed = note

    if not last_released is None:
        if last_released != note_past:
            print("##noteon!:%d"%note)
            virt_out_port.send_noteon(0,note,127)
            last_released = note

def do_note_off(widget,ev):
    global virt_out_port, last_pressed, last_released

    note = widget.get_note_past()

    print("##noteoff:%d"%note)
    virt_out_port.send_noteoff(0,note)
    last_released = None
    last_pressed = None


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

