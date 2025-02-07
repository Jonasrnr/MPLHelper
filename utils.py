import plotly.graph_objects as go
import math

def create_cuboid_mesh(origin, size, color):
    x0, y0, z0 = origin
    dx, dy, dz = size

    x = [x0, x0 + dx, x0 + dx, x0, x0, x0 + dx, x0 + dx, x0]
    y = [y0, y0, y0 + dy, y0 + dy, y0, y0, y0 + dy, y0 + dy]
    z = [z0, z0, z0, z0, z0 + dz, z0 + dz, z0 + dz, z0 + dz]

    bottom_i = [0, 0]
    bottom_j = [1, 2]
    bottom_k = [2, 3]

    top_i = [4, 4]
    top_j = [5, 6]
    top_k = [6, 7]

    front_i = [0, 0]
    front_j = [1, 5]
    front_k = [5, 4]

    right_i = [1, 1]
    right_j = [2, 6]
    right_k = [6, 5]

    back_i = [2, 2]
    back_j = [3, 7]
    back_k = [7, 6]

    left_i = [3, 3]
    left_j = [0, 4]
    left_k = [4, 7]

    i = bottom_i + top_i + front_i + right_i + back_i + left_i
    j = bottom_j + top_j + front_j + right_j + back_j + left_j
    k = bottom_k + top_k + front_k + right_k + back_k + left_k

    return go.Mesh3d(
        x=x, y=y, z=z, i=i, j=j, k=k, color=color, opacity=1, flatshading=True
    )

def update_selection():
    """
    Ruft indirekt die st.rerun()-Funktion auf, um die Auswahl zu aktualisieren.
    """
    st.session_state.rerun_flag = True

def adjust_subplot_positions(subplot_settings):
    """
    Prüft, ob sich Subplots überlappen, und verschiebt sie automatisch so,
    dass keine Überlappungen auftreten.
    """
    adjusted_subplots = []
    
    for i, subplot in enumerate(subplot_settings):
        x, y, width, height = subplot["x"], subplot["y"], subplot["width"], subplot["height"]
        
        # Überprüfe, ob sich dieser Subplot mit einem der vorherigen überlappt
        overlap = True
        while overlap:
            overlap = False
            for j, other_subplot in enumerate(adjusted_subplots):
                ox, oy, owidth, oheight = other_subplot["x"], other_subplot["y"], other_subplot["width"], other_subplot["height"]
                
                if not (x + width <= ox or x >= ox + owidth or y + height <= oy or y >= oy + oheight):
                    # Überlappung erkannt! Wir verschieben den aktuellen Subplot nach unten
                    y -= 0.1  # Schrittweise nach unten verschieben
                    overlap = True
                    break  # Noch einmal überprüfen
            
        adjusted_subplots.append({"title": subplot["title"], "graphs": subplot["graphs"], "x": x, "y": y, "width": width, "height": height})

    return adjusted_subplots

import streamlit as st

def get_preset_layout(layout_type):
    """Gibt eine vordefinierte Subplot-Anordnung zurück."""
    if layout_type == "2x2 Raster":
        return [
            {"title": "Subplot 1", "graphs": [], "x": 0.1, "y": 0.55, "width": 0.35, "height": 0.35},
            {"title": "Subplot 2", "graphs": [], "x": 0.55, "y": 0.55, "width": 0.35, "height": 0.35},
            {"title": "Subplot 3", "graphs": [], "x": 0.1, "y": 0.1, "width": 0.35, "height": 0.35},
            {"title": "Subplot 4", "graphs": [], "x": 0.55, "y": 0.1, "width": 0.35, "height": 0.35},
        ]
    
    elif layout_type == "1 Spalte, 3 Zeilen":
        return [
            {"title": "Subplot 1", "graphs": [], "x": 0.1, "y": 0.80, "width": 0.8, "height": 0.3},
            {"title": "Subplot 2", "graphs": [], "x": 0.1, "y": 0.4, "width": 0.8, "height": 0.3},
            {"title": "Subplot 3", "graphs": [], "x": 0.1, "y": 0.0, "width": 0.8, "height": 0.3},
        ]

    elif layout_type == "3 Spalten, 1 Zeile":
        return [
            {"title": "Subplot 1", "graphs": [], "x": 0.05, "y": 0.1, "width": 0.3, "height": 0.8},
            {"title": "Subplot 2", "graphs": [], "x": 0.45, "y": 0.1, "width": 0.3, "height": 0.8},
            {"title": "Subplot 3", "graphs": [], "x": 0.85, "y": 0.1, "width": 0.3, "height": 0.8},
        ]

    elif layout_type == "Grid 3x3":
        return [
            {"title": "Subplot 1", "graphs": [], "x": 0.05, "y": 0.65, "width": 0.25, "height": 0.25},
            {"title": "Subplot 2", "graphs": [], "x": 0.36, "y": 0.65, "width": 0.25, "height": 0.25},
            {"title": "Subplot 3", "graphs": [], "x": 0.67, "y": 0.65, "width": 0.25, "height": 0.25},
            {"title": "Subplot 4", "graphs": [], "x": 0.05, "y": 0.36, "width": 0.25, "height": 0.25},
            {"title": "Subplot 5", "graphs": [], "x": 0.36, "y": 0.36, "width": 0.25, "height": 0.25},
            {"title": "Subplot 6", "graphs": [], "x": 0.67, "y": 0.36, "width": 0.25, "height": 0.25},
            {"title": "Subplot 7", "graphs": [], "x": 0.05, "y": 0.07, "width": 0.25, "height": 0.25},
            {"title": "Subplot 8", "graphs": [], "x": 0.36, "y": 0.07, "width": 0.25, "height": 0.25},
            {"title": "Subplot 9", "graphs": [], "x": 0.67, "y": 0.07, "width": 0.25, "height": 0.25},
        ]

    elif layout_type == "3 Zeilen, 2 Spalten (Hochformat)":
        return [
            {"title": "Subplot 1", "graphs": [], "x": 0.05, "y": 0.75, "width": 0.4, "height": 0.3},
            {"title": "Subplot 2", "graphs": [], "x": 0.55, "y": 0.75, "width": 0.4, "height": 0.3},
            {"title": "Subplot 3", "graphs": [], "x": 0.05, "y": 0.4, "width": 0.4, "height": 0.3},
            {"title": "Subplot 4", "graphs": [], "x": 0.55, "y": 0.4, "width": 0.4, "height": 0.3},
            {"title": "Subplot 5", "graphs": [], "x": 0.05, "y": 0.05, "width": 0.4, "height": 0.3},
            {"title": "Subplot 6", "graphs": [], "x": 0.55, "y": 0.05, "width": 0.4, "height": 0.3},
        ]

    elif layout_type == "1 großes + 2 kleine unten":
        return [
            {"title": "Großer Subplot", "graphs": [], "x": 0.05, "y": 0.50, "width": 0.9, "height": 0.45},
            {"title": "Kleiner Subplot 1", "graphs": [], "x": 0.05, "y": 0.05, "width": 0.4, "height": 0.35},
            {"title": "Kleiner Subplot 2", "graphs": [], "x": 0.55, "y": 0.05, "width": 0.4, "height": 0.35},
        ]

    elif layout_type == "4 Spalten, 2 Zeilen":
        return [
            {"title": f"Subplot {i+1}", "graphs": [], 
             "x": 0.05 + (i % 4) * 0.22, 
             "y": 0.55 - (i // 4) * 0.45, 
             "width": 0.2, "height": 0.4} for i in range(8)
        ]

    elif layout_type == "1 großes oben, 3 kleine unten":
        return [
            {"title": "Großer Subplot", "graphs": [], "x": 0.05, "y": 0.55, "width": 1.04, "height": 0.4},
            {"title": "Kleiner Subplot 1", "graphs": [], "x": 0.05, "y": 0.05, "width": 0.3, "height": 0.35},
            {"title": "Kleiner Subplot 2", "graphs": [], "x": 0.42, "y": 0.05, "width": 0.3, "height": 0.35},
            {"title": "Kleiner Subplot 3", "graphs": [], "x": 0.79, "y": 0.05, "width": 0.3, "height": 0.35},
        ]

    elif layout_type == "Ringförmig":
        return (
            [{"title": "Mitte", "graphs": [], "x": 0.4, "y": 0.4, "width": 0.2, "height": 0.2}]
            + [{"title": f"Außen {i+1}", "graphs": [], 
                "x": 0.4 + 0.3 * math.cos(i * 2 * math.pi / 6), 
                "y": 0.4 + 0.3 * math.sin(i * 2 * math.pi / 6), 
                "width": 0.15, "height": 0.15} for i in range(6)]
        )

    else:
        return []


def subplot_layout_selector():
    """Zeigt ein Popover für vordefinierte Subplot-Layouts in Streamlit an."""
    with st.popover("🎛️ Vordefinierte Subplot-Layouts wählen", help="⚠️ ACHTUNG! Löscht alle bisherigen Subplot Einstellungen"):
        layout_options = [
            "2x2 Raster", 
            "1 Spalte, 3 Zeilen", 
            "3 Spalten, 1 Zeile", 
            "Grid 3x3",
            "3 Zeilen, 2 Spalten",
            "1 großes + 2 kleine unten",
            "4 Spalten, 2 Zeilen",
            "1 großes oben, 3 kleine unten",
            "Ringförmig"
        ]

        selected_layout = st.radio("📊 Wähle eine Anordnung", layout_options)

        if st.button("Übernehmen", help="⚠️ ACHTUNG! Löscht alle bisherigen Subplot Einstellungen"):
            st.session_state.subplot_settings = get_preset_layout(selected_layout)
            st.session_state.subplot_titles = [subplot["title"] for subplot in st.session_state.subplot_settings]
            st.rerun()

def generate_code():
    """Generiert Python-Code für Matplotlib basierend auf den aktuellen Einstellungen."""
    
    figure_settings = st.session_state.figure_settings
    subplot_settings = st.session_state.subplot_settings
    lines_settings = st.session_state.lines_settings

    code = f"""import pandas as pd
import matplotlib.pyplot as plt

# CSV-Datei laden
df = pd.read_csv("deine_datei.csv")

# Figure erstellen
fig = plt.figure(figsize=({figure_settings["fig_width"]}, {figure_settings["fig_height"]}), dpi={figure_settings["dpi"]})
fig.set_facecolor("{figure_settings["background_color"]}")

"""

    # Subplots generieren
    for subplot in subplot_settings:
        code += f"""
# Subplot: {subplot["title"]}
ax = fig.add_axes([{subplot["x"]}, {subplot["y"]}, {subplot["width"]}, {subplot["height"]}])
ax.set_facecolor("{figure_settings["axes_background_color"]}")
"""

        for graph in subplot["graphs"]:
            graph_data = next((g for g in lines_settings if g["label"] == graph), None)
            if graph_data and graph_data["x_column"] and graph_data["y_column"]:
                code += f"""
# Graph: {graph_data["label"]}
ax.plot(df["{graph_data["x_column"]}"], df["{graph_data["y_column"]}"], 
        color="{graph_data["line_color"]}", 
        linestyle="{graph_data["line_style"]}", 
        linewidth={graph_data["line_width"]}, 
        marker="{graph_data["marker"]}", 
        label="{graph_data["label"]}")
"""

        code += f"""
# Achsen-Einstellungen
ax.set_xlim({figure_settings["xlim"]})
ax.set_ylim({figure_settings["ylim"]})
ax.set_xscale("{figure_settings["xscale"]}")
ax.set_yscale("{figure_settings["yscale"]}")
ax.set_title("{subplot["title"]}", fontsize={figure_settings["title_fontsize"]})
ax.tick_params(axis='both', which='major', labelsize={figure_settings["legend_fontsize"]}, 
               length={figure_settings["tick_length"]}, width={figure_settings["tick_width"]}, 
               colors="{figure_settings["tick_label_color"]}")
ax.xaxis.label.set_color("{figure_settings["axes_label_color"]}")
ax.yaxis.label.set_color("{figure_settings["axes_label_color"]}")

# Raster aktivieren
ax.grid({figure_settings["grid"]}, linestyle="{figure_settings["grid_style"]}", alpha={figure_settings["grid_alpha"]})

"""
        if figure_settings["legend"]:
            code += f"""
# Legende hinzufügen
ax.legend(loc="{figure_settings["legend_loc"]}", fontsize={figure_settings["legend_fontsize"]})"""

    code += """# Diagramm anzeigen
plt.show()
"""

    return code

