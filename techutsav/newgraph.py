from itertools import count
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

plt.style.use('fivethirtyeight')
x_vals = []
y_vals = []

FIELD_NAMES = ["x", "happy", "neutral", "sad"]

plt.plot([], [], label=FIELD_NAMES[1])
plt.plot([], [], label=FIELD_NAMES[2])
plt.plot([], [], label=FIELD_NAMES[3])


def animate(i):
    data = pd.read_csv('accuracy.csv')
    x = data[FIELD_NAMES[0]]
    y1 = data[FIELD_NAMES[1]]
    y2 = data[FIELD_NAMES[2]]
    y3 = data[FIELD_NAMES[3]]

    ax = plt.gca()
    line1, line2, line3 = ax.lines

    line1.set_data(x, y1)
    line2.set_data(x, y2)
    line3.set_data(x, y3)

    xlim_low, xlim_high = ax.get_xlim()
    ylim_low, ylim_high = ax.get_ylim()

    ax.set_xlim(xlim_low, (x.max() + 5))

    y1max = y1.max()
    y2max = y2.max()
    y3max = y3.max()

    # current_ymax = y1max if (y1max > y2max) else y2max
    if (y1max > y2max) and (y1max > y3max):
        current_ymax = y1max
    elif (y2max > y1max) and (y2max > y3max):
        current_ymax = y2max
    else:
        current_ymax = y3max

    y1min = y1.min()
    y2min = y2.min()
    y3min = y3.min()

    # current_ymin = y1min if (y1min < y2min) else y2min
    if (y1min < y2min) and (y1min < y3min):
        current_ymin = y1min
    elif (y2min < y1min) and (y2min < y3min):
        current_ymin = y2min
    else:
        current_ymin = y3min

    ax.set_ylim((current_ymin - 5), (current_ymax + 5))


def start():

    ani = FuncAnimation(plt.gcf(), animate, interval=1000)

    plt.legend()
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    start()