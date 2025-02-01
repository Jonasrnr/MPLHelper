import streamlit as st
from plots.plot_2d import plot_2d
from plots.plot_3d import plot_3d
from plots.plot_3d_block import plot_3d_block
from utils import create_cuboid_mesh
from config import PlotType
import config
from code_generator import generate_python_code
from io import BytesIO
import pandas as pd

st.set_page_config(page_title="Matplotlib Diagramm Generator", layout="wide")

st.markdown(
    """
    <style>
    .block-container {
        max-width: 800px;
        margin-left: auto;
        margin-top: auto;
        margin-bottom: auto;
        margin-right: auto;
    }
    /*Plot-Container (2D)*/
    .stPlot > div {
        max-width: 800px;
        margin-left: auto;
        margin-top: auto;
        margin-bottom: auto;
        margin-right: auto;
    }

    /*Siedbar*/
    [data-testid="stSidebar"] > div:first-child {
        width: 100px;  /* Ändere diesen Wert nach Bedarf */
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("Matplotlib Diagramm Generator - Erweiterte Einstellungen")

# ---------------------------
# Alle Einstellungen in der Sidebar
# ---------------------------
st.sidebar.header("Einstellungen")

# --- Diagrammtyp Einstellungen ---
plot_type = st.sidebar.selectbox("Wähle den Diagrammtyp", [e.value for e in PlotType])

with st.sidebar.expander("Eigene Daten verwenden"):
    # --- Daten hochladen ---
    uploaded_file = st.file_uploader("Lade deine CSV-Datei hoch", type=["csv"])

    if uploaded_file is not None:
        data = pd.read_csv(uploaded_file)
        st.write("Datenvorschau:")
        st.write(data.head())
    else:
        data = None

# --- Figure Einstellungen ---
with st.sidebar.expander("Plot", expanded=False):
    fig_width = config.DEFAULT_FIG_WIDTH
    fig_height = config.DEFAULT_FIG_HEIGHT
    fig_facecolor = st.color_picker("Figur Hintergrundfarbe", "#FFFFFF")
    fig_edgecolor = config.DEFAULT_FIG_EDGECOLOR
    title_fontsize = st.number_input("Titel Schriftgröße", value=14, step=1)
    title = st.text_input("Titel", "Mein Plot")
    font_family = st.selectbox("Schriftfamilie", ["sans-serif", "serif", "monospace"])

# --- Axes Einstellungen ---
with st.sidebar.expander("Axen", expanded=False):
    axes_facecolor = st.color_picker("Achsen Hintergrundfarbe", "#FFFFFF")

# --- Lines Einstellungen ---
if "tab_titles" not in st.session_state:
    st.session_state.tab_titles = [f"Graph {i + 1}" for i in range(1)]

if "lines_settings" not in st.session_state:
    st.session_state.lines_settings = []

with st.sidebar.expander("Graphen", expanded=False):
    num_lines = st.number_input(
        "Anzahl der Graphen",
        min_value=1,
        value=len(st.session_state.tab_titles),
        step=1,
    )

    if num_lines != len(st.session_state.tab_titles):
        if num_lines > len(st.session_state.tab_titles):
            for i in range(len(st.session_state.tab_titles), num_lines):
                st.session_state.tab_titles.append(f"Graph {i + 1}")
        else:
            st.session_state.tab_titles = st.session_state.tab_titles[:num_lines]

    tabs = st.tabs(st.session_state.tab_titles)

    new_lines_settings = []

    for i, tab in enumerate(tabs):
        with tab:
            new_label = st.text_input(
                f"Tab Name für Graph {i + 1}",
                st.session_state.tab_titles[i],
                key=f"tab_name_{i}",
            )

            if new_label != st.session_state.tab_titles[i]:
                st.session_state.tab_titles[i] = new_label
                st.rerun()

            line_color = st.color_picker(
                f"Linienfarbe {i + 1}", "#00f900", key=f"color_{i}"
            )
            line_width = st.slider(
                f"Linienbreite {i + 1}",
                min_value=0.5,
                max_value=5.0,
                step=0.1,
                value=2.0,
                key=f"width_{i}",
            )
            line_style = st.selectbox(
                f"Linienstil {i + 1}",
                ["solid", "dashed", "dashdot", "dotted"],
                key=f"style_{i}",
            )
            marker = st.selectbox(
                f"Marker {i + 1}", ["", "o", "s", "^", "D"], key=f"marker_{i}"
            )

            new_lines_settings.append(
                {
                    "label": new_label,
                    "line_color": line_color,
                    "line_width": line_width,
                    "line_style": line_style,
                    "marker": marker,
                }
            )

    st.session_state.lines_settings = new_lines_settings

# --- Grid Einstellungen ---
with st.sidebar.expander("Grid", expanded=False):
    show_grid = st.checkbox("Zeige Grid", value=True)
    grid_color = st.color_picker("Grid Farbe", "#CCCCCC")
    grid_linestyle = st.selectbox(
        "Grid Linienstil", ["solid", "dashed", "dashdot", "dotted"]
    )
    grid_linewidth = st.slider(
        "Grid Linienbreite", min_value=0.1, max_value=3.0, step=0.1, value=0.8
    )

# --- Legend Einstellungen ---
with st.sidebar.expander("Legende", expanded=False):
    show_legend = st.checkbox("Zeige Legende", value=False)
    legend_location = st.selectbox(
        "Legenden Position",
        ["best", "upper right", "upper left", "lower left", "lower right"],
    )
    legend_fontsize = st.number_input("Legenden Schriftgröße", value=10, step=1)
    legend_facecolor = st.color_picker("Legenden Hintergrundfarbe", "#FFFFFF")

# --- Achsenbeschriftung Einstellungen ---
with st.sidebar.expander("Achsenbeschriftung", expanded=False):
    xlabel = st.text_input("X-Achse Beschriftung", "X-Achse")
    ylabel = st.text_input("Y-Achse Beschriftung", "Y-Achse")
    if plot_type == PlotType.PLOT_3D.value or plot_type == PlotType.PLOT_3D_BLOCK.value:
        zlabel = st.text_input("Z-Achse Beschriftung", "Z-Achse")
    xlabel_fontsize = st.number_input("X-Achse Schriftgröße", value=12, step=1)
    ylabel_fontsize = st.number_input("Y-Achse Schriftgröße", value=12, step=1)
    if plot_type == PlotType.PLOT_3D.value or plot_type == PlotType.PLOT_3D_BLOCK.value:
        zlabel_fontsize = st.number_input("Z-Achse Schriftgröße", value=12, step=1)

grid_x = grid_y = block_fraction = height_scale = line_color = zlabel = (
    zlabel_fontsize
) = None
if plot_type == PlotType.PLOT_3D_BLOCK.value:
    with st.sidebar.expander("Special", expanded=False):
        grid_x = st.number_input(
            "Anzahl Segmente in X-Richtung", min_value=1, value=10, step=1
        )
        grid_y = st.number_input(
            "Anzahl Segmente in Y-Richtung", min_value=1, value=10, step=1
        )
        block_fraction = st.slider(
            "Blockgröße (relativ)", min_value=0.1, max_value=1.0, value=0.8
        )
        height_scale = st.slider(
            "Höhen-Skalierungsfaktor", min_value=0.1, max_value=10.0, value=5.0
        )
        line_color = st.color_picker("Block Farbe", "#00f900")

# ---------------------------
# Hauptbereich: Plot-Vorschau & generierter Code
# ---------------------------
st.subheader("Diagramm-Vorschau")
if plot_type == PlotType.PLOT_2D.value:
    fig = plot_2d(
        fig_width,
        fig_height,
        fig_facecolor,
        fig_edgecolor,
        axes_facecolor,
        st.session_state.lines_settings,
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
        data,
    )
elif plot_type == PlotType.PLOT_3D.value:
    fig = plot_3d(
        fig_width,
        fig_height,
        fig_facecolor,
        fig_edgecolor,
        axes_facecolor,
        st.session_state.lines_settings,
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
        data,
    )
elif plot_type == PlotType.PLOT_3D_BLOCK.value:
    fig = plot_3d_block(
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
        data,
    )

# ---------------------------
# Generierter Python-Code
# ---------------------------
st.markdown("---")
st.subheader("Generierter Python-Code")

# Option to choose between Matplotlib and Plotly for 3D plots
code_library = st.segmented_control(
    "Library", ["Matplotlib", "Plotly"], selection_mode="single"
)

generated_code = generate_python_code(
    plot_type,
    fig_width,
    fig_height,
    fig_facecolor,
    fig_edgecolor,
    axes_facecolor,
    st.session_state.lines_settings,
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
    grid_x,
    grid_y,
    block_fraction,
    height_scale,
    line_color,
    code_library,
)
st.code(generated_code, language="python")
st.download_button(
    label="Download Python-Code",
    data=generated_code,
    file_name="generated_plot.py",
    mime="text/x-python",
)

# ---------------------------
# Download Plot as PNG
# ---------------------------
buf = BytesIO()
if fig:
    if plot_type == PlotType.PLOT_2D.value:
        fig.savefig(buf, format="png")
    elif plot_type == PlotType.PLOT_3D.value:
        fig.write_image(buf, format="png")
    elif plot_type == PlotType.PLOT_3D_BLOCK.value:
        fig.write_image(buf, format="png")
    buf.seek(0)


def cb():
    buf = BytesIO()


st.download_button(
    on_click=cb(),
    label="Download Plot (PNG)",
    data=buf,
    file_name="plot.png",
    mime="image/png",
)
