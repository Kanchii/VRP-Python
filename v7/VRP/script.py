import os
import subprocess

tamanho = [10, 9, 16, 13]

media = 0

for j in range(10):
    tot = 0
    for i, tam in enumerate(tamanho):
        # os.system("python main.py {} {}".format(tam, i))
        result = subprocess.Popen(['python', 'main.py', str(tam), str(i)], stdout = subprocess.PIPE, stderr = subprocess.STDOUT)
        total_distance = float(result.communicate()[0].replace('\n', ''))
        print("Resultado para o deposito #{}: {}".format(i + 1, total_distance))
        tot += total_distance
    print("Resultado da execucao #{}: {}".format(j + 1, tot))
    media += tot
print("Media final depois de 10 execucoes: {}".format(media / 10.0))
