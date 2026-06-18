import numpy as np
from matplotlib.ticker import FuncFormatter
from matplotlib.ticker import ScalarFormatter

# отображение графиков в [мА, мС, кОм, ...] без аллокации нового массива
formatter_to_mA  = FuncFormatter(lambda y, _: f'{y*1000:.3f}')
formatter_to_mS  = FuncFormatter(lambda y, _: f'{y*1000:.3f}')
formatter_to_mV  = FuncFormatter(lambda y, _: f'{y*1000:.3f}')
formatter_to_mSm = FuncFormatter(lambda y, _: f'{y*1000:.3f}')
formatter_to_kOm = FuncFormatter(lambda y, _: f'{y/1000:.3f}')

# Форматирование меток на оси Y в научной нотации
def set_scientific_yaxis(ax, scilimits=(0, 1)):
    fmt = ScalarFormatter(useMathText=True)
    fmt.set_powerlimits(scilimits)
    ax.yaxis.set_major_formatter(fmt)

# Форматирование меток на оси X в научной нотации
def set_scientific_xaxis(ax, scilimits=(0, 1)):
    fmt = ScalarFormatter(useMathText=True)
    fmt.set_powerlimits(scilimits)
    ax.xaxis.set_major_formatter(fmt)