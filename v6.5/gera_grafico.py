from pathlib import Path
import copy
import plotly as py
import plotly.plotly as pyplot
import plotly.graph_objs as go
import plotly.io as pio
import os

pastas = ["C102", "RC101", "RC102", "RC201", "RC202", "R202_Incerto"]
vetor_x = [x for x in range(1000)]

for pasta in pastas:
    if(pasta == "C102" or pasta == "R202_Incerto"):
        file_prefix = pasta[:4]
    else:
        file_prefix = pasta[:5]
    path = pasta + "/" + file_prefix + "_Media.txt"
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
    pio.write_image(fig, 'images/' + file_prefix + '_Graph.png')
