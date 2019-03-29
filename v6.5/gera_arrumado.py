from pathlib import Path
import copy

pastas = ["C102", "RC101", "RC102", "RC201", "RC202", "R202_Incerto"]

for pasta in pastas:
    if(pasta == "C102" or pasta == "R202_Incerto"):
        file_prefix = pasta[:4]
    else:
        file_prefix = pasta[:5]
    for i in range(10):
        path = pasta + "/" + file_prefix + "_" + str(i) + ".txt"
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
                if(sequence != []):
                    if(value > sequence[-1]):
                        if(best_sequence != []):
                            if(sequence[-1] < best_sequence[-1]):
                                best_sequence = copy.deepcopy(sequence)
                            elif(sequence[-1] == best_sequence[-1] and len(sequence) < len(best_sequence)):
                                best_sequence = copy.deepcopy(sequence)
                        else:
                            best_sequence = copy.deepcopy(sequence)
                        sequence = []
                sequence.append(value)
            if(best_sequence == []):
                best_sequence = copy.deepcopy(sequence)
            else:
                if(sequence[-1] < best_sequence[-1]):
                    best_sequence = copy.deepcopy(sequence)
                elif(best_sequence[-1] == sequence[-1] and len(sequence) < len(best_sequence)):
                    best_sequence = copy.deepcopy(sequence)
            while(len(best_sequence) < 1000):
                best_sequence.append(best_sequence[-1])
        with open(pasta + "/" + file_prefix + "_" + str(i) + "_Ajustado.txt", "w") as f:
            for value in best_sequence:
                f.write(str(value) + "\n")
