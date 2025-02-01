import plotly.graph_objects as go
import numpy as np
import streamlit as st
from utils import create_cuboid_mesh


def plot_3d_block(
    fig_width,
    fig_height,
    fig_facecolor,
    line_color,
    title,
    xlabel,
    ylabel,
    zlabel,
    xlabel_fontsize,
    ylabel_fontsize,
    zlabel_fontsize,
    title_fontsize,
    font_family,
    grid_x,
    grid_y,
    block_fraction,
    height_scale,
    data=None,
):
    if data is not None:
        xpos = data.iloc[:, 0]
        ypos = data.iloc[:, 1]
        heights = data.iloc[:, 2] * height_scale
    else:
        xpos, ypos = np.meshgrid(np.arange(grid_x), np.arange(grid_y))
        xpos = xpos.flatten()
        ypos = ypos.flatten()
        heights = np.sin(xpos / 2.0) * np.cos(ypos / 2.0) * height_scale

    fig_plotly = go.Figure()

    for x0, y0, h in zip(xpos, ypos, heights):
        dx = block_fraction
        dy = block_fraction
        ox = x0 + (1 - dx) / 2
        oy = y0 + (1 - dy) / 2
        origin = (ox, oy, 0)
        size = (dx, dy, h)
        cuboid = create_cuboid_mesh(origin, size, line_color)
        fig_plotly.add_trace(cuboid)

    fig_plotly.update_layout(
        title=title,
        scene=dict(
            xaxis_title=xlabel,
            yaxis_title=ylabel,
            zaxis_title="Höhe",
        ),
        paper_bgcolor=fig_facecolor,
        plot_bgcolor=fig_facecolor,
        width=int(fig_width * 100),
        height=int(fig_height * 100),
    )
    st.plotly_chart(fig_plotly, use_container_width=False)

    return fig_plotly
