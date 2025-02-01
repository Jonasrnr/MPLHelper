from config import PlotType


def generate_python_code(
    plot_type,
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
    grid_x=None,
    grid_y=None,
    block_fraction=None,
    height_scale=None,
    line_color=None,
    code_library="Matplotlib",
):
    if plot_type == PlotType.PLOT_2D.value:
        code = f"""import matplotlib.pyplot as plt
                import numpy as np

                fig, ax = plt.subplots(figsize=({fig_width}, {fig_height}),
                                    facecolor="{fig_facecolor}", edgecolor="{fig_edgecolor}")
                ax.set_facecolor("{axes_facecolor}")

                x = np.linspace(0, 10, 100)
                """
        for i, settings in enumerate(lines_settings):
            code += f"""
                    y{i} = np.sin(x + {i})
                    ax.plot(x, y{i}, color="{settings['line_color']}", linewidth={settings['line_width']},
                            linestyle="{settings['line_style']}", marker="{settings['marker']}", label="{settings['label']}")
                    """
        if show_grid:
            code += f"""
                    ax.grid(True, color="{grid_color}", linestyle="{grid_linestyle}", linewidth={grid_linewidth})
                    """
        if show_legend:
            code += f"""
                    ax.legend(loc="{legend_location}", fontsize={legend_fontsize}, facecolor="{legend_facecolor}")
                    """
        code += f"""
                ax.set_xlabel("{xlabel}", fontsize={xlabel_fontsize}, fontfamily="{font_family}")
                ax.set_ylabel("{ylabel}", fontsize={ylabel_fontsize}, fontfamily="{font_family}")
                ax.set_title("{title}", fontsize={title_fontsize}, fontfamily="{font_family}")

                plt.show()
                """
    elif plot_type == PlotType.PLOT_3D.value:
        if code_library == "Matplotlib":
            code = f"""import matplotlib.pyplot as plt
                    import numpy as np
                    from mpl_toolkits.mplot3d import Axes3D

                    fig = plt.figure(figsize=({fig_width}, {fig_height}),
                                    facecolor="{fig_facecolor}", edgecolor="{fig_edgecolor}")
                    ax = fig.add_subplot(111, projection='3d')
                    ax.set_facecolor("{axes_facecolor}")

                    x = np.linspace(0, 10, 100)
                    """
            for i, settings in enumerate(lines_settings):
                code += f"""
                        y{i} = np.sin(x + {i})
                        z{i} = np.cos(x + {i})
                        ax.plot(x, y{i}, z{i}, color="{settings['line_color']}", linewidth={settings['line_width']},
                                linestyle="{settings['line_style']}", marker="{settings['marker']}", label="{settings['label']}")
                        """
            if show_grid:
                code += f"""
                        ax.grid(True, color="{grid_color}", linestyle="{grid_linestyle}", linewidth={grid_linewidth})
                        """
            if show_legend:
                code += f"""
                        ax.legend(loc="{legend_location}", fontsize={legend_fontsize}, facecolor="{legend_facecolor}")
                        """
            code += f"""
                    ax.set_xlabel("{xlabel}", fontsize={xlabel_fontsize}, fontfamily="{font_family}")
                    ax.set_ylabel("{ylabel}", fontsize={ylabel_fontsize}, fontfamily="{font_family}")
                    ax.set_zlabel("Z-Achse", fontsize={xlabel_fontsize}, fontfamily="{font_family}")
                    ax.set_title("{title}", fontsize={title_fontsize}, fontfamily="{font_family}")

                    plt.show()
                    """
        else:
            code = f"""import plotly.graph_objects as go
                    import numpy as np

                    fig_plotly = go.Figure()

                    x = np.linspace(0, 10, 100)
                    """
            for i, settings in enumerate(lines_settings):
                code += f"""
                        y{i} = np.sin(x + {i})
                        z{i} = np.cos(x + {i})
                        fig_plotly.add_trace(go.Scatter3d(
                            x=x, y=y{i}, z=z{i}, mode="{'lines+markers' if settings['marker'] else 'lines'}",
                            line=dict(color="{settings['line_color']}", width={settings['line_width']}, dash="{settings['line_style']}"),
                            marker=dict(symbol="{settings['marker']}", size=6) if settings['marker'] else None,
                            name="{settings['label']}"
                        ))
                        """
            code += f"""
                    fig_plotly.update_layout(
                        title="{title}",
                        scene=dict(
                            xaxis_title="{xlabel}",
                            yaxis_title="{ylabel}",
                            zaxis_title="Z-Achse",
                        ),
                        paper_bgcolor="{fig_facecolor}",
                        plot_bgcolor="{fig_facecolor}",
                        width={int(fig_width * 100)},
                        height={int(fig_height * 100)},
                    )

                    fig_plotly.show()
                    """
    elif plot_type == PlotType.PLOT_3D_BLOCK.value:
        code = f"""import plotly.graph_objects as go
                import numpy as np
                from utils import create_cuboid_mesh

                xpos, ypos = np.meshgrid(np.arange({grid_x}), np.arange({grid_y}))
                xpos = xpos.flatten()
                ypos = ypos.flatten()

                heights = np.sin(xpos / 2.0) * np.cos(ypos / 2.0) * {height_scale}

                fig_plotly = go.Figure()

                for x0, y0, h in zip(xpos, ypos, heights):
                    dx = {block_fraction}
                    dy = {block_fraction}
                    ox = x0 + (1 - dx) / 2
                    oy = y0 + (1 - dy) / 2
                    origin = (ox, oy, 0)
                    size = (dx, dy, h)
                    cuboid = create_cuboid_mesh(origin, size, "{line_color}")
                    fig_plotly.add_trace(cuboid)

                fig_plotly.update_layout(
                    title="{title}",
                    scene=dict(
                        xaxis_title="{xlabel}",
                        yaxis_title="{ylabel}",
                        zaxis_title="Höhe",
                    ),
                    paper_bgcolor="{fig_facecolor}",
                    plot_bgcolor="{fig_facecolor}",
                    width={int(fig_width * 100)},
                    height={int(fig_height * 100)},
                )

                fig_plotly.show()
                """
    return code
