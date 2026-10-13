"""Assembly convention: finish the previous layer; every input must connect.

These are puzzle/assembly rules, not a claim of collision-only enforcement.
Layer footprints must be declared, including any boundary pieces. Intentional
separator spaces are not missing tiles. None is not a Boolean signal, and a
logical wildcard still needs a physically present supplying connector.
"""


def require_complete_layer(expected, placed):
    expected, placed = set(expected), set(placed)
    if expected != placed:
        raise ValueError(f'Incomplete or unexpected previous layer: '
                         f'{len(expected-placed)} missing, {len(placed-expected)} extra.')


def require_inputs(connections):
    """connections contains (physically present output value, input type)."""
    for value, socket in connections:
        if value is None:
            raise ValueError('Bridging is forbidden: an input has no supplying output.')
        if socket == '*':
            if type(value) is not int or value not in (0,1):
                raise ValueError('A wildcard requires an existing Boolean output.')
        elif type(value) is not type(socket) or value != socket:
            raise ValueError(f'Incompatible connection: {value!r} to {socket!r}.')
