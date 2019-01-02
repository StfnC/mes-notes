import io
import base64
import matplotlib

matplotlib.use('Agg')
import matplotlib.pyplot as plt

def build_graph(data):
    img = io.BytesIO()
    plt.figure(figsize=(11,6))
    subjects = list(data.keys())

    def get_all_values(index, labels, data):
        all_values = []
        for i in range(len(data)):
            label_values = []
            values = data.get(labels[i])
            for value in values:
                label_values.append(value[index])
            all_values.append(label_values)
        return all_values

    label_count = len(data)
    if label_count == 0:
        return None

    x_values = get_all_values(1, subjects, data)
    y_values = get_all_values(0, subjects, data)

    for i in range(len(data)):
        plt.gca().xaxis.set_major_formatter(matplotlib.dates.DateFormatter('%d-%m-%Y'))
        plt.plot(x_values[i], y_values[i], marker='o', markersize=8, linewidth=3, label=subjects[i])
        plt.gcf().autofmt_xdate()
        plt.legend()
    plt.savefig(img, format='png')
    img.seek(0)
    graph_url = base64.b64encode(img.getvalue()).decode()
    plt.close()
    return 'data:image/png;base64,{}'.format(graph_url)
