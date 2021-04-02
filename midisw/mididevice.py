
"""
    MIDIDeviceDef.profile = {
      "name": {
           accept:    {num: "alias_name", ....} # list of event
           accept_cc: {num: "alias_name", ....} # list of cc&alias_name
           send:      {num: "alias name", ....}                  
           send_cc:   {num: "alias_name", ....}
           banks: {
              (bank_msb,bank_lsb): {
                 "name":  "the_bank_name"
                 "progs": {num: ["prog_name", "prog_category"],.... }
              }
                .....
            }
           }
           drum_channel: ch_no
           drum_banks:{
              (bank_msb,bank_lsb): {
                  name:  "the_bank_name"
                  progs: {num: ["prog_name","prog_category"], ....}
              }
              ..... 
           }
      }
    }
"""

#####################################################################
class MIDIDef(dict):
    ALIAS_IF_NOTNAMED = {}

    def __init__(self, defdict={}):
        super().__init__(self)
        self.clear()
        for k in defdict.keys():
            self.add(k,defdict[k])


    def add(self,key, value=None):
        if value is None and key in self.ALIAS_IF_NOTNAMED:
            self[key] = self.ALIAS_IF_NOTNAMED[key]
        else:
            self[key] = value

    def is_defined(self, key):
        return key in self.keys()

    def is_named(self, val):
        return val in self.values()

####################################

class MIDIEventDef(MIDIDef):
    ALIAS_IF_NOTNAMED = {
        0x80 : "NOTE_OFF",
        0x90 : "NOTE_ON",
        0xa0 : "POLY_PRESSURE",
        0xb0 : "CONTROL_CHANGE",
        0xc0 : "PROGRAM_CHANGE",
        0xd0 : "CHANNEL_PRESSURE",
        0xe0 : "PITCHBEND",
        0xf0 : "SYSEX",
        0xf1 : "MIDI_TIME_CODE/MTC",
        0xf2 : "SONG_POSITION_POINTER",
        0xf3 : "SONG_SELECT",
        #0xf4 : "undefined",
        #0xf5 : "undefined",
        0xf6 : "TUNE_REQUEST",
        0xf7 : "EOX",
        0xf8 : "TIMING_CLOCK",
        #0xf9 : "undefined",
        0xfa : "SONG_START",
        0xfb : "SONG_CONTINUE",
        0xfc : "SONG_STOP",
        #0xfd : "undefined",
        0xfe : "ACTIVE_SENSING",
        0xff : "SYSTEM_RESET"
    }

####################################        

class MIDICCDef(MIDIDef):
    ALIAS_IF_NOTNAMED = {
        0x00 : "BANK_SELECT_MSB",
        0x01 : "MODULATION_WHEEL_MSB",
        0x02 : "BREATH_CONTROLLER",
        #0x03 : "undefined",
        0x04 : "FOOT_CONTROLLER_MSB",
        0x05 : "PORTAMENT_TIME_MSB",
        0x06 : "DATA_ENTRY_MSB",
        0x07 : "CHANNEL_VOLUME_MSB",
        0x08 : "BALANCE_MSB",
        #0x09 : "undefined",
        0x0a : "PAN_MSB",
        0x0b : "EXPRESSION_CONTROLLER_MSB",
        0x0c : "EFFECT_CONTROL_1_MSB",
        0x0d : "EFFECT_CONTROL_2_MSB",
        #0x0e : "undefined",
        #0x0f : "undefined",
        0x10 : "GENERAL_PURPOSE_CONTROLLER_1_MSB",
        0x11 : "GENERAL_PURPOSE_CONTROLLER_2_MSB",
        0x12 : "GENERAL_PURPOSE_CONTROLLER_3_MSB",
        0x13 : "GENERAL_PURPOSE_CONTROLLER_4_MSB",
        #0x14 : "undefined",
        #0x15 : "undefined",
        #0x16 : "undefined",
        #0x17 : "undefined",
        #0x18 : "undefined",
        #0x19 : "undefined",
        #0x1a : "undefined",
        #0x1b : "undefined",
        #0x1c : "undefined",
        #0x1d : "undefined",
        #0x1e : "undefined",
        #0x1f : "undefined",
        0x20 : "BANK_SELECT_LSB",
        0x21 : "MODULATION_WHEEL_LSB",
        0x22 : "BREATH_CONTROLLER_LSB",
        #0x23 : "undefined",
        0x24 : "FOOT_CONTROLLER_LSB",
        0x25 : "PORTAMENT_TIME_LSB",
        0x26 : "DATA_ENTRY_LSB",
        0x27 : "CHANNEL_VOLUME_LSB",
        0x28 : "BALANCE_LSB",
        0x2a : "PAN_LSB",
        0x2b : "EXPRESSION_CONTROLLER_LSB",
        0x2c : "EFFECT_CONTROL_1_LSB",
        0x2d : "EFFECT_CONTROL_2_LSB",
        #0x2e : "undefined",
        #0x2f : "undefined",
        0x30 : "GENERAL_PURPOSE_CONTROLLER_1_LSB",
        0x31 : "GENERAL_PURPOSE_CONTROLLER_2_LSB",
        0x32 : "GENERAL_PURPOSE_CONTROLLER_3_LSB",        
        0x33 : "GENERAL_PURPOSE_CONTROLLER_4_LSB",
        #0x34 : "undefined",
        #0x35 : "undefined",        
        #0x36 : "undefined",
        #0x37 : "undefined",
        #0x38 : "undefined",
        #0x39 : "undefined",
        #0x3a : "undefined",
        #0x3b : "undefined",
        #0x3c : "undefined",
        #0x3d : "undefined",
        #0x3e : "undefined",
        #0x3f : "undefined",
        0x40 : "SUSTAIN_ONOFF",
        0x41 : "PORTAMENT_ONOFF",
        0x42 : "SOSTENUTO_ONOFF",
        0x43 : "SOFT_PEDAL_ONOFF",
        0x44 : "LEGATO_ONOFF",
        0x45 : "HOLD_2_ONOFF",
        0x46 : "SOUND_CONTROLLER_1",
        0x47 : "SOUND_CONTROLLER_2",
        0x48 : "SOUND_CONTROLLER_3",
        0x49 : "SOUND_CONTROLLER_4",
        0x4a : "SOUND_CONTROLLER_5",
        0x4b : "SOUND_CONTROLLER_6",
        0x4c : "SOUND_CONTROLLER_7",
        0x4d : "SOUND_CONTROLLER_8",
        0x4e : "SOUND_CONTROLLER_9",
        0x4f : "SOUND_CONTROLLER_10",
        0x50 : "GENERAL_PURPOSE_CONTROLLER_5",
        0x51 : "GENERAL_PURPOSE_CONTROLLER_6",
        0x52 : "GENERAL_PURPOSE_CONTROLLER_7",
        0x53 : "GENERAL_PURPOSE_CONTROLLER_8",
        0x54 : "PORTAMENT_CONTROL",
        #0x55 : "undefined",
        #0x56 : "undefined",
        #0x57 : "undefined",        
        0x58 : "HIGH_RESOLUTION_VELOCITY_PREFIX",
        #0x59 : "undefined",
        #0x5a : "undefined",        
        0x5b : "EFFECTS_1_DEPTH",
        0x5c : "EFFECTS_2_DEPTH",
        0x5d : "EFFECTS_3_DEPTH",
        0x5e : "EFFECTS_4_DEPTH",
        0x5f : "EFFECTS_5_DEPTH",
        0x60 : "DETA_INCREMENT",
        0x61 : "DETA_DECRIMENT",
        0x62 : "NRPN_LSB",
        0x63 : "NRPN_MSB",
        0x64 : "RPN_LSB",
        0x65 : "RPN_MSB",
        #0x66 : "undefined",
        #0x67 : "undefined",
        #0x68 : "undefined",
        #0x69 : "undefined",
        #0x6a : "undefined",
        #0x6b : "undefined",
        #0x6c : "undefined",
        #0x6d : "undefined",
        #0x6e : "undefined",
        #0x6f : "undefined",
        #0x70 : "undefined",
        #0x71 : "undefined",
        #0x72 : "undefined",
        #0x73 : "undefined",
        #0x74 : "undefined",
        #0x75 : "undefined",
        #0x76 : "undefined",
        #0x77 : "undefined",
        0x78 : "ALL_SOUND_OFF",
        0x79 : "RESET_ALL_CONTROLLERS",
        0x7a : "LOCAL_CONTROL_ONOFF",
        0x7b : "ALL_NOTES_OFF",
        0x7c : "OMNI_MODE_OFF",
        0x7d : "OMNI_MODE_ON",
        0x7e : "MONO_MODE_ON",
        0x7f : "POLY_MODE_ON",
    }


####################################
class MIDIRPNDef(MIDIDef):
    ALIAS_IF_NOTNAMED = {
        (0x00,0x00) : "PITCHBEND_SENSIBILITY",
        (0x00,0x01) : "CHANNEL_FINE_TUNING",
        (0x00,0x02) : "CANNEL_COARSE_TUNING",
        (0x00,0x03) : "TUNING_PROGRAM_SELECT",
        (0x00,0x04) : "TUNING_BANK_SELECT",
        (0x00,0x05) : "MODULATION_DEPTH_RANGE",
        (0x3d,0x00) : "AZIMUTH ANGLE",
        (0x3d,0x01) : "ELEVATION_ANGLE",
        (0x3d,0x02) : "GAIN",
        (0x3d,0x03) : "DISTANCE_RATIO",
        (0x3d,0x04) : "MAXIMUM_DISTANCE",
        (0x3d,0x05) : "GAIN_AT_MAXIMUM_DISTANCE",
        (0x3d,0x06) : "REFERENCE_DISTANCE_RATIO",
        (0x3d,0x07) : "PAN_SPREAD_ANGLE",
        (0x3d,0x08) : "ROLL_ANGLE",
        (0x7f,0x7f) : "RPN_NULL",
    }


class MIDINRPNDef(MIDIDef):
    ALIAS_IF_NOTNAMED = {}


####################################

####################################

class BankSetDef(MIDIDef):
    def define(self,msb,lsb, bank_name=""):
        self.d[(msb,lsb)] = {"name": bank_name, "progs": {}}
        self.d_rev[bank_name] = (msb,lsb)

    def get_bankname(self,msb,lsb):
        return self.d[(msb,lsb)]["name"]

    def get_bankno(self,name):
        return self.d_rev[name]

    def define_tone(bank_name,prog_no,tone_name, category_name):
        self.d[self.get_bankno(bank_name)]["progs"][prog_no] = [tone_name, category_name]
        

#####################################################################

class MIDIDeviceDef(object):
    profiles = {}

    def __init__(self):
        super(MIDIDeviceDef, self).__init__()

    def add(self,name):
        if not isinstance(name,str):
            assert TypeError("profile name must be a string")
        if len(name) <= 0:
            assert ValueError("null named")

        self.profiles[name] = {
            #
            # import from MIDI implimentation chart
            #
            "accept": {
                "notes": (None,None),  ### (begin_range , end_range)
                "ch":    (None,None),  ### (begin_range , end_range)
                "event":   MIDIEventDef(),
                "cc":  MIDICCDef(),
                "rpn": MIDIRPNDef(),
                "nrpn": MIDINRPNDef(),
            },
            "send" : {
                "notes": (None,None), 
                "ch":    (None,None), 
                "event": MIDIEventDef(),
                "cc":    MIDICCDef(),
                "rpn":  MIDIRPNDef(),
                "nrpn": MIDINRPNDef(),
            },
            #
            # import from MIDI tonelist
            #
            "banks": BankSetDef(),
            "drum_channel": None,
            "drum_banks": BankSetDef(),
        }

    def list(self):
        return self.profiles.keys()
