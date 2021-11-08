
import re
import copy

import yaml

from midisw.envdefs import *
from midisw.util import *
from midisw.mididefs import *

from midisw.profile.profile_vars import *
import midisw.tonenamedb

##########################################################################

PROFILE_DEFAULT['synth'] = f"""
type: "synth"
name: "nullname"

recive:
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
tonenamedb_csv: ""
"""


PROFILE_DEFAULT['synth/fluidsynth'] = f"""
type: "synth/fluidsynth"
soundfont: ""
recive:
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

PROFILE_DEFAULT["synth/qsynth"] = """
type: "synth/qsynth"
config: ~/.config/rncbc.org/Qsynth.conf
"""

PROFILE_DEFAULT['synth/hard'] = f"""
type: "synth/hard"
"""

###########################################################################

def _getrange(rstr: str):
    (mins,maxs) = re.sub(r'[\[\]]','',rstr).split(',')

    if maxs == '':
        maxs = mins

    mini = int(mins)
    maxi = int(maxs)+1

    return range(mini, maxi)
    


def _remove_null_conf(prof: dict):
    retprof = {}

    for k in prof:
        if prof[k] is None:
            continue

        if type(prof[k]) is dict and len(prof[k]) > 0:
            retprof[k] =  _remove_null_conf(prof[k])
        elif len(prof[k]) > 0:
            retprof[k] = prof[k]
        else:
            pass

    return retprof



def _build_profile_as_synth(prof: dict):
    #
    # remove null configs.
    #
    retprof = _remove_null_conf(prof)

    #
    # convert string->int some key/parameters
    #
    for k1 in ['send','recive']:
        if not k1 in retprof:
            continue
        #
        # extract min/max
        #
        for k2 in ['ch','notes']:
            if not k2 in retprof[k1]:
                continue
            retprof[k1][k2] = _getrange(prof[k1][k2])
        #
        # make dict(int)
        #
        for k2 in ['message','cc','rpn']:
            if not k2 in retprof[k1]:
                continue 

            d = copy.copy(retprof[k1][k2])
            for i in d:
                nk = int(i)
                nv = d[i]
                del(retprof[k1][k2][i])
                retprof[k1][k2][nk] = nv

    # =======================================
    # build tone_name_db
    # =======================================

    if retprof["type"] == "synth/fluidsynth":
        #
        # extract tonenamedb-def from soundfont
        #
        if "soundfont" in retprof and retprof["soundfont"] != "":
            retprof["tonenamedb"] = midisw.tonenamedb.SoundFont()
            retprof["tonenamedb"].load(os.path.expanduser(retprof["soundfont"]))
    elif retprof["type"] == "synth/qsynth":
        retprof["fluidinstances"] = []
    elif retprof["type"] == "synth/zynaddsubfx":
        retprof["tonenamedb"] = midisw.tonenamedb.Zynaddsubfx()
        retprof["tonenamedb"].load()
    else:
        pass

    #
    # overwrite tone_name_db by csv
    #
    if 'tonenamedb_csv' in retprof and retprof["tonenamedb_csv"] != '':
        retprof["tonenamedb"] = midisw.tonenamedb.CSVFile()
        retprof["tonenamedb"].load(os.path.join(PROFILE_BASE,retprof["type"], retprof["tonenamedb_csv"]))

    #
    #
    #
    return retprof

PROFILE_BUILDER['synth'] = _build_profile_as_synth
