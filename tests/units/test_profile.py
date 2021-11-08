import unittest
import midisw.profile as test_target

import logging

import midisw.envdef as ENVDEF

#logging.basicConfig(level=ENVDEF.LOGGING_LEVEL)
logging.basicConfig(level=logging.DEBUG)

class ProfileTest(unittest.TestCase):
    def setUp(self):
        #
        # cleanup default config
        #
        test_target.cleanup_profile()
        test_target.create_profile()

    def tearDown(self):
        pass

    def test_loading(self):
        profile_type = "startup"
        profile_name = "Z1-jack-PCH"

        prof = test_target.load_profile(profile_type, profile_name)
        self.assertIsNotNone(prof['name'])

    def test_fluidsynth_default(self):
        profile_category = "startup"
        profile_name = "Z2-fluidsynth-default"

        logging.debug(f"#loading profile:{profile_type},{profile_name}")

        prof = test_target.load_profile(profile_category, profile_name)

        logging.debug(f"#builded profile:{prof}")
        self.assertTrue(prof['require'][0]['type'] == 'jack/audio')
        self.assertTrue(prof['require'][0]['name'] == 'system:playback_1')
        self.assertTrue(prof['require'][1]['type'] == 'jack/audio')
        self.assertTrue(prof['require'][1]['name'] == 'system:playback_2')
        self.assertTrue(prof['portname-prefix'] in prof['command'])

    def test_zynaddsubfx_default(self):
        profile_category = "startup"
        profile_name = "Z2-zynaddsubfx-default"

        prof = test_target.load_profile(profile_category, profile_name)

        logging.debug(f"#builded profile:{prof}")
        self.assertTrue(prof['require'][0]['type'] == 'jack/audio')
        self.assertTrue(prof['require'][0]['name'] == 'system:playback_1')
        self.assertTrue(prof['require'][1]['type'] == 'jack/audio')
        self.assertTrue(prof['require'][1]['name'] == 'system:playback_2')
        self.assertTrue(prof['portname-prefix'] in prof['command'])


    def test_expanding_command(self):
        profile_category = "startup"
        profile_name = "Z0-init-PCH"
        
        prof = test_target.load_profile(profile_category, profile_name)

        logging.debug(f"#builded profile:{prof}")
        self.assertTrue(type(prof['command']) is str)

###################################################################
if __name__ == "__main__":
    unittest.main()
