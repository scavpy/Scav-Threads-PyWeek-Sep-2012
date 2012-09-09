"""
Modes of operation

Each mode of operation allows for different mechanisms by which the operator may
control the device, and different results are communicated thereby.

Upon completion of the task for which the mode of operation is designed, the
result og the operation is a symbolic representation of the succeeding mode.
"""

import pygame

class ModeOfOperation(object):
    """ Being a mould from which other modes of operation can be cast and
    forged into their divers forms """
    def __init__(self):
        self.screen = pygame.display.get_surface()
        self.clock = pygame.time.Clock()
    def operate(self, current_situation):
        return "Preparation"
    def clear_screen(self, colour=(0,0,0), image=None):
        if image:
            self.screen.blit(image,(0,0))
        else:
            self.screen.fill(colour)

MODES_IN_USE = {"DoingNoThing":ModeOfOperation()}

class ShepherdOfModes(object):
    """ That which directs the orderly transition between modes """
    def begin(self, mode_name, current_situation):
        while mode_name:
            try:
                mode = MODES_IN_USE[mode_name]
            except KeyError:
                module_name = mode_name.lower() + "_mode"
                module = __import__(module_name)
                mode = getattr(module, mode_name + "Mode")()
                MODES_IN_USE[mode_name] = mode
            mode_name = mode.operate(current_situation)
