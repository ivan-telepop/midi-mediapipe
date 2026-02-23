import mido


MIDI_PORT_NAMES = mido.get_output_names()
# Opened MIDI


def midi_message_handler(port_name: str, msg_data: int, velocity: int):
    """MIDI Message handler - temp solution
    Args:
        port_name (str): one of the opened ports
        msg_data (int): note data sent to port
    """
    with  mido.open_output(port_name) as port:
        init_msg = mido.Message('note_on', velocity=velocity, note=msg_data)
        port.send(init_msg)
        close_msg = mido.Message('note_off', velocity=velocity, note=msg_data)
        port.send(close_msg)