#this is the code for the midi keypad, Since I'm unsure if LEDS will be usable, I've decided to markout some things, and wait to see how everything fairs.
import keypad
import touchio
from adafruit_midi.control_change import ControlChange
from microcontroller import pin

from kmk.extensions.media_keys import MediaKeys
from kmk.extensions.rgb import RGB, AnimationModes
from kmk.keys import KC
from kmk.kmk_keyboard import KMKKeyboard
from kmk.modules.encoder import EncoderHandler
from kmk.modules.midi import MidiKeys
from kmk.modules.potentiometer import PotentiometerHandler
from kmk.scanners import Scanner
from kmk.scanners.keypad import KeysScanner

class TouchPad(Scanner):
     def __init__(self, pin):
          self.pads = [touchio.TouchIn(p) for p in pin]
          self.pressed = [False] * len(pin)
     
     def keycount(self):
          return len(self.pads)

     def isChanges(self):
          for p in enumerate(self.pads):
               active = p.value
               if active != self.pressed[p]:
                    self.pressed[p] = active
                    #add in LED code here
                    ischange = keypad.Event(p + self.offset, active)
                    return ischange  


          CapKeypad = KMKKeyboard()
          midi = MidiKeys()
          mediaKey = MediaKeys()

          CapKeypad.matrix = [TouchPad ([pin.GPIO13,pin.GPIO12,pin.GPIO11,pin.GPIO10,pin.GPIO9,pin.GPIO8, pin.GPIO7]), KeysScanner([pin.GPIO4, pin.GPIO5, pin.GPIO6], pressedval =True, pulled=True)]
          CapKeypad.keymap = [KC.MIDINOTE(70),KC.MIDINOTE(72),KC.MIDINOTE(74),KC.MIDINOTE(75),KC.MIDINOTE(77),KC.MIDINOTE(79),KC.MIDINOTE(71),KC.MIDINOTE(35),KC.MIDINOTE(37),KC.MIDINOTE(43)]

          encode = EncoderHandler()
          encode.pins(pin.GPIO43, pin.GPIO44, None)
          encode.map = (KC.VOLD, KC.VOLU,KC.NO) 

          gauges = PotentiometerHandler()
          gauges.pins((pin.GPIO2, lambda state: midi.send(ControlChange(1, state.position))), (pin.GPIO1, lambda state : midi.send(ControlChange(7, state.position))))

          CapKeypad.modules = [midi, encode, gauges]
          #make sure that the animationmode fits with the one that you end up using for the LEDs.
          CapKeypad.extensions = [mediaKey, RGB(pinPixel = pin.GPIO3, num_pixels=3, val_default=80, animation_mode = AnimationModes.RAINBOW)]

          if __name__ == '__main__':
               CapKeypad.go()