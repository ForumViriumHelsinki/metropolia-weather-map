import os


def save_graph(plt):
    current_dir = os.path.dirname(os.path.realpath(__file__))
    save_path = os.path.join(f"{current_dir}/graphs", "average_monthly_temperature.svg")
    plt.savefig(save_path)

    save_path = os.path.join(f"{current_dir}/graphs", "average_monthly_temperature.png")
    plt.savefig(save_path)
