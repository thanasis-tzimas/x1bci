from array import array


class VirtualMachine:
    Memory: array('Q')
    Flags: dict

    def __init__(self) -> None:
        self.Memory = array('Q', [])
        self.Flags = {
            'Overflow': False,
            'Underflow': False,
            'Carry': False,
            'Zero': False,
        }