
from matplotlib.pyplot import figure, show
from numpy import arange, sin, pi


class snx:
    def __init__(self, a, b , c):
        self.a = a
        self.b = b
        self.c = c


    def sixxxx(self):
        t = arange(self.a, self.b, self.c)
        fig = figure(1)

        ax1 = fig.add_subplot(211)
        ax1.plot(t, sin(2*pi*t))
        ax1.grid(True)
        ax1.set_ylim((-10, 10))
        ax1.set_ylabel('1 Hz')
        ax1.set_title('A sine wave or two')

        for label in ax1.get_xticklabels():
            label.set_color('r')

        ax2 = fig.add_subplot(212)
        ax2.plot(t, sin(2*2*pi*t))
        ax2.grid(True)
        ax2.set_ylim((-2, 2))
        l = ax2.set_xlabel('Hi mom')
        l.set_color('g')
        l.set_fontsize('large')
        show()

    def edit_set(self, new_b):
        self.b = new_b

a = snx(0.1, 10, 0.001)
a.sixxxx()
a.edit_set(1)
a.sixxxx()