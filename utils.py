

def indent(text, prefix="    "):
    if not text.strip():
        return ""

    return "\n".join([prefix + line for line in text.split("\n")[:-1]]) + "\n"

def indentReprList(objects, prefix="    "):
    s = ""
    for o in objects:
        s += repr(o) + "\n"

    s = indent(s, prefix=prefix)

    if not s.strip():
        return ""
    else:
        return "\n" + s

