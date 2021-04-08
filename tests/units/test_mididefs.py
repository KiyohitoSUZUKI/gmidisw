import unittest
import midisw.mididefs as test_target

##################################################################################

class UtilFuncTest(unittest.TestCase):
    def setUp(self):
        pass
    
    def tearDown(self):
        pass

    def test_num2note(self):
        #
        # yamaha check
        #
        self.assertEqual(test_target.num2note(60),"C4")
        self.assertEqual(test_target.num2note(60,True),"C3")

        #
        # boundary check
        #
        self.assertEqual(test_target.num2note(-1),"G9")
        self.assertEqual(test_target.num2note(128),"C-1")


    def test_note2num(self):
        #
        # yamaha check
        #
        self.assertEqual(test_target.note2num("C4"),60)
        self.assertEqual(test_target.note2num("C4",True),60+12)

        #
        # boundary check
        #
        self.assertEqual(test_target.note2num("C-1"),0)
        self.assertEqual(test_target.note2num("C-2",True),0)
        self.assertEqual(test_target.note2num("C#-1"),1)
        self.assertEqual(test_target.note2num("Db-1"),1)
        self.assertEqual(test_target.note2num("D-1"),2)
        self.assertEqual(test_target.note2num("d#-1"),3)        
        self.assertEqual(test_target.note2num("eb-1"),3)        
        self.assertEqual(test_target.note2num("e-1"),4)        

        self.assertEqual(test_target.note2num("G9"),127)
        self.assertEqual(test_target.note2num("G#9"),0)
        self.assertEqual(test_target.note2num("A9"),1)
        self.assertEqual(test_target.note2num("G8",True),127)

        #
        # bad arg check.
        #
        with self.assertRaises(TypeError):
            test_target.note2num(10.0)
        with self.assertRaises(ValueError):
            foo = test_target.note2num("C#")
        with self.assertRaises(ValueError):
            foo = test_target.note2num("44100")
        with self.assertRaises(ValueError):
            foo = test_target.note2num("Say Hello")


    def test_is_black_or_white(self):
        self.assertTrue(test_target.is_white(60))
        self.assertTrue(test_target.is_black(61))
        self.assertTrue(test_target.is_white("C4"))        
        self.assertTrue(test_target.is_black("C#4"))        
        self.assertTrue(test_target.is_black("Db4"))        

        with self.assertRaises(ValueError):
            foo = test_target.is_black("B#")
        with self.assertRaises(ValueError):
            foo = test_target.is_white("B#")
        with self.assertRaises(ValueError):
            foo = test_target.is_black("C")
        with self.assertRaises(ValueError):
            foo = test_target.is_black("This Is Black Key")
        

##################################################################################

class MIDIEventDefTest(unittest.TestCase):
    def setUp(self):
        self.evdef = test_target.MIDIEventDef()
        self.evdef.define(0x80)
        self.pc = (0xc0,"PROGRAMCHANGE!!") 
        self.evdef.define(self.pc[0],self.pc[1],)
        self.evdef[0xb0] = "CC"

    def tearDown(self):
        pass

    def test_defined(self):
        self.assertTrue(self.evdef.is_defined(0x80))
        self.assertEqual(self.evdef[0x80], test_target.MIDIEventDef.ALIAS_IF_NOTNAMED[0x80])
        self.assertTrue(self.evdef.is_defined(self.pc[0]))
        self.assertTrue(self.evdef.is_named(self.pc[1]))
        self.assertEqual(self.evdef[0xb0],"CC")

    def test_notedefined(self):
        self.assertFalse(self.evdef.is_defined(0x90))
        self.assertFalse(self.evdef.is_named("NOTE_ON"))

    def test_reverse_refer(self):
        self.assertEqual(self.evdef.rref("NOTE_OFF"),0x80)

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


    
#########################################################################################


###################################################################
if __name__ == "__main__":
    unittest.main()
    

    
