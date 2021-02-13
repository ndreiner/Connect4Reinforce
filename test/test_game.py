# test/test_game.py

import src.game as game
import numpy as np
import unittest

if __name__ == "__main__":
    unittest.main()

class testGame(unittest.TestCase):
    def testinit(self):
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


