import time
import unittest
import midisw.profile as test_profile
import midisw.startup as test_target

import logging

from midisw.envdefs import *

#logging.basicConfig(level=LOGGING_LEVEL)
logging.basicConfig(level=logging.DEBUG)

class TestStartup(unittest.TestCase):
    def setUp(self):
        test_profile.cleanup_profile()
        test_profile.create_profile()

        self.target_profile_names=['Z00-init-PCH',
                              'Z10-jack-PCH',
                              'Z11-a2jmidid',
                              'Z20-rawsoftsynth-startup',
                              'Z21-fluidsynth-default',
                              'Z22-fluidsynth-specsf',
                              'Z23-zynaddsubfx-default',
                              'Z24-zynaddsubfx-tutname',
                              'Z40-connect-eachports',
        ]


    def tearDown(self):
        pass

    def test_start_to_stop(self):
        loaded_profs = {}
        p_wrapper = {}

        for profname in self.target_profile_names:
            logging.debug(f"# loading profile:{profname}")
            loaded_profs[profname] = test_profile.load_profile('startup',profname)
            logging.debug(f"# done profile={loaded_profs[profname]}")

        for profname in self.target_profile_names:
            logging.debug(f"## starting:{profname} ############################################")

            p_wrapper[profname] = test_target.ProcessWrapper(loaded_profs[profname])
            p_wrapper[profname].start()

            self.assertTrue(p_wrapper[profname].is_active())

            logging.debug("### checking port:"+str(p_wrapper[profname].prof['provides']))
            for port in p_wrapper[profname].prof['provides']:
                self.assertTrue(test_target.is_port_active(port['type'],port['name']))


        logging.debug('# sleeping 10 sec ###################################')
        time.sleep(10)

        for profname in reversed(self.target_profile_names):
            logging.debug(f"## stopping:{profname} ......")

            p_wrapper[profname].stop()

            self.assertFalse(p_wrapper[profname].is_active())
            for port in p_wrapper[profname].prof['provides']:
                self.assertFalse(test_target.is_port_active(port['type'],port['name']))
        
if __name__ == "__main__":
    unittest.main()
