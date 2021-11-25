import re
import logging

from functools import lru_cache

import midisw.envdefs

import midisw.util
import midisw.profile

########################################################
########################################################
class MIDIPort(object):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.port_names = {}
        self.refresh_ports()
        self.port_profiles = {}
        self.synth_profiles = midisw.Synth()
        self.apply_guess()

    def refresh_ports(self):
        for ptype in ["jack/midi/input", "jack/midi/output"]:
            self.port_names[ptype] = {}
            for p in midisw.util.lsport(ptype):
                self.port_names[ptype][p]=p
        
    def apply_guess(self):
        for ptype in ["jack/midi/input", "jack/midi/output"]:
            self.port_profiles[ptype] = {}
            for portname in self.port_names[ptype]:
                scanproflst = []
                if ptype == "jack/midi/input":
                    scanproflst =  self.synth_profiles.ls_writable()
                else:
                    scanproflst =  self.synth_profiles.ls_readable()

                for prof in scanproflst:
                    if "jackname" in prof and prof["jackname"] in portname:
                        self.port_profiles[ptype][portname] = prof
                    
                if not portname in self.port_profiles[ptype]:
                    self.port_profiles[ptype][portname] = midisw.profile.apply_default("synth", {})

###########################################################

