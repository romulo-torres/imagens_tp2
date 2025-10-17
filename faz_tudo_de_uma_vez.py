import subprocess
import time

inicio_tempo = time.time() # inicio do tempo

#OBS: Todos os arquivos que são de quadros identificados manualmente devem acabar com _manual.txt pro script funcionar. Tem que colocar cada um desses na pasta de cortes_manuais
lista_videos = ["homem_aranha.mp4", "trivago.mp4", "flamengo_jornal.mp4", "minecraft_trailer.mp4", "old_town_road.mp4"
""] #Aqui tu coloca todos os arquivos manuais 


for video in lista_videos:
    limiar1_hist = '50000'
    limiar2_hist = '100000'
    limiar3_bic = '5.0'
    limiar4_bic = '1.0'

    nome_video = video.split(".mp4")[0] # Pegando só o nome sem o formato
    diretorio_chaves1_hist = f"cortes_chaves/{nome_video}_{limiar1_hist}_hist.txt"
    diretorio_chaves2_hist = f"cortes_chaves/{nome_video}_{limiar2_hist}_hist.txt"

    diretorio_chaves1_bic = f"cortes_chaves/{nome_video}_{limiar1_hist}_bic.txt"
    diretorio_chaves2_bic = f"cortes_chaves/{nome_video}_{limiar2_hist}_bic.txt"

    diretorio_id1_hist = f"cortes_identificados/{nome_video}_{limiar1_hist}_hist.txt"
    diretorio_id2_hist = f"cortes_identificados/{nome_video}_{limiar2_hist}_hist.txt"

    diretorio_id1_bic = f"cortes_identificados/{nome_video}_{limiar3_bic}_bic.txt"
    diretorio_id2_bic = f"cortes_identificados/{nome_video}_{limiar4_bic}_bic.txt"


    diretorio_manual = f"cortes_manuais/{nome_video}_manual.txt"
    diretorio_video = f"videos/{video}"
   

    #Limiar1 (HISTOGRAMA)
    subprocess.run(
        ['python3', 'detector_corte_histograma.py', diretorio_video, limiar1_hist],
        capture_output=False,  # Captura a saída
        text=True  # Para garantir que a saída seja tratada como texto
    )

    subprocess.run(
        ['python3', 'estatisticas_quadros.py', diretorio_manual, diretorio_id1_hist],
        capture_output=False,  # Captura a saída
        text=True  # Para garantir que a saída seja tratada como texto
    )

    #Limiar1 (BIC)
    subprocess.run(
        ['python3', 'detector_corte_BIC.py', diretorio_video, limiar3_bic],
        capture_output=False,  # Captura a saída
        text=True  # Para garantir que a saída seja tratada como texto
    )

    subprocess.run(
        ['python3', 'estatisticas_quadros.py', diretorio_manual, diretorio_id1_bic],
        capture_output=False,  # Captura a saída
        text=True  # Para garantir que a saída seja tratada como texto
    )

    #Limiar2 (HISTOGRAMA)
    subprocess.run(
        ['python3', 'detector_corte_histograma.py', diretorio_video, limiar2_hist],
        capture_output=False,  # Captura a saída
        text=True  # Para garantir que a saída seja tratada como texto
    )

    subprocess.run(
        ['python3', 'estatisticas_quadros.py', diretorio_manual, diretorio_id2_hist],
        capture_output=False,  # Captura a saída
        text=True  # Para garantir que a saída seja tratada como texto
    )

    # #Limiar2 (BIC)
    subprocess.run(
        ['python3', 'detector_corte_BIC.py', diretorio_video, limiar4_bic],
        capture_output=False,  # Captura a saída
        text=True  # Para garantir que a saída seja tratada como texto
    )

    subprocess.run(
        ['python3', 'estatisticas_quadros.py', diretorio_manual, diretorio_id2_bic],
        capture_output=False,  # Captura a saída
        text=True  # Para garantir que a saída seja tratada como texto
    )

fim_tempo = time.time() # fim do tempo

print(f"Tempo de execução: {(fim_tempo - inicio_tempo)/60:.2f} minutos ({(fim_tempo - inicio_tempo):.2f} segundos)")