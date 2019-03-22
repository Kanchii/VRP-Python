from pathlib import Path
import copy

pastas = ["C102", "RC101", "RC102", "RC201", "RC202", "R202_Incerto"]

for pasta in pastas:
    if(pasta == "C102" or pasta == "R202_Incerto"):
        file_prefix = pasta[:4]
    else:
        file_prefix = pasta[:5]
    all_datas = []
    for i in range(10):
        path = pasta + "/" + file_prefix + "_" + str(i) + "_Ajustado.txt"
        file = Path(path)
        if(not file.is_file()):
            continue
        with open(path, 'r') as f:
            sequence = []
            lines = f.readlines()
            for line in lines:
                value = float(line)
                sequence.append(value)
        all_datas.append(sequence)
    vetor_media = []
    for i in range(1000):
        tot = 0
        for vetor in all_datas:
            tot += vetor[i]
        tot /= float(len(all_datas))
        vetor_media.append(tot)
    with open(pasta + "/" + file_prefix + "_Media.txt", "w") as f:
        for value in vetor_media:
            f.write(str(value) + "\n")
