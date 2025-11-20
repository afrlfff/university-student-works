
def float_to_decimal_str(x, max_decimals=10):
    s = f"{x:.{max_decimals}f}"
    
    if '.' in s:
        s = s.rstrip('0').rstrip('.')
    return s if s != '' else '0'
