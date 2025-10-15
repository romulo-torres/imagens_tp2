import subprocess
import time

inicio_tempo = time.time() # inicio do tempo

#OBS: Todos os arquivos que são de quadros identificados manualmente devem acabar com _manual.txt pro script funcionar
lista_videos = ["homem_aranha.mp4", "trivago.mp4", "flamengo_jornal.mp4", "minecraft_trailer.mp4", "old_town_road.mp4"] #Aqui tu coloca todos os arquivos manuais 


for video in lista_videos:
    limiar1 = '50000'
    limiar2 = '100000'
    nome_video = video.split(".mp4")[0] # Pegando só o nome sem o formato
    diretorio_chaves1 = f"cortes_chaves/{nome_video}_{limiar1}.txt"
    diretorio_id1 = f"cortes_identificados/{nome_video}_{limiar1}.txt"
    diretorio_chaves2 = f"cortes_chaves/{nome_video}_{limiar2}.txt"
    diretorio_id2 = f"cortes_identificados/{nome_video}_{limiar2}.txt"
    diretorio_manual = f"cortes_manuais/{nome_video}_manual.txt"
    diretorio_video = f"videos/{video}"
   

    #Limiar1
    subprocess.run(
        ['python3', 'detector_corte_histograma.py', diretorio_video, limiar1],
        capture_output=False,  # Captura a saída
        text=True  # Para garantir que a saída seja tratada como texto
    )

    subprocess.run(
        ['python3', 'estatisticas_quadros.py', diretorio_manual, diretorio_id1],
        capture_output=False,  # Captura a saída
        text=True  # Para garantir que a saída seja tratada como texto
    )

    #Limiar2
    subprocess.run(
        ['python3', 'detector_corte_histograma.py', diretorio_video, limiar2],
        capture_output=False,  # Captura a saída
        text=True  # Para garantir que a saída seja tratada como texto
    )

    subprocess.run(
        ['python3', 'estatisticas_quadros.py', diretorio_manual, diretorio_id2],
        capture_output=False,  # Captura a saída
        text=True  # Para garantir que a saída seja tratada como texto
    )

fim_tempo = time.time() # fim do tempo

print(f"Tempo de execução: {(fim_tempo - inicio_tempo)/60:.2f} minutos ({(fim_tempo - inicio_tempo):.2f} segundos)")