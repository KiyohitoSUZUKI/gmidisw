import unittest
import midisw.profile as test_target

import logging

from midisw.envdefs import *
from midisw.mididefs import *
import midisw.util 

logging.basicConfig(level=LOGGING_LEVEL)
#logging.basicConfig(level=logging.DEBUG)

class TestProfileSynth(unittest.TestCase):
    def setUp(self):
        #
        # cleanup default config
        #
        test_target.cleanup()
        test_target.create()

    def tearDown(self):
        pass

    def test_loading_fluidsynth(self):
        logging.debug("#@testing loading synth/fluidsynth======================")

        profile_category = "synth"
        profile_name = "fluidsynth/Z00-FluidR3_GM"

        prof = test_target.load(profile_category, profile_name)

        logging.debug("#@prof:%s: %s"%(profile_name,prof))

        self.assertIsNotNone(prof["name"])
        self.assertFalse('send' in prof)
        self.assertTrue(type(prof["recive"]["message"][0x80]) is str)
        self.assertTrue(min(prof["recive"]["ch"]) == 0)
        self.assertTrue(max(prof["recive"]["ch"]) == 15)
        self.assertTrue(min(prof["recive"]["notes"]) == 0)
        self.assertTrue(max(prof["recive"]["notes"]) == 127)

    def test_loading_fc50(self):
        logging.debug("#@testing loading synth/hard/fc-50======================")
        profile_category = "synth"
        profile_name = "hard/fc-50"

        prof = test_target.load(profile_category, profile_name)

        logging.debug("#@prof:%s: %s"%(profile_name,prof))

        self.assertFalse( 'recive' in prof )
        self.assertTrue(  7 in prof["send"]["cc"] )
        self.assertFalse( 0x80 in prof["send"]["message"] )
        self.assertTrue(0xc0 in prof["send"]["message"] )
        self.assertTrue(0xb0 in prof["send"]["message"] )
        
    def test_loading_tonenamedb(self):
        logging.debug("#@testing loading tonenamedb======================")

        profile_category = "synth"

        for profile_name in ["fluidsynth/Z00-FluidR3_GM", "fluidsynth/Z01-FluidR3_GM"]:

            prof = test_target.load(profile_category, profile_name)

            logging.debug("#@prof:%s: %s -------------"%(profile_name,prof))

            l = prof["tonenamedb"].ls()

#            logging.debug("##@ prof.tonenamedb:%s"%l)

            self.assertTrue(len(l) > 0)

            self.assertTrue(prof["tonenamedb"].get_tname(0,0,0) == "Yamaha Grand Piano")
            self.assertTrue(l[0][0] == 0)
            self.assertTrue(l[0][1] == 0)
            self.assertTrue(l[0][2] == 0)
            if "tonenamecsv" in prof:
                self.assertTrue(l[0][3] == "Piano")
            else:
                self.assertTrue(l[0][3] == midisw.util.sfpath2sfname(prof["soundfont"]))
            self.assertTrue(l[0][4] == "Yamaha Grand Piano")


    def test_loading_tonenamedb_zynaddsubfx(self):        
        logging.debug("#@testing loading zynaddsubfx======================")

        profile_category = "synth"
        profile_name = "zynaddsubfx/Z00-zynaddsubfx"

        prof = test_target.load(profile_category, profile_name)

        logging.debug("#@prof:%s: %s"%(profile_name,prof))

        l = prof["tonenamedb"].ls()

        self.assertTrue(len(l) > 0)

        self.assertTrue(l[0][3] == "Arpeggios")

    
###################################################################
if __name__ == "__main__":
    unittest.main()
