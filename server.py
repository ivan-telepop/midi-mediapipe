import socket
import time
import rtmidi
import re
from rtmidi import *
from rtmidi.midiconstants import NOTE_OFF, NOTE_ON


# import time
# import rtmidi

# midiout = rtmidi.MidiOut()
# available_ports = midiout.get_ports()

# if available_ports:
#     midiout.open_port(0)
# else:
#     midiout.open_virtual_port("My virtual output")

# with midiout:
#     # channel 1, middle C, velocity 112
#     note_on = [0x90, 60, 112]
#     note_off = [0x80, 60, 0]
#     midiout.send_message(note_on)
#     time.sleep(0.5)
#     midiout.send_message(note_off)
#     time.sleep(0.1)

# del midiout





class MidiPool(object):
    """ MidiPool class: 
    singletone works with MIDI IN / OUT
    Args:
        object (_type_): _description_
    """
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(MidiPool, cls).__new__(cls)
            return cls.instance

    def __init__(self):
        self.MIDIOUT = rtmidi.MidiOut(name="My MIDI Port's Hub")
        print(f"OPENED MIDI PORTS IS :{self.MIDIOUT.get_ports()}")
    def __repr__(self):
        return f"OPENED PORTS:{self.MIDIOUT.get_port_count()}"

    def play_midi_message(self, NOTE, PORT):
            with (self.MIDIOUT.open_port(PORT) if self.MIDIOUT.get_ports() else self.MIDIOUT.open_virtual_port("My virtual output")) as OPENED_MIDI_PORTS:
                if OPENED_MIDI_PORTS:
                    
                    OPENED_MIDI_PORTS.send_message([NOTE_ON, NOTE, 112])
                    time.sleep(0.1)
                    OPENED_MIDI_PORTS.send_message([NOTE_OFF, NOTE, 0])
                    time.sleep(0.1)
                else:
                    print(f"MIDI PORTS OPENNING ERROR:{OPENED_MIDI_PORTS}")


# List of Notes
CENTER_NOTES = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']




MIDI_POOL = MidiPool()
if __name__ == '__main__':
    print(f'MIDI POOL STARTED WITH: {MIDI_POOL.__repr__()} \n')
    HOST = '127.0.0.1'
    PORT = 65432
    
    
    
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as skt:
        skt.bind((HOST, PORT))
        skt.listen()
        conn, addr = skt.accept()
        with conn:
            print('Connected by', addr)
            while True:
                bytes_data = conn.recv(1024)
                data_string = bytes_data.decode('utf-8')
                # for testing experience just found all digits
                digits_one = re.findall('\d', data_string)
                digits_two = re.findall('\d[0-9]', data_string)
                digits_three = re.findall('\d[0-9][0-9]', data_string)
                MIDI_POOL.play_midi_message(int(digits_two[0]), int(digits_one[0]))


