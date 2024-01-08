import csv
import random
from datetime import datetime, timedelta

def gerar_temperaturas():
    return round(random.uniform(25, 26), 2)

data_inicio = datetime(2023, 11, 1)
proximos_x_meses = 3
janela_temporal = proximos_x_meses * 30 * 24  # Assumindo 30 dias por mês e 24h/dia
qtde_salas = 8

with open('recursos/temperaturas.csv', 'w', newline='') as csv_file:
    writer = csv.writer(csv_file)
    # Gerar header
    writer.writerow(['id_sala', 'horario', 'temperatura'])
    # Escreve os dados a cada hora na janela temporal selecionada
    for sala in range(1, qtde_salas + 1):
        for i in range(janela_temporal):
            timestamp = int((data_inicio + timedelta(hours=i)).timestamp())
            temperatura = gerar_temperaturas()
            writer.writerow([sala, timestamp, temperatura])

# Abrir o CSV novamente
rows = []
with open('recursos/temperaturas.csv', 'r') as csv_file:
    reader = csv.reader(csv_file)
    header = next(reader)
    for row in reader:
        rows.append(row)

# Add anomalias em X (Ex.: 15) temperaturas aleatórias
qtde_anomalias = 15
anomaly_indices = random.sample(range(len(rows)), qtde_anomalias)
for idx in anomaly_indices:
    # A anomalia estará entre a temperatura X a Y (Ex.: 5 a 10)
    rows[idx][2] = str(float(rows[idx][2]) + random.randint(5,10))  

# Salvar e fechar o arquivo
with open('recursos/temperaturas.csv', 'w', newline='') as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(header)
    writer.writerows(rows)
