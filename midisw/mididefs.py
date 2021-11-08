
import yaml

from midisw.envdefs import *


logging.basicConfig(level=LOGGING_LEVEL)

############################################################ util funcs
_NOTES =  {
    "C":0,
    "C#":1,
    "Db":1,
    "D":2,
    "D#":3,
    "Eb":3,
    "E":4,
    "F":5,
    "F#":6,
    "Gb":6,
    "G":7,
    "G#":8,
    "Ab":8,
    "A":9,
    "A#":10,
    "Bb":10,
    "B":11
}

_NOTES_LOWER = {}
for k in _NOTES.keys():
     _NOTES_LOWER[k.lower()] = _NOTES[k]

_NOTES_BLACK = (1,3,6,8,10)
_NOTES_WHITE = (0,2,4,5,7,9,11)


def is_black_or_white(note, ditect_d):
     if isinstance(note, int):
          return note % 12  in ditect_d
     elif isinstance(note, str):
          return note2num(note) % 12 in ditect_d
     else:
          raise ValueError("bad value:"+note)
     

def is_white(note):
     return is_black_or_white(note, _NOTES_WHITE)

def is_black(note):
     #return is_black_or_white(note, _NOTES_BLACK)
     return not is_white(note)


def note2num(note, is_yamaha = False):
    global _NOTES

    if isinstance(note, str):
         note = note.lower()

         for i in range(len(note)):
              if note[i].isdigit() or note[i] == '-':
                   nt = note[:i]
                   oct = int(note[i:]) + 1
                   
                   if is_yamaha:
                        oct += 1

                   if nt in _NOTES_LOWER.keys():
                        num = _NOTES_LOWER[nt] + oct * 12
                   else:
                        raise ValueError("Bad value:"+note)

                   return num & 0x7f
         raise ValueError("Bad value:"+note)
    else:
         raise TypeError("Bad arg type:")

def num2note(num,is_yamaha=False):
    global _NOTES

    num = int(num) & 0x7f

    oct = num//12
    if is_yamaha:
        oct -= 2
    else:
        oct -= 1

    nio = num % 12
    nname = [k for k,v in _NOTES.items() if v == nio][0]

    return nname + str(oct)



#####################################################################
#####################################################################

MIDI_MESSAGE_YAML = """
    0x80 : NOTE_OFF
    0x90 : NOTE_ON
    0xa0 : POLY_PRESSURE
    0xb0 : CONTROL_CHANGE
    0xc0 : PROGRAM_CHANGE
    0xd0 : CHANNEL_PRESSURE
    0xe0 : PITCHBEND
    0xf0 : SYSEX
    0xf1 : MIDI_TIME_CODE/MTC
    0xf2 : SONG_POSITION_POINTER
    0xf3 : SONG_SELECT
    #0xf4 : undefined
    #0xf5 : undefined
    0xf6 : TUNE_REQUEST
    0xf7 : EOX
    0xf8 : TIMING_CLOCK
    #0xf9 : undefined
    0xfa : SONG_START
    0xfb : SONG_CONTINUE
    0xfc : SONG_STOP
    #0xfd : undefined
    0xfe : ACTIVE_SENSING
    0xff : SYSTEM_RESET
"""

MIDI_MESSAGE=yaml.safe_load(MIDI_MESSAGE_YAML)

MIDI_CC_YAML = """
    0x00 : BANK_SELECT_MSB
    0x01 : MODULATION_WHEEL_MSB
    0x02 : BREATH_CONTROLLER
    #0x03 : undefined
    0x04 : FOOT_CONTROLLER_MSB
    0x05 : PORTAMENT_TIME_MSB
    0x06 : DATA_ENTRY_MSB
    0x07 : CHANNEL_VOLUME_MSB
    0x08 : BALANCE_MSB
    #0x09 : undefined
    0x0a : PAN_MSB
    0x0b : EXPRESSION_CONTROLLER_MSB
    0x0c : EFFECT_CONTROL_1_MSB
    0x0d : EFFECT_CONTROL_2_MSB
    #0x0e : undefined
    #0x0f : undefined
    0x10 : GENERAL_PURPOSE_CONTROLLER_1_MSB
    0x11 : GENERAL_PURPOSE_CONTROLLER_2_MSB
    0x12 : GENERAL_PURPOSE_CONTROLLER_3_MSB
    0x13 : GENERAL_PURPOSE_CONTROLLER_4_MSB
    #0x14 : undefined
    #0x15 : undefined
    #0x16 : undefined
    #0x17 : undefined
    #0x18 : undefined
    #0x19 : undefined
    #0x1a : undefined
    #0x1b : undefined
    #0x1c : undefined
    #0x1d : undefined
    #0x1e : undefined
    #0x1f : undefined
    0x20 : BANK_SELECT_LSB
    0x21 : MODULATION_WHEEL_LSB
    0x22 : BREATH_CONTROLLER_LSB
    #0x23 : undefined
    0x24 : FOOT_CONTROLLER_LSB
    0x25 : PORTAMENT_TIME_LSB
    0x26 : DATA_ENTRY_LSB
    0x27 : CHANNEL_VOLUME_LSB
    0x28 : BALANCE_LSB
    0x2a : PAN_LSB
    0x2b : EXPRESSION_CONTROLLER_LSB
    0x2c : EFFECT_CONTROL_1_LSB
    0x2d : EFFECT_CONTROL_2_LSB
    #0x2e : undefined
    #0x2f : undefined
    0x30 : GENERAL_PURPOSE_CONTROLLER_1_LSB
    0x31 : GENERAL_PURPOSE_CONTROLLER_2_LSB
    0x32 : GENERAL_PURPOSE_CONTROLLER_3_LSB,        
    0x33 : GENERAL_PURPOSE_CONTROLLER_4_LSB
    #0x34 : undefined
    #0x35 : undefined,        
    #0x36 : undefined
    #0x37 : undefined
    #0x38 : undefined
    #0x39 : undefined
    #0x3a : undefined
    #0x3b : undefined
    #0x3c : undefined
    #0x3d : undefined
    #0x3e : undefined
    #0x3f : undefined
    0x40 : SUSTAIN_ONOFF
    0x41 : PORTAMENT_ONOFF
    0x42 : SOSTENUTO_ONOFF
    0x43 : SOFT_PEDAL_ONOFF
    0x44 : LEGATO_ONOFF
    0x45 : HOLD_2_ONOFF
    0x46 : SOUND_CONTROLLER_1
    0x47 : SOUND_CONTROLLER_2
    0x48 : SOUND_CONTROLLER_3
    0x49 : SOUND_CONTROLLER_4
    0x4a : SOUND_CONTROLLER_5
    0x4b : SOUND_CONTROLLER_6
    0x4c : SOUND_CONTROLLER_7
    0x4d : SOUND_CONTROLLER_8
    0x4e : SOUND_CONTROLLER_9
    0x4f : SOUND_CONTROLLER_10
    0x50 : GENERAL_PURPOSE_CONTROLLER_5
    0x51 : GENERAL_PURPOSE_CONTROLLER_6
    0x52 : GENERAL_PURPOSE_CONTROLLER_7
    0x53 : GENERAL_PURPOSE_CONTROLLER_8
    0x54 : PORTAMENT_CONTROL
    #0x55 : undefined
    #0x56 : undefined
    #0x57 : undefined,        
    0x58 : HIGH_RESOLUTION_VELOCITY_PREFIX
    #0x59 : undefined
    #0x5a : undefined,        
    0x5b : EFFECTS_1_DEPTH
    0x5c : EFFECTS_2_DEPTH
    0x5d : EFFECTS_3_DEPTH
    0x5e : EFFECTS_4_DEPTH
    0x5f : EFFECTS_5_DEPTH
    0x60 : DETA_INCREMENT
    0x61 : DETA_DECRIMENT
    0x62 : NRPN_LSB
    0x63 : NRPN_MSB
    0x64 : RPN_LSB
    0x65 : RPN_MSB
    #0x66 : undefined
    #0x67 : undefined
    #0x68 : undefined
    #0x69 : undefined
    #0x6a : undefined
    #0x6b : undefined
    #0x6c : undefined
    #0x6d : undefined
    #0x6e : undefined
    #0x6f : undefined
    #0x70 : undefined
    #0x71 : undefined
    #0x72 : undefined
    #0x73 : undefined
    #0x74 : undefined
    #0x75 : undefined
    #0x76 : undefined
    #0x77 : undefined
    0x78 : ALL_SOUND_OFF
    0x79 : RESET_ALL_CONTROLLERS
    0x7a : LOCAL_CONTROL_ONOFF
    0x7b : ALL_NOTES_OFF
    0x7c : OMNI_MODE_OFF
    0x7d : OMNI_MODE_ON
    0x7e : MONO_MODE_ON
    0x7f : POLY_MODE_ON
"""

MIDI_CC=yaml.safe_load(MIDI_CC_YAML)

####################################
MIDI_RPN_YAML = """
    0x00,0x00 : PITCHBEND_SENSIBILITY
    0x00,0x01 : CHANNEL_FINE_TUNING
    0x00,0x02 : CANNEL_COARSE_TUNING
    0x00,0x03 : TUNING_PROGRAM_SELECT
    0x00,0x04 : TUNING_BANK_SELECT
    0x00,0x05 : MODULATION_DEPTH_RANGE
    0x3d,0x00 : AZIMUTH ANGLE
    0x3d,0x01 : ELEVATION_ANGLE
    0x3d,0x02 : GAIN
    0x3d,0x03 : DISTANCE_RATIO
    0x3d,0x04 : MAXIMUM_DISTANCE
    0x3d,0x05 : GAIN_AT_MAXIMUM_DISTANCE
    0x3d,0x06 : REFERENCE_DISTANCE_RATIO
    0x3d,0x07 : PAN_SPREAD_ANGLE
    0x3d,0x08 : ROLL_ANGLE
    0x7f,0x7f : RPN_NULL
"""

MIDI_RPN=yaml.safe_load(MIDI_RPN_YAML)

#MIDI_RPN={}
#for k in _tmprpn.keys():
#     msb=int(k.split(",")[0],16)
#     lsb=int(k.split(",")[0],16)
#     MIDI_RPN[(msb,lsb)] = _tmprpn[k]

#def load_synth_profile(profile_name):
#     prof = {}
#     return prof

####################################
        
