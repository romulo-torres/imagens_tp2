import cv2
import sys

nome_do_video = sys.argv[1]
registro = sys.argv[2]

video = cv2.VideoCapture(nome_do_video)
if not video.isOpened():
    print("Erro ao abrir o vídeo.")
    exit()

numero_do_frame = 0  
frames_registrados = []  
fps = round(video.get(cv2.CAP_PROP_FPS))
print(f"fps do vídeo {fps}")    
salto = fps # // 2  

# Obter o número total de frames para limitar a navegação
total_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))

while True:
    video.set(cv2.CAP_PROP_POS_FRAMES, numero_do_frame)
    ret, frame = video.read()

    if not ret:
        break

    # Adicionar informação do frame atual na janela
    frame_info = f"Frame: {numero_do_frame}/{total_frames-1} | Registrados: {len(frames_registrados)}"
    cv2.putText(frame, frame_info, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 255), 2)
    
    cv2.imshow("Quadro", frame)

    key = cv2.waitKey(0) & 0xFF
    
    if key == 81 or key == 83:  # Seta esquerda (81) ou direita (83) no Linux/Mac
        # Verificar se estamos no OpenCV com codificação diferente
        if key == 81:  # Seta esquerda - voltar
            numero_do_frame = max(0, numero_do_frame - salto)
        elif key == 83:  # Seta direita - avançar
            numero_do_frame = min(total_frames - 1, numero_do_frame + salto)
    
    elif key == ord('a') or key == ord('d'):  # Alternativa com teclas A/D
        if key == ord('a'):  # Tecla A - voltar
            numero_do_frame = max(0, numero_do_frame - salto)
        elif key == ord('d'):  # Tecla D - avançar
            numero_do_frame = min(total_frames - 1, numero_do_frame + salto)
    
    elif key == ord('s'):  # Registrar frame atual
        if numero_do_frame not in frames_registrados:
            frames_registrados.append(numero_do_frame)
            print(f"Frame {numero_do_frame} registrado!")
        else:
            print(f"Frame {numero_do_frame} já estava registrado!")
    
    elif key == ord('q'):  # Sair do programa
        print("Encerrando programa...")
        break
    
    elif key == ord('r'):  # Remover frame dos registrados (opcional)
        if numero_do_frame in frames_registrados:
            frames_registrados.remove(numero_do_frame)
            print(f"Frame {numero_do_frame} removido dos registros!")
    
    # Atualizar display com nova posição
    continue

with open(registro, "w") as arquivo:
    conteudo = "\n".join(map(str, frames_registrados))
    arquivo.write(conteudo)

print(f"Frames registrados salvos em {registro}: {frames_registrados}")
video.release()
cv2.destroyAllWindows()