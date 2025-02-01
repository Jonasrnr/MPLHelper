import kaleido
import plotly
import plotly.graph_objects as go
import numpy as np
from utils import create_cuboid_mesh

xpos, ypos = np.meshgrid(np.arange(10), np.arange(10))
xpos = xpos.flatten()
ypos = ypos.flatten()

heights = np.sin(xpos / 2.0) * np.cos(ypos / 2.0) * 5.0

fig_plotly = go.Figure()

for x0, y0, h in zip(xpos, ypos, heights):
    dx = 0.8
    dy = 0.8
    ox = x0 + (1 - dx) / 2
    oy = y0 + (1 - dy) / 2
    origin = (ox, oy, 0)
    size = (dx, dy, h)
    cuboid = create_cuboid_mesh(origin, size, "#00f900")
    fig_plotly.add_trace(cuboid)

fig_plotly.update_layout(
    title="Mein Plot",
    scene=dict(
        xaxis_title="X-Achse",
        yaxis_title="Y-Achse",
        zaxis_title="Höhe",
    ),
    paper_bgcolor="#FFFFFF",
    plot_bgcolor="#FFFFFF",
    width=600,
    height=400,
)

plotly.io.write_image(fig_plotly, "plotly.png", engine="kaleido")
fig_plotly.show()
