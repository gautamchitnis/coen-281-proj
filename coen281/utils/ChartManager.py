from io import BytesIO
from matplotlib import pyplot
import base64


class ChartManager:

    def get_bar_graph(self, x, y):
        pyplot.switch_backend('AGG')
        fig = pyplot.figure(figsize=(3.5, 3))

        pyplot.bar(x=x, height=y)

        pyplot.tight_layout()

        buffer = BytesIO()
        pyplot.savefig(buffer, format='png')
        buffer.seek(0)
        image_png = buffer.getvalue()
        graph = base64.b64encode(image_png)
        graph = graph.decode('utf-8')
        buffer.close()

        return graph

    def get_pie_chart(self, x, lbl, exp):
        pyplot.switch_backend('AGG')
        fig = pyplot.figure(figsize=(3.5, 3))

        pyplot.pie(x=x, labels=lbl)

        # pyplot.tight_layout()

        buffer = BytesIO()
        pyplot.savefig(buffer, format='png')
        buffer.seek(0)
        image_png = buffer.getvalue()
        graph = base64.b64encode(image_png)
        graph = graph.decode('utf-8')
        buffer.close()

        return graph
