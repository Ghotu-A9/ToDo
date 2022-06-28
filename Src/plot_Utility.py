import matplotlib

matplotlib.use('GTK3Agg')  # or 'GTK3Cairo'
import matplotlib.pyplot as plt
import numpy as np

from matplotlib.backends.backend_gtk3agg import (
    FigureCanvasGTK3Agg as FigureCanvas)

import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

plt.style.use('_mpl-gallery-nogrid')

fig, ax = plt.subplots()

size = 0.3
vals = np.array([[60., 32.], [37., 40.], [29., 10.]])

cmap = plt.colormaps["tab20c"]
outer_colors = cmap(np.arange(3)*4)
inner_colors = cmap([1, 2, 5, 6, 9, 10])

ax.pie(vals.sum(axis=1), radius=1, colors=outer_colors,
       wedgeprops=dict(width=size, edgecolor='w'))



ax.set(aspect="equal", title='Pie plot with `ax.pie`')

Window = Gtk.Window()

canvas = FigureCanvas(fig)  # a Gtk.DrawingArea
canvas.set_size_request(800, 600)
Window.add(canvas)

Window.connect("destroy", Gtk.main_quit)

print(type(fig.canvas))

Window.show_all()

Gtk.main()
