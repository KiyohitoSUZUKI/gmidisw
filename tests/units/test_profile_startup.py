import unittest
import midisw.profile as test_target

import logging

from midisw.envdefs import *

logging.basicConfig(level=LOGGING_LEVEL)
#logging.basicConfig(level=logging.DEBUG)

class TestProfileStartup(unittest.TestCase):
    def setUp(self):
        #
        # cleanup default config
        #
        test_target.cleanup_profile()
        test_target.create_profile()

    def tearDown(self):
        pass

    def test_loading(self):
        profile_category = "startup"
        profile_name = "Z10-jack-PCH"

        prof = test_target.load_profile(profile_category, profile_name)
        self.assertIsNotNone(prof['name'])

    def test_fluidsynth_default(self):
        profile_category = "startup"
        profile_name = "Z21-fluidsynth-default"

        logging.debug(f"#loading profile:{profile_category},{profile_name}")

        prof = test_target.load_profile(profile_category, profile_name)

        logging.debug(f"#builded profile:{prof}")
        self.assertTrue(prof['require'][0]['type'] == 'jack/audio')
        self.assertTrue(prof['require'][0]['name'] == 'system:playback_1')
        self.assertTrue(prof['require'][1]['type'] == 'jack/audio')
        self.assertTrue(prof['require'][1]['name'] == 'system:playback_2')
        self.assertTrue(prof['portname_prefix'] in prof['command'])

    def test_zynaddsubfx_default(self):
        profile_category = "startup"
        profile_name = "Z23-zynaddsubfx-default"

        prof = test_target.load_profile(profile_category, profile_name)

        logging.debug(f"#builded profile:{prof}")
        self.assertTrue(prof['require'][0]['type'] == 'jack/audio')
        self.assertTrue(prof['require'][0]['name'] == 'system:playback_1')
        self.assertTrue(prof['require'][1]['type'] == 'jack/audio')
        self.assertTrue(prof['require'][1]['name'] == 'system:playback_2')
        self.assertTrue(prof['portname_prefix'] in prof['command'])


    def test_expanding_command(self):
        profile_category = "startup"
        profile_name = "Z00-init-PCH"
        
        prof = test_target.load_profile(profile_category, profile_name)

        logging.debug(f"#builded profile:{prof}")
        self.assertTrue(type(prof['command']) is str)

###################################################################
if __name__ == "__main__":
    unittest.main()
