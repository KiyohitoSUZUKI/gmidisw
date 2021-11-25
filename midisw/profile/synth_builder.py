
import re
import copy

import yaml

from midisw.envdefs import *
from midisw.util import *
from midisw.mididefs import *

import midisw.profile.util

from midisw.profile.modulevars import *
import midisw.tonenamedb

##########################################################################

PROFILE_DEFAULT['synth'] = f"""
type: "synth"
category: "synth"
name: "default-midi definition"

recv:
  ch: "0,15"
  notes: "0,127"
  message:
    { MIDI_MESSAGE_YAML }
  cc:
    { MIDI_CC_YAML }
  rpn:
    { MIDI_RPN_YAML }

send:
  ch: "0,15"
  notes: "0,127"
  message:
    { MIDI_MESSAGE_YAML }
  cc:
    { MIDI_CC_YAML }
  rpn:
    { MIDI_RPN_YAML }

tonenamedb:
tonenamecsv: ""
"""


PROFILE_DEFAULT['synth/fluidsynth'] = f"""
type: "synth/fluidsynth"
soundfont: ""
recv:
  ch: "0,15"
  notes: "0,127"
  message:
    0x80 : NOTE_OFF
    0x90 : NOTE_ON
    0xb0 : CONTROL_CHANGE
    0xc0 : PROGRAM_CHANGE
    0xe0 : PITCHBEND
  cc:
    1   : "Modulation"
    6   : "DataEntry MSB"
    7   : "Volume"
    10  : "Panpot"
    11  : "Expression"
    38  : "DataEntry LSB"
    64  : "Sustain"
    100 : "RPN LSB"
    101 : "RPN MSB"
    120 : "All Sound Off"
    121 : "Rset All Control"
send:
"""

PROFILE_DEFAULT["synth/fluidsynth/qsynth"] = f"""
type: "synth/fluidsynth/qsynth"
config: "~/.config/rncbc.org/Qsynth.conf"
send:
"""

PROFILE_DEFAULT["synth/zynaddsubfx"] = """
type: "synth/zynaddsubfx"
send:
"""

PROFILE_DEFAULT['synth/hard'] = f"""
type: "synth/hard"
recv:
send:
"""

###########################################################################

def _build_profile_as_synth(prof: dict):
    #
    # remove null configs.
    #
    retprof = midisw.profile.util.remove_null_conf(prof)

    #
    # convert string->int some key/parameters
    #
    for k1 in ['send','recv']:
        if not k1 in retprof:
            continue
        #
        # extract min/max
        #
        for k2 in ['ch','notes']:
            if not k2 in retprof[k1]:
                continue
            retprof[k1][k2] = midisw.profile.util.getrange(prof[k1][k2])
        #
        # make dict(int)
        #
        for k2 in ['message','cc']:
            if not k2 in retprof[k1]:
                continue 

            d = copy.copy(retprof[k1][k2])
            for i in d:
                nk = int(i)

                nv = d[i]
                del(retprof[k1][k2][i])
                retprof[k1][k2][nk] = nv
        #
        # tuppled-key proc
        #
        if k2 == 'rpn':
            pass

    # =======================================
    # build tone_name_db / synth specific setting
    # =======================================

    if retprof["type"] == "synth/fluidsynth":
        #
        # extract tonenamedb-def from soundfont
        #
        if "soundfont" in retprof and retprof["soundfont"] != "":
            retprof["tonenamedb"] = midisw.tonenamedb.SoundFont()
            retprof["tonenamedb"].load(retprof["soundfont"])
            retprof["jackname"] = midisw.util.sfpath2sfname(retprof["soundfont"])
    elif retprof["type"] == "synth/zynaddsubfx":
        retprof["tonenamedb"] = midisw.tonenamedb.Zynaddsubfx()
        retprof["tonenamedb"].load()
        retprof["jackname"] = "zynaddsubfx"

    #
    # overwrite tone_name_db by csv
    #
    if 'tonenamecsv' in retprof and retprof["tonenamecsv"] != '':
        retprof["tonenamedb"] = midisw.tonenamedb.CSVFile()
        retprof["tonenamedb"].load(os.path.join(PROFILE_BASE,retprof["type"], retprof["tonenamecsv"]))

    #
    #
    #
    return retprof

PROFILE_BUILDER['synth'] = _build_profile_as_synth

