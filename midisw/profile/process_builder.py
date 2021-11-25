
from midisw.envdefs import *
from midisw.util import *

from midisw.profile.modulevars import *

##############################################################################

PROFILE_DEFAULT['process'] = '''
type: process
category: "process"
require :
  - type : alsa/audio
    name : PCH
  - type : alsa/audio
    name : PCH
provides : [ ]
command : bash
'''

PROFILE_DEFAULT["process/synth"] = """
type: process/synth
"""

PROFILE_DEFAULT['process/synth/fluidsynth'] = '''
type: process/synth/fluidsynth
require :
  - type : jack/audio
    name : system:playback_1
  - type : jack/audio
    name : system:playback_2
soundfont : /usr/share/sounds/sf2/FluidR3_GM.sf2
'''

PROFILE_DEFAULT['process/synth/zynaddsubfx'] = '''
type: process/synth/zynaddsubfx
require :
  - type : jack/audio
    name : system:playback_1
  - type : jack/audio
    name : system:playback_2
'''

PROFILE_DEFAULT['process/oneshot'] = '''
type: process/oneshot
require :
  - type : jack/audio
    name : system:playback_1
  - type : jack/audio
    name : system:playback_2
'''

##############################################################################

def _build_profile_as_process(prof: dict):
    #
    # set each synthtype default configulation
    #
    if prof['type'] == 'process':
        prof['command'] = f"xterm -T '{prof['name']}' -e '{prof['command']}'"

    elif prof['type'] == 'process/oneshot':
        if type(prof['command']) is list:
            cmd = f"xterm -T '{prof['name']}' -e '"
            for cl in prof['command']:
                #cmd += f"{cl};".replace("'","''")
                cmd += f"{cl};"
            cmd += "'"
            prof['command'] = cmd

    elif prof['type'] == 'process/synth/fluidsynth':
        prof['soundfont_expandpath'] = sfpath = os.path.expanduser(prof['soundfont'])
        prof['portname_prefix'] = portname_prefix = os.path.splitext(os.path.basename(sfpath))[0]
        prof['jack_name'] = portname_prefix
        prof['command'] = f"xterm -T '{prof['name']}' -e 'fluidsynth --chorus=no --reverb=no --audio-driver=jack --midi-driver=jack -o audio.jack.id={portname_prefix} -o midi.jack.id={portname_prefix} {sfpath}'"
        prof["provides"] = [
            {'type' : 'jack/midi',  'name' : f"{portname_prefix}:midi_00" },
            {'type' : "jack/audio", 'name' : f"{portname_prefix}:left"},
            {'type' : "jack/audio", 'name' : f"{portname_prefix}:right"},
        ]

    elif prof['type'] == 'process/synth/zynaddsubfx':
        portname_prefix = 'zynaddsubfx'
        if 'zynaddsubfx_name' in prof:
            prof['command'] = f"zynaddsubfx --output=jack --input=jack -N {prof['zynaddsubfx_name']}"
            portname_prefix += f"_{prof['zynaddsubfx_name']}" 
        else:
            prof['command'] = f"zynaddsubfx --output=jack --input=jack"
        prof['portname_prefix'] = portname_prefix
        prof['jack_name'] = portname_prefix

        prof["provides"] = [
            {'type' : 'jack/midi',  'name' : f"{portname_prefix}:midi_input" },
            {'type' : 'jack/midi',  'name' : f"{portname_prefix}:osc" },
            {'type' : 'jack/audio',  'name' : f"{portname_prefix}:out_1" },
            {'type' : 'jack/audio',  'name' : f"{portname_prefix}:out_2" },
        ]

    else:
        pass

    return prof

PROFILE_BUILDER['process'] = _build_profile_as_process
