def to_latex(text):
    return r"$" + text + r"$"

idx2param = {
    0: "sigma",
    1: "rho",
    2: "beta"
}
param2idx = {v: k for k, v in idx2param.items()}

idx2var = {
    0: 'x',
    1: 'y',
    2: 'z',
}
var2idx = {v: k for k, v in idx2var.items()}

COLORS = [
    'blue', 'red', 'green', 'orange', 'purple',
    'brown', 'pink', 'gray', 'olive', 'cyan',
    'magenta', 'lime', 'teal', 'navy', 'maroon',
    'gold', 'coral', 'darkgreen', 'steelblue', 'indigo'
]

def smart_format(x, precision=3):
    if x == int(x):
        return f"{int(x)}"
    else:
        return f"{x:.{precision}f}"