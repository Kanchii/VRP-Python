from pathlib import Path
import copy
import plotly as py
import plotly.plotly as pyplot
import plotly.graph_objs as go
import plotly.io as pio
import os

pastas = ["C101_Certos_ParAN_FC_1_3", "C101_ParAN_FC_2_7"]
other = ["FC_1.3", "FC_2.7"]
cnt = 0
for pasta in pastas:
    vetor_y = []
    for i in range(5):
        file_prefix = pasta[:4]
        path = pasta + "/" + file_prefix + "_" + str(i) + "_Ajustado.txt"
        file = Path(path)
        if(not file.is_file()):
            break
        with open(path, 'r') as f:
            lines = f.readlines()
            vetor_y.append(float(lines[-1]))
    trace = go.Box(
        y = vetor_y
    )
    # print(vetor_y)
        # py.offline.init_notebook_mode(connected=True)
    data = [trace]
    fig = go.Figure(data = data)
    # fig.add_box(
    #     y = vetor_y
    # );
    # data = [trace]
    # py.offline.plot(fig)
    if not os.path.exists('boxplots'):
        os.mkdir('boxplots')
    pio.write_image(fig, 'boxplots/' + file_prefix + "_" + other[cnt] + '_BoxPlot.png')
    cnt += 1
