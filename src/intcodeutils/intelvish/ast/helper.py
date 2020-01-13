def str_format(nodetype, name, children = None):
    outp = nodetype;
    if name is not None:
        outp += ' ' + name
    if type(children) == dict:
        outp += ' {\n'
        for name, items in children.items():
            outp += '  ' + name + ':\n'
            for item in items:
                outp += '    ' + str(item).replace('\n', '\n    ') + '\n'
        outp += '}'
    elif type(children) == list:
        outp += ' [\n'
        for item in children:
            outp += '  ' + str(item).replace('\n', '\n  ') + '\n'
        outp += ']'
    return outp