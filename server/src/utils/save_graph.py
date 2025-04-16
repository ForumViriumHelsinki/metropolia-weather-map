import os


def save_graph(file_name, plt, folder=None):
    base_path = os.path.join(os.path.dirname(__file__), "..", "analysis", "graphs")
    if folder:
        base_path = os.path.join(base_path, folder)

    svg_path = os.path.join(base_path, f"{file_name}.svg")
    png_path = os.path.join(base_path, f"{file_name}.png")

    plt.savefig(svg_path)
    plt.savefig(png_path)
