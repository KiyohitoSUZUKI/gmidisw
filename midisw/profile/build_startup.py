
from midisw.envdefs import *
from midisw.util import *

from midisw.profile.profile_vars import *

##############################################################################

PROFILE_DEFAULT['startup'] = '''
require :
  - type : alsa/audio
    name : PCH
  - type : alsa/audio
    name : PCH
provides : [ ]
command : bash
'''

PROFILE_DEFAULT['startup/synth/fluidsynth'] = '''
require :
  - type : jack/audio
    name : system:playback_1
  - type : jack/audio
    name : system:playback_2
soundfont : /usr/share/sounds/sf2/FluidR3_GM.sf2
'''

PROFILE_DEFAULT['startup/synth/zynaddsubfx'] = '''
require :
  - type : jack/audio
    name : system:playback_1
  - type : jack/audio
    name : system:playback_2
'''

PROFILE_DEFAULT['startup/oneshot'] = '''
require :
  - type : jack/audio
    name : system:playback_1
  - type : jack/audio
    name : system:playback_2
'''

##############################################################################

def _build_profile_as_startup(prof: dict):
    #
    # set each synthtype default configulation
    #
    if prof['type'] == 'startup':
        prof['command'] = f"xterm -T '{prof['profile']}:{prof['name']}' -e '{prof['command']}'"

    elif prof['type'] == 'startup/oneshot':
        if type(prof['command']) is list:
            cmd = f"xterm -T '{prof['profile']}:{prof['name']}' -e '"
            for cl in prof['command']:
                #cmd += f"{cl};".replace("'","''")
                cmd += f"{cl};"
            cmd += "'"
            prof['command'] = cmd

    elif prof['type'] == 'startup/synth/fluidsynth':
        prof['soundfont_expandpath'] = sfpath = os.path.expanduser(prof['soundfont'])
        prof['portname_prefix'] = portname_prefix = os.path.splitext(os.path.basename(sfpath))[0]
        prof['jack_name'] = portname_prefix
        prof['command'] = f"xterm -T '{prof['profile']}:{prof['name']}' -e 'fluidsynth --chorus=no --reverb=no --audio-driver=jack --midi-driver=jack -o audio.jack.id={portname_prefix} -o midi.jack.id={portname_prefix} {sfpath}'"
        prof["provides"] = [
            {'type' : 'jack/midi',  'name' : f"{portname_prefix}:midi_00" },
            {'type' : "jack/audio", 'name' : f"{portname_prefix}:left"},
            {'type' : "jack/audio", 'name' : f"{portname_prefix}:right"},
        ]

    elif prof['type'] == 'startup/synth/zynaddsubfx':
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

PROFILE_BUILDER['startup'] = _build_profile_as_startup
