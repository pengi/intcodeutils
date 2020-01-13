def _format(value):
    outp = ''
    if type(value) == dict:
        outp += '{\n'
        for name, item in value.items():
            outp += '  ' + name + ': ' + _format(item).replace('\n', '\n  ') + '\n'
        outp += '}'
    elif type(value) == list:
        outp += '[\n'
        for item in value:
            outp += '  ' + _format(item).replace('\n', '\n  ') + '\n'
        outp += ']'
    else:
        outp += str(value)
    return outp

def str_format(nodetype, name, children = None):
    outp = nodetype;
    if name is not None:
        outp += ' ' + name
    if children is not None:
        outp += ' ' + _format(children)
    return outp