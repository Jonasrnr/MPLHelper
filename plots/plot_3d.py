import plotly.graph_objects as go
import numpy as np
import streamlit as st


def plot_3d(
    fig_width,
    fig_height,
    fig_facecolor,
    fig_edgecolor,
    axes_facecolor,
    lines_settings,
    show_grid,
    grid_color,
    grid_linestyle,
    grid_linewidth,
    show_legend,
    legend_location,
    legend_fontsize,
    legend_facecolor,
    xlabel,
    ylabel,
    zlabel,
    xlabel_fontsize,
    ylabel_fontsize,
    zlabel_fontsize,
    title,
    title_fontsize,
    font_family,
    data=None,
):
    fig_plotly = go.Figure()

    if data is not None:
        x = data.iloc[:, 0]
        for i, settings in enumerate(lines_settings):
            y = data.iloc[:, i + 1]
            z = data.iloc[:, i + 2]
            dash_mapping = {
                "solid": "solid",
                "dashed": "dash",
                "dashdot": "dashdot",
                "dotted": "dot",
            }
            marker_mapping = {
                "": None,
                "o": "circle",
                "s": "square",
                "^": "triangle-up",
                "D": "diamond",
            }
            dash = dash_mapping.get(settings["line_style"], "solid")
            marker_symbol = marker_mapping.get(settings["marker"], None)
            mode = "lines+markers" if marker_symbol is not None else "lines"

            fig_plotly.add_trace(
                go.Scatter3d(
                    x=x,
                    y=y,
                    z=z,
                    mode=mode,
                    line=dict(
                        color=settings["line_color"],
                        width=settings["line_width"],
                        dash=dash,
                    ),
                    marker=(
                        dict(symbol=marker_symbol, size=6)
                        if marker_symbol is not None
                        else None
                    ),
                    name=settings["label"],
                )
            )
    else:
        x = np.linspace(0, 10, 100)
        for i, settings in enumerate(lines_settings):
            y = np.sin(x + i)
            z = np.cos(x + i)
            dash_mapping = {
                "solid": "solid",
                "dashed": "dash",
                "dashdot": "dashdot",
                "dotted": "dot",
            }
            marker_mapping = {
                "": None,
                "o": "circle",
                "s": "square",
                "^": "triangle-up",
                "D": "diamond",
            }
            dash = dash_mapping.get(settings["line_style"], "solid")
            marker_symbol = marker_mapping.get(settings["marker"], None)
            mode = "lines+markers" if marker_symbol is not None else "lines"

            fig_plotly.add_trace(
                go.Scatter3d(
                    x=x,
                    y=y,
                    z=z,
                    mode=mode,
                    line=dict(
                        color=settings["line_color"],
                        width=settings["line_width"],
                        dash=dash,
                    ),
                    marker=(
                        dict(symbol=marker_symbol, size=6)
                        if marker_symbol is not None
                        else None
                    ),
                    name=settings["label"],
                )
            )

    fig_plotly.update_layout(
        title=title,
        scene=dict(
            xaxis_title=xlabel,
            yaxis_title=ylabel,
            zaxis_title=zlabel,
        ),
        paper_bgcolor=fig_facecolor,
        plot_bgcolor=fig_facecolor,
        width=int(fig_width * 100),
        height=int(fig_height * 100),
    )
    st.plotly_chart(fig_plotly, use_container_width=False)

    return fig_plotly
