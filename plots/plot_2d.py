import matplotlib.pyplot as plt
import numpy as np
import streamlit as st


def plot_2d(
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
    xlabel_fontsize,
    ylabel_fontsize,
    title,
    title_fontsize,
    font_family,
    data=None,
):
    fig, ax = plt.subplots(
        figsize=(fig_width, fig_height),
        facecolor=fig_facecolor,
        edgecolor=fig_edgecolor,
    )
    ax.set_facecolor(axes_facecolor)

    if data is not None:
        x = data.iloc[:, 0]
        for i, settings in enumerate(lines_settings):
            y = data.iloc[:, i + 1]
            ax.plot(
                x,
                y,
                color=settings["line_color"],
                linewidth=settings["line_width"],
                linestyle=settings["line_style"],
                marker=settings["marker"],
                label=settings["label"],
            )
    else:
        x = np.linspace(0, 10, 100)
        for i, settings in enumerate(lines_settings):
            y = np.sin(x + i)
            ax.plot(
                x,
                y,
                color=settings["line_color"],
                linewidth=settings["line_width"],
                linestyle=settings["line_style"],
                marker=settings["marker"],
                label=settings["label"],
            )

    if show_grid:
        ax.grid(
            True, color=grid_color, linestyle=grid_linestyle, linewidth=grid_linewidth
        )
    if show_legend:
        ax.legend(
            loc=legend_location, fontsize=legend_fontsize, facecolor=legend_facecolor
        )
    ax.set_xlabel(xlabel, fontsize=xlabel_fontsize, fontfamily=font_family)
    ax.set_ylabel(ylabel, fontsize=ylabel_fontsize, fontfamily=font_family)
    ax.set_title(title, fontsize=title_fontsize, fontfamily=font_family)
    st.pyplot(fig, use_container_width=False)

    return fig
