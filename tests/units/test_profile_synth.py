import unittest
import midisw.profile as test_target

import logging

from midisw.envdefs import *
from midisw.mididefs import *
from midisw.util import *

logging.basicConfig(level=LOGGING_LEVEL)
#logging.basicConfig(level=logging.DEBUG)

class TestProfileSynth(unittest.TestCase):
    def setUp(self):
        #
        # cleanup default config
        #
        test_target.cleanup_profile()
        test_target.create_profile()

    def tearDown(self):
        pass

    def test_loading_fluidsynth(self):
        profile_category = "synth"
        profile_name = "fluidsynth/Z00-FluidR3_GM"

        prof = test_target.load_profile(profile_category, profile_name)

        logging.debug("#@prof:%s: %s"%(profile_name,prof))

        self.assertIsNotNone(prof["name"])
        self.assertFalse('send' in prof)
        self.assertTrue(type(prof["recive"]["message"][0x80]) is str)
        self.assertTrue(min(prof["recive"]["ch"]) == 0)
        self.assertTrue(max(prof["recive"]["ch"]) == 15)
        self.assertTrue(min(prof["recive"]["notes"]) == 0)
        self.assertTrue(max(prof["recive"]["notes"]) == 127)

    def test_loading_fc50(self):
        profile_category = "synth"
        profile_name = "hard/fc-50"

        prof = test_target.load_profile(profile_category, profile_name)

        logging.debug("#@prof:%s: %s"%(profile_name,prof))

        self.assertFalse( 'recive' in prof )
        self.assertTrue(  7 in prof["send"]["cc"] )
        self.assertFalse( 0x80 in prof["send"]["message"] )
        self.assertTrue(0xc0 in prof["send"]["message"] )
        self.assertTrue(0xb0 in prof["send"]["message"] )
        
    def test_loading_tonenamedb(self):
        profile_category = "synth"

        for profile_name in ["fluidsynth/Z00-FluidR3_GM", "fluidsynth/Z01-FluidR3_GM"]:

            prof = test_target.load_profile(profile_category, profile_name)

            logging.debug("#@prof:%s: %s"%(profile_name,prof))

            l = prof["tonenamedb"].ls()

            logging.debug("##@ prof.tonenamedb:%s"%l)

            self.assertTrue(len(l) > 0)
            self.assertTrue(prof["tonenamedb"].get_tonename(0,0,0) == "Yamaha Grand Piano")
            self.assertTrue(l[0][0] == 0)
            self.assertTrue(l[0][1] == 0)
            self.assertTrue(l[0][2] == 0)
            self.assertTrue(l[0][4] == "Yamaha Grand Piano")


        

###################################################################
if __name__ == "__main__":
    unittest.main()
