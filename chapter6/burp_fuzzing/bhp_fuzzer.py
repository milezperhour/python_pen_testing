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


# BHPFuzzer class that extends IIntruderPayloadGenerator
class BHPFuzzer(IIntruderPayloadGenerator):
    def __init__(self, extender, attack):
        self._extender     = extender
        self._helpers      = extender._helpers
        self._attack       = attack
        seld.max_payloads  = 10
        self.num_iterations = 0

        return


# checks when maximum number of fuzzing iterations is reached
def hasMorePayloads(self):
    if self.num_iterations == self.max_payloads:
        return False
    else:
        return True


# receives the original HTTP payload; fuzzing happens here
# current_payload variable arrives as a byte array
def getNextPayload(self, current_payload):

    # convert byte array into a string
    payload = ''.join(chr(x) for x in current_payload)

    # call our simple mutator to fuzz the POST
    payload = self.mutate_payload(payload)

    # increase the number of fuzzing attempts
    self.num_iterations += 1

    return payload


def reset(self):
    self.num_iterations = 0
    return


def mutate_payload(self, original_payload):
    # pick a simple mutator or even call a script
    picker = random.randint(1, 3)

    # select a random offset in the payload to mutate
    offset  = random.randint(0, len(original_payload)-1)
    payload = original_payload[:offset]

    # random offset insert a SQL injection attempt
    if picker == 1:
        payload += "'"

    # jam an XSS attempt in
    if picker == 2:
        payload += "<script>alert('BHP!');</script>"

    # repeat a chunk of the original payload a random number
    if picker == 3:
        chunk_length = random.randint(len(payload[offset:]),len(payload)-1)
        repeater     = random.randint(1,10)

        for i in range(repeater):
            payload += original_payload[offset:offset+chunk_length]

    # add the remaining bits of the payload
    payload += original_payload[offset:]

    return payload
