# test/test_game.py

from logging import exception
import src.game as game
import numpy as np
import unittest

if __name__ == "__main__":
    unittest.main()

class testField(unittest.TestCase):
    def testfieldinit(self):
        """
        Test correct Initialisation
        """
        # check explicit argumets
        myfield_explicit = game.field(FIELD_HEIGHT=3,
                             FIELD_WIDTH=4)
        #init implicit, check arg order
        myfield_implicit = game.field(3,4)
        
        desired_field = np.zeros((3,4))
        
        self.assertTrue(
            np.array_equal(
                myfield_explicit.get_matrix(),
                desired_field
            ),
            msg = "Initalisation produces wrong matrix"
        )
        self.assertTrue(
            np.array_equal(
                myfield_implicit.get_matrix(),
                desired_field
                ),
            msg= "Init Arguments not in correct Order"
        )
    
    def testfielddrop(self):
        """
        Teste den drop 
        """
        myfield_explicit = game.field(FIELD_HEIGHT=3,
                             FIELD_WIDTH=4)
        myfield_explicit.drop(1, token = 1)
        myfield_explicit.drop(1, token = 1)
        myfield_explicit.drop(1, token = 1)
        desired_field = np.array([[0,1,0,0],
                                  [0,1,0,0],
                                  [0,1,0,0]])
        self.assertTrue(
            np.array_equal(
                myfield_explicit.get_matrix(),
                desired_field
            ),
            msg = "Drops are incorrectly registered"
        )
        
        # Should assert
        with self.assertRaises(Exception) as Exception_context:
            myfield_explicit.drop(1, token = 1)
            self.assertTrue('Column is already full!' in Exception_context.exception)

class Testgame(unittest.TestCase):
    def testinitGame(self):
        """
        Check if gameinit works
        """
        mygame = game.game(game.field(FIELD_HEIGHT=3,
                             FIELD_WIDTH=4),
                    n_connect_to_win=4)
        
        winstate = mygame.exec_action(0,1)
        winstate = mygame.exec_action(1,1)
        winstate = mygame.exec_action(2,1)
        winstate = mygame.exec_action(3,1)
        self.assertEqual(1, winstate)



