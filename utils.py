def parse_component(c):
    if "-" in c:
        name, out = c.split("-")
        return f"{name}[{out}]"
    i = 0
    name = ""
    ID = ""
    while c[i].isalpha():
        name += c[i]
        i+=1
    ID = c[i:]
    return (name, ID)

def precook_component(c, sep = ">>>", input_sep = ","):
    """
    transforms a string component to a tuple containing ([inputs], (component_name, component_id))
    default sep : ">>>"
    default input_sep : ", "
    """
    inputs, component = map(str.strip, c.split(sep))
    inputs = map(lambda x: parse_component(x.strip()), inputs.split(input_sep))
    
    