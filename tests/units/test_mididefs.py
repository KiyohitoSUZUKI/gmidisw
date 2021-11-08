import unittest
import midisw.mididefs as test_target

##################################################################################

class TestMIDIDefs(unittest.TestCase):
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


###################################################################
if __name__ == "__main__":
    unittest.main()
    

    
