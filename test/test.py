import pandas as pd
import matplotlib.pyplot as plt

# CSV-Datei laden
df = pd.read_csv("Sinus_Daten.csv")

# Figure erstellen
fig = plt.figure(figsize=(8, 5), dpi=100)
fig.set_facecolor("#ffffff")


# Subplot: Großer Subplot
ax = fig.add_axes([0.05, 0.5, 0.9, 0.45])
ax.set_facecolor("#ffffff")

# Graph: Graph 2
ax.plot(df["X"], df["Kosinus"], 
        color="#00f900", 
        linestyle="solid", 
        linewidth=2.0, 
        marker="", 
        label="Graph 2")

# Graph: Graph 3
ax.plot(df["X"], df["Logarithmus"], 
        color="#00f900", 
        linestyle="solid", 
        linewidth=2.0, 
        marker="", 
        label="Graph 3")

# Achsen-Einstellungen
ax.set_xlim((0, 100))
ax.set_ylim((0, 100))
ax.set_xscale("linear")
ax.set_yscale("linear")
ax.set_title("Großer Subplot", fontsize=14)
ax.tick_params(axis='both', which='major', labelsize=10, 
               length=5, width=1, 
               colors="#000000")
ax.xaxis.label.set_color("#000000")
ax.yaxis.label.set_color("#000000")

# Raster aktivieren
ax.grid(True, linestyle="-", alpha=0.7)


# Subplot: Kleiner Subplot 1
ax = fig.add_axes([0.05, 0.05, 0.4, 0.35])
ax.set_facecolor("#ffffff")

# Graph: Graph 2
ax.plot(df["X"], df["Kosinus"], 
        color="#00f900", 
        linestyle="solid", 
        linewidth=2.0, 
        marker="", 
        label="Graph 2")

# Achsen-Einstellungen
ax.set_xlim((0, 100))
ax.set_ylim((0, 100))
ax.set_xscale("linear")
ax.set_yscale("linear")
ax.set_title("Kleiner Subplot 1", fontsize=14)
ax.tick_params(axis='both', which='major', labelsize=10, 
               length=5, width=1, 
               colors="#000000")
ax.xaxis.label.set_color("#000000")
ax.yaxis.label.set_color("#000000")

# Raster aktivieren
ax.grid(True, linestyle="-", alpha=0.7)


# Subplot: Kleiner Subplot 2
ax = fig.add_axes([0.55, 0.05, 0.4, 0.35])
ax.set_facecolor("#ffffff")

# Graph: Graph 3
ax.plot(df["X"], df["Logarithmus"], 
        color="#00f900", 
        linestyle="solid", 
        linewidth=2.0, 
        marker="", 
        label="Graph 3")

# Achsen-Einstellungen
ax.set_xlim((0, 100))
ax.set_ylim((0, 100))
ax.set_xscale("linear")
ax.set_yscale("linear")
ax.set_title("Kleiner Subplot 2", fontsize=14)
ax.tick_params(axis='both', which='major', labelsize=10, 
               length=5, width=1, 
               colors="#000000")
ax.xaxis.label.set_color("#000000")
ax.yaxis.label.set_color("#000000")

# Raster aktivieren
ax.grid(True, linestyle="-", alpha=0.7)

# Diagramm anzeigen
plt.show()