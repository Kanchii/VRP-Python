from pathlib import Path
import copy

pastas = ["C101_Het"]

for pasta in pastas:
    for i in range(11):
        path = pasta + "/" + pasta + "_" + str(i) + ".txt"
        file = Path(path)
        if(not file.is_file()):
            continue
        with open(path, 'r') as f:
            best_sequence = []
            sequence = []
            lines = f.readlines()
            for line in lines:
                values = line.split(":")
                value = float(values[1])
                vehicle = int(values[2])
                if(sequence != []):
                    if(value > sequence[-1][0]):
                        if(best_sequence != []):
                            if(sequence[-1][0] < best_sequence[-1][0]):
                                best_sequence = copy.deepcopy(sequence)
                            elif(sequence[-1][0] == best_sequence[-1][0] and len(sequence) < len(best_sequence)):
                                best_sequence = copy.deepcopy(sequence)
                        else:
                            best_sequence = copy.deepcopy(sequence)
                        sequence = []
                sequence.append((value, vehicle))
            if(best_sequence == []):
                best_sequence = copy.deepcopy(sequence)
            else:
                if(sequence[-1][0] < best_sequence[-1][0]):
                    best_sequence = copy.deepcopy(sequence)
                elif(best_sequence[-1][0] == sequence[-1][0] and len(sequence) < len(best_sequence)):
                    best_sequence = copy.deepcopy(sequence)
            while(len(best_sequence) < 1000):
                best_sequence.append(best_sequence[-1])
        with open(pasta + "/" + pasta + "_" + str(i) + "_Ajustado.txt", "w") as f:
            for par in best_sequence:
                f.write(str(par[0]) + ":" + str(par[1]) + "\n")
