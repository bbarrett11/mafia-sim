from Load import loadSetupFromFile
from MafiaGame import MafiaGame
import Constants
import unittest
import random
from Action import Action, ActionType

# Test Helper methods
def createGame(setup_name: str):
    setup = loadSetupFromFile(file_name=setup_name)
    game = MafiaGame(setup)
    return game
    

class TestAllStarsMethods(unittest.TestCase):

    def testCop(self):
        game = createGame("allstars")
        cop = [player for player in game.alive_players if player.role == Constants.COP][0]
        self.assertTrue(Constants.COP == cop.role)
        cop.role.doNightAction()
        self.assertEqual(len(game.night_actions),1)
        cop_check = game.night_actions[0]
        target = cop_check.target
        self.assertEqual(cop_check.type,ActionType.CHECK)
        self.assertEqual(cop_check.owner,cop)
        self.assertNotEqual(cop_check.target,cop)
        self.assertIn(cop_check.target,game.alive_players)
        
        game.resolveNightActions()
        self.assertEqual(len(game.night_actions),0)
        self.assertEqual(len(cop.results),1)
        self.assertEqual(cop.results[0]['type'],ActionType.CHECK)
        gen_target, gen_align = cop.results[0]['content']
        self.assertEqual(gen_target,target)
        self.assertEqual(gen_align,target.alignment)


    def test_split(self):
        s = 'hello world'
        self.assertEqual(s.split(), ['hello', 'world'])
        # check that s.split fails when the separator is not a string
        #with self.assertRaises(TypeError):
        #    s.split(2)

if __name__ == '__main__':
    unittest.main()
