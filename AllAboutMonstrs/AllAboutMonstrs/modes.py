"""
Modes of operation

Each mode of operation allows for different mechanisms by which the operator may
control the device, and different results are communicated thereby.

Upon completion of the task for which the mode of operation is designed, the
result og the operation is a symbolic representation of the succeeding mode.
"""

class ModeOfOperation(object):
    """ Being a mould from which other modes of operation can be cast and
    forged into their divers forms """
    def operate(self, current_situation):
        return "Preparation"

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
