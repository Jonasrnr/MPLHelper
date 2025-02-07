import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import io, re
import utils

st.markdown(
    """
    <style>
    div[data-testid="stTabs"] {
        overflow-x: auto;
        white-space: nowrap;
        display: flex;
        flex-wrap: nowrap;
        scrollbar-width: thin;
        scrollbar-color: #888 #f1f1f1;
    }

    /* Optional: Ästhetische Scrollbar */
    div[data-testid="stTabs"]::-webkit-scrollbar {
        height: 6px;
    }
    
    div[data-testid="stTabs"]::-webkit-scrollbar-thumb {
        background-color: #888;
        border-radius: 10px;
    }

    div[data-testid="stTabs"]::-webkit-scrollbar-track {
        background: #f1f1f1;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <style>
    div[data-testid="stTabs"] {
        width: 100% !important;  /* Volle Breite */
        display: flex;
    }
    div[data-testid="stTabs"] > div {
        flex-grow: 1;
        width: 100% !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# 🌟 Initialisierung von Session State
if "used_y_columns" not in st.session_state:
    st.session_state.used_y_columns = set()

if "rerun_flag" not in st.session_state:
    st.session_state.rerun_flag = False

if "figure_settings" not in st.session_state:
    st.session_state.figure_settings = {
        "library": "Matplotlib",
        "fig_width": 8,
        "fig_height": 5,
        "dpi": 100,
        "background_color": "#ffffff",
        "axes_background_color": "#ffffff",
        "tight_layout": True,
        "xlim": (None, None),
        "ylim": (None, None),
        "xscale": "linear",
        "yscale": "linear",
        "grid": True,
        "grid_style": "--",
        "grid_alpha": 0.7,
        "invert_x": False,
        "invert_y": False,
        "title": "Mein Diagramm",
        "title_fontsize": 14,
        "legend": False,
        "legend_loc": "upper right",
        "legend_fontsize": 10,
        "font_family": "sans-serif",
        "axes_label_color": "#000000",
        "tick_label_color": "#000000",
        "tick_length": 5,
        "tick_width": 1,
        "graphs": [],
        "subplots": []
    }

if "expanders" not in st.session_state:
    st.session_state.expanders = {}

if "tab_titles" not in st.session_state:
    st.session_state.tab_titles = [f"Graph {i + 1}" for i in range(1)]

if "lines_settings" not in st.session_state:
    st.session_state.lines_settings = [{
        "label": f"Graph {i + 1}",
        "line_color": "#00f900",
        "line_width": 2.0,
        "line_style": "solid",
        "marker": "",
        "x_column": None,
        "y_column": None,
    } for i in range(1)]

if "subplot_titles" not in st.session_state:
    st.session_state.subplot_titles = [f"Subplot {i + 1}" for i in range(1)]

if "subplot_settings" not in st.session_state:
    st.session_state.subplot_settings = [{
        "title": f"Subplot {i + 1}",
        "graphs": [],
        "x": 0.1,
        "y": 0.1,
        "width": 0.8,
        "height": 0.8
    } for i in range(1)]

figure_settings = st.session_state.figure_settings

# 📂 Datei-Upload
uploaded_file = st.file_uploader("📂 Lade eine CSV-Datei hoch", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
else:
    # Test CSV data
    df = pd.read_csv("Sinus_Daten.csv")

# 📂 Sidebar mit Expandern für bessere Übersicht
with st.sidebar:
    st.header("⚙️ Figure-Einstellungen")

    # 📚 Allgemeine Einstellungen
    with st.expander("📚 Allgemeine Einstellungen", expanded=False):
        with st.popover("Titel"):
            figure_settings["title"] = st.text_input("📌 Diagrammtitel", figure_settings["title"])
            figure_settings["title_fontsize"] = st.slider("🖋️ Titelgröße", 8, 20, figure_settings["title_fontsize"])
        figure_settings["fig_width"] = st.slider("📏 Breite", 1, 50, figure_settings["fig_width"])
        figure_settings["fig_height"] = st.slider("📐 Höhe", 1, 50, figure_settings["fig_height"])
        figure_settings["dpi"] = st.slider("📌 DPI", 50, 300, figure_settings["dpi"])
        allg_col_1, allg_col_2 = st.columns(2)
        
    # 📊 Achseneinstellungen
    with st.expander("📊 Achseneinstellungen"):
        achs_col_1, achs_col_2 = st.columns(2)
        with achs_col_1:
            with st.popover("X-Achse"):
                figure_settings["xscale"] = st.selectbox("📏 X-Achsen-Skalierung", ["linear", "log"])
                figure_settings["xlim"] = st.number_input("🔍 X-Achsenbereich (min)", value=0), st.number_input("🔍 X-Achsenbereich (min)", value=100)
            
            figure_settings["axes_label_color"] = st.color_picker("Farbe der Achsentexte", figure_settings["axes_label_color"])
            figure_settings["tick_length"] = st.number_input("Tick-Länge", 1, 10, value=figure_settings["tick_length"])

        with achs_col_2:
            with st.popover("Y-Achse"):
                figure_settings["yscale"] = st.selectbox("📏 Y-Achsen-Skalierung", ["linear", "log"])
                figure_settings["ylim"] = st.number_input("🔍 Y-Achsenbereich (min)", value=0), st.number_input("🔍 Y-Achsenbereich (min)", value=100)
            
            figure_settings["tick_label_color"] = st.color_picker("Farbe der Achsenwerte", figure_settings["tick_label_color"])
            figure_settings["tick_width"] = st.number_input("Tick-Breite", 1, 5, value=figure_settings["tick_width"])

        figure_settings["grid"] = st.checkbox("📐 Raster anzeigen", figure_settings["grid"])
        figure_settings["grid_style"] = st.selectbox("🖌️ Rasterstil", ["-", "--", "-.", ":"])
        figure_settings["grid_alpha"] = st.slider("🌫️ Rastertransparenz", 0.1, 1.0, figure_settings["grid_alpha"])

    # 📈 Graphen
    with st.expander("📈 Graphen", expanded=False):
        tabs = st.tabs(st.session_state.tab_titles)

        new_lines_settings = []

        for i, tab in enumerate(tabs):
            with tab:
                new_label = st.text_input(
                    f"Name",
                    st.session_state.tab_titles[i],
                    key=f"tab_name_{i}",
                )

                if new_label != st.session_state.tab_titles[i]:
                    old_label = st.session_state.tab_titles[i]
                    st.session_state.tab_titles[i] = new_label

                    for subplot in st.session_state.subplot_settings:
                        subplot["graphs"] = [new_label if g == old_label else g for g in subplot["graphs"]]

                    st.rerun()

                line_color = st.color_picker(
                    f"Linienfarbe", st.session_state.lines_settings[i]["line_color"], key=f"color_{i}"
                )
                line_width = st.slider(
                    f"Linienbreite",
                    min_value=0.5,
                    max_value=5.0,
                    step=0.1,
                    value=st.session_state.lines_settings[i]["line_width"],
                    key=f"linewidth_{i}",
                )
                line_style = st.selectbox(
                    f"Linienstil",
                    ["solid", "dashed", "dashdot", "dotted"],
                    index=["solid", "dashed", "dashdot", "dotted"].index(st.session_state.lines_settings[i]["line_style"]),
                    key=f"style_{i}",
                )
                marker = st.selectbox(
                    f"Marker", ["", "o", "s", "^", "D"], index=["", "o", "s", "^", "D"].index(st.session_state.lines_settings[i]["marker"]), key=f"marker_{i}"
                )

                if st.session_state.lines_settings[i]["x_column"]:
                    x_column = st.selectbox(
                        f"X-Werte",
                        df.columns,
                        index=df.columns.get_loc(st.session_state.lines_settings[i]["x_column"]),
                        key=f"x_column_{i}",
                    )
                else:
                    x_column = df.columns[0]

                if st.session_state.lines_settings[i]["y_column"]:
                    y_column = st.selectbox(
                        f"Y-Werte",
                        df.columns,
                        index=df.columns.get_loc(st.session_state.lines_settings[i]["y_column"]),
                        key=f"y_column_{i}",
                    )
                else:
                    y_column = df.columns[1]
                    utils.update_selection()

                st.session_state.used_y_columns.add(y_column)

                new_lines_settings.append(
                    {
                        "label": new_label,
                        "line_color": line_color,
                        "line_width": line_width,
                        "line_style": line_style,
                        "marker": marker,
                        "x_column": x_column,
                        "y_column": y_column,
                    }
                )

                if st.button("🗑️" + st.session_state.tab_titles[i]+ " entfernen"):
                    if len(st.session_state.tab_titles) != 1:
                        st.session_state.tab_titles.pop(i)
                        st.session_state.lines_settings.pop(i)
                        if y_column:
                            st.session_state.used_y_columns.remove(y_column)
                    st.rerun()

        st.session_state.lines_settings = new_lines_settings

        if st.button("➕ Neuen Graph hinzufügen"):
            tset = {
                int(match.group(1)) 
                for item in st.session_state.tab_titles
                if (match := re.match(r"Graph (\d+)$", item)) 
            }
            i = 1
            while i in tset:
                i += 1
            
            y_column = next((col for col in df.columns[1:] if col not in st.session_state.used_y_columns), None)

            st.session_state.tab_titles.append(f"Graph {i}")
            st.session_state.lines_settings.append({
                "label": f"Graph {i}",
                "line_color": "#00f900",
                "line_width": 2.0,
                "line_style": "solid",
                "marker": "",
                "x_column": df.columns[0],
                "y_column": y_column
            })

            st.session_state.used_y_columns.add(y_column)

            st.rerun()

    # 📈 Subplots
    with st.expander("📈 Subplots", expanded=False):
        subplot_tabs = st.tabs(st.session_state.subplot_titles)

        new_subplot_settings = []

        for i, tab in enumerate(subplot_tabs):
            with tab:
                new_subplot_title = st.text_input(
                    f"Name",
                    st.session_state.subplot_titles[i],
                    key=f"subplot_name_{i}",
                )

                if new_subplot_title != st.session_state.subplot_titles[i]:
                    st.session_state.subplot_titles[i] = new_subplot_title
                    st.rerun()

                subplot_graphs = st.multiselect(
                    f"Graphen für {new_subplot_title}",
                    [d["label"] for d in st.session_state.lines_settings],
                    default=st.session_state.subplot_settings[i]["graphs"],
                    key=f"subplot_graphs_{i}"
                )

                sub_col_1, sub_col_2 = st.columns([3,3])
                
                with sub_col_1:
                    x = st.number_input(f"X-Position", -5.0, 5.0, st.session_state.subplot_settings[i]["x"], step=0.1, key=f"x_{i}")
                    y = st.number_input(f"Y-Position", -5.0, 5.0, st.session_state.subplot_settings[i]["y"], step=0.1, key=f"y_{i}")
                
                with sub_col_2:
                    width = st.number_input(f"Breite", 0.1, 5.0, st.session_state.subplot_settings[i]["width"], step=0.1, key=f"width_{i}")
                    height = st.number_input(f"Höhe", 0.1, 5.0, st.session_state.subplot_settings[i]["height"], step=0.1, key=f"height_{i}")

                # Check Überlappung
                st.session_state.subplot_settings = utils.adjust_subplot_positions(st.session_state.subplot_settings)


                new_subplot_settings.append(
                    {
                        "title": new_subplot_title,
                        "graphs": subplot_graphs,
                        "x": x,
                        "y": y,
                        "width": width,
                        "height": height
                    }
                )

                if st.button("🗑️" + st.session_state.subplot_titles[i]+ " entfernen"):
                    if len(st.session_state.subplot_titles) != 1:
                        st.session_state.subplot_titles.pop(i)
                        st.session_state.subplot_settings.pop(i)
                    st.rerun()

        st.session_state.subplot_settings = new_subplot_settings

        utils.subplot_layout_selector()

        if st.button("➕ Neuen Subplot hinzufügen"):
            tset = {
                int(match.group(1)) 
                for item in st.session_state.subplot_titles
                if (match := re.match(r"Subplot (\d+)$", item)) 
            }
            i = 1
            while i in tset:
                i += 1

            st.session_state.subplot_titles.append(f"Subplot {i}")
            st.session_state.subplot_settings.append({
                "title": f"Subplot {i}",
                "graphs": [],
                "x": 0.1,
                "y": 0.1,
                "width": 0.8,
                "height": 0.8
            })

            st.rerun()


    # 📖 Legende
    with st.sidebar.expander("📖 Legende"):
        figure_settings["legend"] = st.checkbox("📜 Legende anzeigen", figure_settings["legend"])
        figure_settings["legend_loc"] = st.selectbox("Legendenposition", ["upper right", "lower left", "upper left", "lower right"], index=["upper right", "lower left", "upper left", "lower right"].index(figure_settings["legend_loc"]))
        figure_settings["legend_fontsize"] = st.slider("Legenden-Schriftgröße", 8, 20, figure_settings["legend_fontsize"])
        figure_settings["font_family"] = st.selectbox("Schriftart", ["sans-serif", "serif", "monospace"], index=["sans-serif", "serif", "monospace"].index(figure_settings["font_family"]))

# 📊 Matplotlib-Plot erstellen
if figure_settings["library"] == "Matplotlib":
    fig = plt.figure(figsize=(figure_settings["fig_width"], figure_settings["fig_height"]), dpi=figure_settings["dpi"])
    fig.set_facecolor(figure_settings["background_color"])

    for subplot in st.session_state.subplot_settings:
        ax = fig.add_axes([subplot["x"], subplot["y"], subplot["width"], subplot["height"]])
        ax.set_facecolor(figure_settings["axes_background_color"])

        for graph_title in subplot["graphs"]:
            graph = next((g for g in st.session_state.lines_settings if g["label"] == graph_title), None)
            if graph and graph["x_column"] and graph["y_column"]:
                ax.plot(df[graph["x_column"]], df[graph["y_column"]], color=graph["line_color"], label=graph["label"], linestyle=graph["line_style"], linewidth=graph["line_width"], marker=graph["marker"])

        ax.set_xlim(figure_settings["xlim"])
        ax.set_ylim(figure_settings["ylim"])
        ax.set_xscale(figure_settings["xscale"])
        ax.set_yscale(figure_settings["yscale"])
        ax.set_title(subplot["title"], fontsize=figure_settings["title_fontsize"])

        if figure_settings["legend"]:
            ax.legend(loc=figure_settings["legend_loc"], fontsize=figure_settings["legend_fontsize"])

        if figure_settings["grid"]:
            ax.grid(True, linestyle=figure_settings["grid_style"], alpha=figure_settings["grid_alpha"])

        ax.tick_params(axis='both', which='major', labelsize=figure_settings["legend_fontsize"], length=figure_settings["tick_length"], width=figure_settings["tick_width"], colors=figure_settings["tick_label_color"])
        ax.xaxis.label.set_color(figure_settings["axes_label_color"])
        ax.yaxis.label.set_color(figure_settings["axes_label_color"])

    st.pyplot(fig)

    fig.update_layout(
        title=figure_settings["title"],
        width=figure_settings["fig_width"] * 100,
        height=figure_settings["fig_height"] * 100,
        legend=dict(font=dict(size=figure_settings["legend_fontsize"]), orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        paper_bgcolor=figure_settings["background_color"],
        plot_bgcolor=figure_settings["axes_background_color"],
        font=dict(family=figure_settings["font_family"])
    )

    st.plotly_chart(fig)

# 🔗 Python-Code zum Kopieren generieren
code = utils.generate_code()

st.code(code, language="python")

# 📥 Download-Funktion für PNG
if figure_settings["library"] == "Matplotlib" and fig:
    img_buf = io.BytesIO()
    fig.savefig(img_buf, format="png")
    st.download_button("📥 Diagramm als PNG herunterladen", img_buf, "diagramm.png", "image/png")


if st.session_state.rerun_flag:
    st.session_state.rerun_flag = False
    st.rerun()