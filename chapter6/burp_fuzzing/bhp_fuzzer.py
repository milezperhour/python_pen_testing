from burp import IBurpExtender # import the IBurpExtender class (required)
from burp import IIntruderPayloadGeneratorFactory
from burp import IIntruderPayloadGenerator

from java.util import List, ArrayList

import random

# define BurpExtender class, which extends the IBurpExtender and IIntruderPayloadGeneratorFactory classes
class BurpExtender(IBurpExtender, IIntruderPayloadGeneratorFactory):
    def registerExtenderCallbacks(self, callbacks):
        self._callbacks = callbacks
        self._helpers   = callbacks.getHelpers()

        # function to register the class so the Intruder tool is aware that
        # we can generate payloads
        callbacks.registerIntruderPayloadGeneratorFactory(self)

        return

# function to return the name of the payload generator
def getGeneratorName(self):
    return 'BHP Payload Generator'

# function that receives the attack parameter and returns an instance of the
# IIntruderPayloadGenerator class, which is called BHPFuzzer
def createNewInstance(self, attack):
    return BHP(self, attack)
