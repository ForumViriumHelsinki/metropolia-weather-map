import os


def save_graph(file_name, plt):
    current_dir = os.path.dirname(os.path.realpath(__file__))
    save_path = os.path.join(f"{current_dir}/graphs", f"{file_name}.svg")
    plt.savefig(save_path)

    save_path = os.path.join(f"{current_dir}/graphs", f"{file_name}.png")
    plt.savefig(save_path)
