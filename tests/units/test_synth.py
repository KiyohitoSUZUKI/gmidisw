import unittest

import midisw.synth as test_target

import logging

#logging.basicConfig(level=midisw.envdefs.LOGGING_LEVEL)
logging.basicConfig(level=logging.DEBUG)

class TestSynth(unittest.TestCase):
    def setUp(self):
        pass
    def tearDown(self):
        pass

    def test_loading_synth(self):
        logging.debug("## loading synth profile all")

        synth_profile = test_target.Synth()

        for prof in synth_profile.profiles:
            logging.debug("## loaded profile: name=%s,type=%s"%(prof["name"], prof["type"]))
            self.assertTrue(prof["category"] == "synth")

        for prof in synth_profile.ls_writable():
            self.assertTrue("recv" in prof)
        for prof in synth_profile.ls_readable():
            self.assertTrue("send" in prof)

        for prof in synth_profile.ls_writable():
            if  "jackname" in prof and  prof["jackname"] == "QGM":
                self.assertTrue(prof["tonenamedb"].get_tname(0,0,0) == "Yamaha Grand Piano")

###################################################################
if __name__=="__main__":
    unittest.main()

#if __name__=="__main__":
#    sp = Synth()
#
#    for pf in sp.profiles:
#        logging.debug("## available profile: %s(%s)"%(pf["name"],pf["type"]))
#
#    for pf in sp.ls_writable():
#        logging.debug("## found writable_profile: %s"%pf)
#    for pf in sp.ls_readable():
#        logging.debug("## found readable_profile: %s"%pf)
#
#    for pf in sp.profiles:
#        if "tonenamedb" in pf and not pf["tonenamedb"] is None:
#            for i in pf["tonenamedb"].ls():
#                logging.debug("###@ %s : %u,%u,%u,%s,%s"%(
#                    pf["jackname"], i[0],i[1],i[2], i[3],i[4]))
        
