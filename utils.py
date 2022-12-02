def parse_component(c):
    if "-" in c:
        name, out = c.split("-")
        if name == "INval":
            return f"&{name}[{out}]"
        return f"&{name}.OUTval[{out}]"
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
    component = parse_component(component)
    return (inputs, component)

def cook(c):
    """
    transforms a precooked component to a parsed c++ line
    """
    c = precook_component(c)
    line = f"""\t\t\tintern.pushback(new {c[1][0]}({', '.join(c[0])}));
\t\t\t{c[1][0]} & {c[1][0]}{c[1][1]} = *(intern.back());"""
    return line

def multicook(cs, sep = '|'):
    """
    cs : components separated by sep
    """
    cs = list(map(str.strip, cs.split(sep)))
    cs = list(map(cook, cs))
    return "\n".join(cs)
    

if __name__ == "__main__":
    to_cook = "INval-0, INval-1 >>> NAND1"
    print(cook(to_cook))