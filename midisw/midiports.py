
import rtmidi

def get_in_ports():
    return rtmidi.MidiIn().get_ports()

def get_out_ports():
    return rtmidi.MidiOut().get_ports()
