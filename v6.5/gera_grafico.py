from pathlib import Path
import copy
import plotly as py
import plotly.plotly as pyplot
import plotly.graph_objs as go
import plotly.io as pio
import os

pastas = ["C101_Het"]
vetor_x = [x for x in range(100)]

for pasta in pastas:
    path = pasta + "/" + pasta + "_Media.txt"
    file = Path(path)
    if(not file.is_file()):
        break
    with open(path, 'r') as f:
        vetor_y = []
        lines = f.readlines()
        for line in lines:
            vetor_y.append(float(line))
    trace = go.Scatter(
        x = vetor_x,
        y = vetor_y
    )
    # py.offline.init_notebook_mode(connected=True)
    fig = go.Figure()
    fig.add_scatter(
        x = vetor_x,
        y = vetor_y,
        mode = "lines"
    );
    # data = [trace]
    # py.offline.plot(fig)
    if not os.path.exists('images'):
        os.mkdir('images')
    pio.write_image(fig, 'images/' + pasta + '_Graph.png')
