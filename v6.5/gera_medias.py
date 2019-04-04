from pathlib import Path
import copy

pastas = ["R201_Het"]

for pasta in pastas:
    file_prefix = pasta[:4]
    all_datas = []
    for i in range(10):
        path = pasta + "/" + file_prefix + "_Het_" + str(i) + "_Ajustado.txt"
        file = Path(path)
        if(not file.is_file()):
            continue
        with open(path, 'r') as f:
            sequence = []
            lines = f.readlines()
            for line in lines:
                values = line.split(":")
                value = float(values[0])
                sequence.append(value)
        all_datas.append(sequence)
    vetor_media = []
    for i in range(1000):
        tot = 0
        for vetor in all_datas:
            tot += vetor[i]
        tot /= float(len(all_datas))
        vetor_media.append(tot)
    with open(pasta + "/" + file_prefix + "_Het_Media.txt", "w") as f:
        for value in vetor_media:
            f.write(str(value) + "\n")
