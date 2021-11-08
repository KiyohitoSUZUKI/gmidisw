import os
import shutil
import yaml
import logging

import midisw.envdef as ENVDEF

logging.basicConfig(level=ENVDEF.LOGGING_LEVEL)
#########################################    
DEFAULT_PROFILE = {}

#########################################
def cleanup_profile():
    if os.path.exists(ENVDEF.PROFILE_BASE):
        shutil.rmtree(ENVDEF.PROFILE_BASE)

def create_profile():
    shutil.copytree(ENVDEF.TEMPLATE_PROFILE_BASE,
                    ENVDEF.PROFILE_BASE,
                    dirs_exist_ok=True)


#########################################    
DEFAULT_PROFILE['startup'] = '''
type: startup
require :
  - type : alsa/audio
    name : PCH
  - type : alsa/audio
    name : PCH
provides : [ ]
command : bash
'''

DEFAULT_PROFILE['startup/synth/fluidsynth'] = '''
require :
  - type : jack/audio
    name : system:playback_1
  - type : jack/audio
    name : system:playback_2
soundfont : /usr/share/sounds/sf2/FluidR3_GM.sf2
'''

DEFAULT_PROFILE['startup/synth/zynaddsubfx'] = '''
require :
  - type : jack/audio
    name : system:playback_1
  - type : jack/audio
    name : system:playback_2
'''

DEFAULT_PROFILE['startup/oneshot'] = '''
require :
  - type : jack/audio
    name : system:playback_1
  - type : jack/audio
    name : system:playback_2
'''


def build_startup_profile(prof):
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
        prof['soundfont-path'] = sfpath = os.path.expanduser(prof['soundfont'])
        prof['portname-prefix'] = portname_prefix = os.path.splitext(os.path.basename(sfpath))[0]
        prof['command'] = f"xterm -T '{prof['profile']}:{prof['name']}' -e 'fluidsynth --chorus=no --reverb=no --audio-driver=jack --midi-driver=jack -o audio.jack.id={portname_prefix} -o midi.jack.id={portname_prefix} {sfpath}'"
        prof["provides"] = [
            {'type' : 'jack/midi',  'name' : f"{portname_prefix}:midi_00" },
            {'type' : "jack/audio", 'name' : f"{portname_prefix}:left"},
            {'type' : "jack/audio", 'name' : f"{portname_prefix}:right"},
        ]

    elif prof['type'] == 'startup/synth/zynaddsubfx':
        portname_prefix = 'zynaddsubfx'
        if 'zynaddsubfx-name' in prof:
            prof['command'] = f"zynaddsubfx --output=jack --input=jack -N {prof['zynaddsubfx-name']}"
            portname_prefix += f"_{prof['zynaddsubfx-name']}" 
        else:
            prof['command'] = f"zynaddsubfx --output=jack --input=jack"
        prof['portname-prefix'] = portname_prefix

        prof["provides"] = [
            {'type' : 'jack/midi',  'name' : f"{portname_prefix}:midi_input" },
            {'type' : 'jack/midi',  'name' : f"{portname_prefix}:osc" },
            {'type' : 'jack/audio',  'name' : f"{portname_prefix}:out_1" },
            {'type' : 'jack/audio',  'name' : f"{portname_prefix}:out_2" },
        ]

    else:
        pass

    return prof
    

def load_profile(profile_category, profile_name):
    filename = os.path.join(ENVDEF.PROFILE_BASE,profile_category,profile_name+'.yml')
    with open(filename,'r') as ldf:
        prof = {}
        loaded_prof = yaml.safe_load(ldf)
        prof['category'] = profile_category
        prof['profile'] = profile_name
        prof['path'] = filename

        if not 'type' in loaded_prof:
            loaded_prof['type'] = profile_category

        if not loaded_prof['type'] in DEFAULT_PROFILE:
            raise ValueError("unknown profile type dtected!"+loaded_prof['type'])
        
        if profile_category == 'startup':
            prof.update(yaml.safe_load(DEFAULT_PROFILE['startup']))    # apply DEFAULT(startup common)
            prof.update(yaml.safe_load(DEFAULT_PROFILE[loaded_prof['type']])) # apply DEFAULT(each synth)
            prof.update(loaded_prof)                # update  by loaded profile
            prof = build_startup_profile(prof)      # update each synthtype settings
        elif profile_category == 'synth':
            pass
        else:
            raise ValueEror("unknown profile category detected!"+profile_category)
            pass

        return prof
        
