ufrom pycomm3 import LogixDriver
from datetime import datetime
from time import sleep
import csv

def atualizar_temperaturas():
    lista_de_dados = []
    # Horário
    timestamp = int(datetime.timestamp(datetime.now()))
    # Baixar os dados
    with LogixDriver('192.168.1.36') as clp:
        dados = clp.read('Program:MainProgram.temp_salas{8}').value
    for id_num in range(8):
        lista_de_dados.append({'id_sala': id_num+1, 'horario': timestamp, 'temperatura': format(dados[id_num],'.2f')})
    # Gerar CSV
    with open('temperaturas.csv', 'a', newline='') as csv_file:
        fieldnames = ['id_sala', 'horario','temperatura']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

        # Write data
        writer.writerows(lista_de_dados)

while True:
    atualizar_temperaturas()
    print(f"{datetime.now().strftime('%H:%M')} Banco de Dados atualizado!")
    sleep(60)