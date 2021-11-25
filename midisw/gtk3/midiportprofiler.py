import logging

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk

import midisw.synth
import midisw.util
import midisw.midiport

########################################################
class MIDIPortProfiler(Gtk.VBox):
    WIDTH=320
    HEIGHT=640

    def __init__(self, *args, portdef = midisw.midiport.MIDIPort() ,**kwargs):
        super().__init__(*args, **kwargs)
        self.set_size_request(self.WIDTH, self.HEIGHT)
        self.portdef = portdef
        self.lstore = {}
        for n in self.portdef.port_names:
            self._draw_ports(n)

    def _draw_ports(self, port_type: str):
        hlbl = Gtk.Label()
        hlbl.set_text(port_type)
        self.pack_start(hlbl, False, False, 0)

        scrw = Gtk.ScrolledWindow()
        self.pack_start(scrw, True, True, 0)
        
        self.lstore[port_type] = Gtk.ListStore(str,str)
        for nm in self.portdef.port_names[port_type]:
            self.lstore[port_type].append([ nm, self.portdef.port_profiles[port_type][nm]["name"] ])

        tview = Gtk.TreeView(model = self.lstore[port_type])
        scrw.add(tview)

        rendtxt = Gtk.CellRendererText()
        col = Gtk.TreeViewColumn("portname")
        col.set_property("resizable", True)
        col.pack_start(rendtxt, True)
        col.add_attribute(rendtxt, "text", 0)
        tview.append_column(col)

        lstorecombo = Gtk.ListStore(str)
        if port_type == "jack/midi/input":
            tgtlst = self.portdef.synth_profiles.ls_writable()
        else:
            tgtlst = self.portdef.synth_profiles.ls_readable()

        for pr in tgtlst:
            lstorecombo.append([pr["name"]])
        rendcombo = Gtk.CellRendererCombo()
        rendcombo.set_property("editable", True)
        rendcombo.set_property("model", lstorecombo)
        rendcombo.set_property("text-column", 0)
        colcombo = Gtk.TreeViewColumn("port profile")
        colcombo.set_property("resizable", True)
        colcombo.pack_start(rendcombo, False)
        colcombo.add_attribute(rendcombo, "text", 1)
        tview.append_column(colcombo)
        if port_type == "jack/midi/input":
            rendcombo.connect("edited", self.on_combo_changed_input)
        else:
            rendcombo.connect("edited", self.on_combo_changed_output)

    def on_combo_changed_input(self, widget, path, text):
        self.lstore["jack/midi/input"][path][1] = text

    def on_combo_changed_output(self, widget, path, text):
        self.lstore["jack/midi/output"][path][1] = text

########################################################
if __name__=="__main__":

    midi_ports = midisw.midiport.MIDIPort()

    top = Gtk.Window()
    ppt = MIDIPortProfiler(portdef = midi_ports)
    top.add(ppt)
    top.show_all()
    Gtk.main()
    pass
