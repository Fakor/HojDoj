import unittest

from sketch_logic_tests import SketchLogicTests
from interpreter_tests import InterpreterTests

def suite():
    suite = unittest.TestSuite()
    suite.addTest(SketchLogicTests('Sketch Logic Tests'))
    suite.addTest(InterpreterTests('Interpreter Tests'))
    return suite

if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suite())