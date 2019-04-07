from pathlib import Path
import copy
import os
import matplotlib.pyplot as plt

pastas = ["C101_Het_FC_1.0", "C101_Het_FC_1.5",
          "C101_Het_FC_1.8", "C101_Het_FC_1.9",
          "C101_Het_FC_1.85", "C101_Het_FC_1.95",
          "C101_Het_FC_2.1", "C101_Het_FC_2.2",
          "C101_Het_FC_2.05", "C101_Het_FC_2.5",
          "C101_Het_FC_2.15", "C101_Het_FC_3.0"]

qtd_x = 200
vetor_x = [x for x in range(qtd_x)]

vetor_padrao = []
with open("C101_Het/C101_Het_Media.txt", 'r') as f:
    lines = f.readlines()
    for idx, line in enumerate(lines):
        if(idx == qtd_x):
            break
        vetor_padrao.append(float(line))

for pasta in pastas:
    path = pasta + "/" + pasta + "_Media.txt"
    file = Path(path)
    if(not file.is_file()):
        break
    cnt = 0
    with open(path, 'r') as f:
        vetor_y = []
        lines = f.readlines()
        for idx, line in enumerate(lines):
            if(idx == qtd_x):
                break
            vetor_y.append(float(line))
    
    line_1 = plt.plot(vetor_x, vetor_padrao, label='α = 2.0')
    line_2 = plt.plot(vetor_x, vetor_y, linestyle='--',
                      label='α = ' + pasta[12:])
    plt.legend(bbox_to_anchor=(0.9, 0.88),
               bbox_transform=plt.gcf().transFigure)

    plt.xlabel('Iteration')
    plt.ylabel('Total distance')
    plt.title(pasta + " x C101")
    plt.show()
    # data = [trace]
    # py.offline.plot(fig)
    # if not os.path.exists('images'):
    #     os.mkdir('images')
    # pio.write_image(fig, 'images/' + pasta + '_Graph.png')
