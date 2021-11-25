import unittest

import midisw.midiport as test_target
import midisw.synth as test_synth
import logging

#logging.basicConfig(level=midisw.envdefs.LOGGING_LEVEL)
logging.basicConfig(level=logging.DEBUG)

class TestMIDIPort(unittest.TestCase):
    def setUp(self):
        pass
    def tearDown(self):
        pass

    def test_port_profile(self):
        logging.debug("## loading synth profile all")

        midi_ports = test_target.MIDIPort()

        for port_type in midi_ports.port_names:
            logging.debug("#@ listing port_type=%s "%port_type)
            for pname in midi_ports.port_names[port_type]:
                logging.debug("#@ name='%s', profile='%s'"%(pname, midi_ports.port_profiles[port_type][pname]["name"]))
#                if "tonenamedb" in midi_ports.port_profiles[port_type][pname]:
#                    for t in midi_ports.port_profiles[port_type][pname]["tonenamedb"].ls():
#                        logging.debug("#@found tone= %u,%u,%u,%s,%s"%(t[0],t[1],t[2],  t[3],t[4]))



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
        
