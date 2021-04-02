import unittest
import midisw.mididevice as test_target

##################################################################################

class MIDIEventDefTest(unittest.TestCase):
    def setUp(self):
        self.evdef = test_target.MIDIEventDef()
        self.evdef.add(0x80)
        self.pc = (0xc0,"PROGRAMCHANGE!!") 
        self.evdef.add(self.pc[0],self.pc[1],)

    def tearDown(self):
        pass

    def test_defined(self):
        self.assertTrue(self.evdef.is_defined(0x80))
        self.assertEqual(self.evdef[0x80], test_target.MIDIEventDef.ALIAS_IF_NOTNAMED[0x80])
        self.assertTrue(self.evdef.is_defined(self.pc[0]))
        self.assertTrue(self.evdef.is_named(self.pc[1]))

    def test_notedefined(self):
        self.assertFalse(self.evdef.is_defined(0x90))
        self.assertFalse(self.evdef.is_named("NOTE_ON"))


##################################################################################
class MIDICCDefTest(unittest.TestCase):
    def setUp(self):
        self.ccdef=test_target.MIDICCDef({0x00: None, 0x07: "VOLUME"})

    def tearDown(self):
        pass

    def test_defined(self):
        self.assertEqual(len(self.ccdef.keys()), 2)
        self.assertEqual(len(self.ccdef.values()), 2)

        self.assertTrue(self.ccdef.is_defined(0x00))
        self.assertEqual(self.ccdef[0x00], test_target.MIDICCDef.ALIAS_IF_NOTNAMED[0x00])

        self.assertTrue(self.ccdef.is_defined(0x07))
        self.assertEqual(self.ccdef[0x07], "VOLUME")

    def test_notdefined(self):
        self.assertFalse(self.ccdef.is_defined(0x01))
        self.assertFalse(self.ccdef.is_named(""))


if __name__ == "__main__":
    unittest.main()
    
