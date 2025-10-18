# Alunos: Nycksandro Lima dos Santos e Rômulo Fernandes Torres
import cv2
import sys 

def calcula_histograma(frame):
    altura, largura, n_bandas = frame.shape # Pegando altura e largura da imagem
    histograma = [0 for i in range(0,256*3)] # Criando um "vetor" de 768 elementos pra guardar os 256 valores de R G e B
    
    for i in range(0, altura): # Depois a linha
        for j in range(0, largura): # Depois a coluna
            for banda in range(0,n_bandas): # Primeiro percorro a banda
                indice = int(frame[i][j][banda]) + banda*256 # Calculo pra achar a posição do pixel correto no histograma
                histograma[indice]+=1 # Incremento na posição certo

    return histograma
        
def histograma_local(frame): 
    altura, largura, n_bandas = frame.shape
    proporcao_centro = 0.6 # 60% para o centro
    proporcao_borda = 0.1 # e 10 % para cada canto

    altura_centro = int(altura * proporcao_centro)
    largura_centro = int(largura * proporcao_centro)

    altura_borda = int(altura * proporcao_borda)
    largura_borda = int(largura * proporcao_borda)

    topo = altura_borda  # Início da altura do centro
    esquerda = largura_borda  # Início da largura do centro

    centro = frame[topo:topo+altura_centro, esquerda:esquerda+largura_centro] #Pegando o centro

    # Pegando as bordas

    borda_superior_esquerda = frame[0:altura_borda, 0:largura_borda]
    
    borda_superior_direita = frame[0:altura_borda, largura-largura_borda:largura]
    
    borda_inferior_esquerda = frame[altura-altura_borda:altura, 0:largura_borda]
    
    borda_inferior_direita = frame[altura-altura_borda:altura, largura-largura_borda:largura]

    bordas = [centro, borda_superior_esquerda, borda_superior_direita, borda_inferior_esquerda, borda_inferior_direita]
    histogramas = []
    for borda in bordas: # Calculo o histograma de cada particao
        histogramas.append(calcula_histograma(borda))
    
    return histogramas # Retorno a lista de histogramas (de cada bloco)

def verifica_tudo_preto(frame, limiar): # Funçãozinha pra saber se o frame é todo preto
    altura, largura, n_bandas = frame.shape # Pegando a altura e largura da imagem
    cont = 0
    
    for i in range(0, altura):
        for j in range(0, largura):
            if(frame[i][j][0] <= limiar and frame[i][j][1] <= limiar and frame[i][j][2] <= limiar):
                cont+=1

    if(cont/(altura*largura) > 0.9): # Se 90% dos pixels for menor do q esse limiar, então ta tudo escuro
        return True
    
    return False

def verifica_tudo_branco(frame, limiar): # Mesma coisa da função de ver se tá tudo preto, so que branco
    altura, largura, n_bandas = frame.shape # Pegando a altura e largura da imagem
    cont = 0
    
    for i in range(0, altura):
        for j in range(0, largura):
            if(frame[i][j][0] >= limiar and frame[i][j][1] >= limiar and frame[i][j][2] >= limiar):
                cont+=1

    if(cont/(altura*largura) > 0.9): # Se 90% dos pixels for menor do q esse limiar, então ta tudo branco
        return True
    
    return False

def distancia_euclidiana(hist1, hist2): # Função pra calcular a distancia euclidiana de dois histogramas de mesmo tamanho
    soma = 0
    for i in range(0, len(hist1)):
        soma += (hist1[i] - hist2[i])**2

    return soma**0.5 

def maior_distancia_euclidiana(histogramas1, histogramas2): # Função pra eu descobrir qual é a maxima das distancia eucldiana entre as 5 partições
    distancias = [] # Crio uma lista pra guardar cada distancia
    for i in range(0, len(histogramas1)):
        distancias.append(distancia_euclidiana(histogramas1[i], histogramas2[i])) # Coloco na lista a distancia euclidiana de cada partição

    return max(distancias) # Retornando o maior


nome_do_video = sys.argv[1] # Caminho do vídeo
limiar = int(sys.argv[2]) # Ler o Limiar

print(f"Vídeo: {nome_do_video} (Histograma, {limiar})\n")
video = cv2.VideoCapture(nome_do_video) # Leio o vídeo

if not video.isOpened(): # Vejo se não deu nenhum erro
    print("Erro ao abrir o vídeo.")
    exit()

fps = round(video.get(cv2.CAP_PROP_FPS)) # Pego a quantidade de fps do video
total_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT)) # Pego o número total de frames
frame_atual = 0 # Começo no frame 0
quadros_chaves = [] # Lista pra eu guardar os meus quadros chaves
quadros_identificados = [] # Lista pra eu guardar os meus quadros identificados

#Vou ler o primeiro frame valido (nem preto, nem branco)
video.set(cv2.CAP_PROP_POS_FRAMES, frame_atual) # Seto as configurações pra pegar o frame1
ret, frame1 = video.read() # Pego o frame atual
while(frame_atual + fps <= total_frames and (verifica_tudo_preto(frame1, 10) == True or verifica_tudo_branco(frame1, 240) == True)):
    #print(f"O frame: {frame_atual} é branco ou preto" )
    video.set(cv2.CAP_PROP_POS_FRAMES, frame_atual) # Seto as configurações pra pegar o frame
    ret, frame1 = video.read() # Pego o frame atual
    frame_atual+=fps # Pulo pro proximo take
    
frame_info1 = f"{frame_atual}/{total_frames-1}" # Pegando as informações do frame1
pode_frame1 = True # Seto que o frame1 pode ter o histograma calculado

while(frame_atual < total_frames): # Enquanto n li todos os quadros
    pode_frame2 = False # Variavel pra eu controlar se pode ou não calcular o histograma para o frame2

    frame_atual+=fps # Vou pro proximo take

    #Lendo o segundo take
    video.set(cv2.CAP_PROP_POS_FRAMES, frame_atual) # Seto as configurações pra pegar o frame2
    ret, frame2 = video.read() # Pego o frame atual

    #Vou lendo até achar um frame que não seja nem todo branco, nem todo preto, e que esteja antes de acabar o vídeo
    while(frame_atual < total_frames and (frame2 is not None) and (verifica_tudo_preto(frame2, 10) == True or verifica_tudo_branco(frame2, 240) == True)): # Vou procurando o frame até vir um que não é nem todo preto nem todo branco
        video.set(cv2.CAP_PROP_POS_FRAMES, frame_atual) # Seto as configurações pra pegar o frame
        ret, frame2 = video.read() # Pego o frame atual
        frame_atual+=fps # Pulo pro proximo take
    
    if(frame_atual < total_frames and frame2 is not None): # Se tiver dentro dos frames totais
        pode_frame2 = True # Então posso calcular o histograma
    frame_info2 = f"{frame_atual}/{total_frames-1}" # Pegando as informações do frame

    if(pode_frame2 == False): # Se o frame2 for false, é pq vai ta errado. O primeiro sempre vai ser verdadeiro na logica q eu montei
        break

     # Se chegou aqui, eu vou ter 2 frames que não são nem branco, nem preto, e ainda n acabou o vídeo, ai sim vou poder comparar seus histogramas
    histogramas_frame1 = histograma_local(frame1)
    histogramas_frame2 = histograma_local(frame2)    
    
    #A gente decidiu escolher a maxima dentre as distancia pra comparar com a limiar, pois assim a gente vai ter um valor melhor entre as partições para se comparar com o limiar
    resultado = maior_distancia_euclidiana(histogramas_frame1, histogramas_frame2) # Calculo o maximo das distancia euclidiana
    print(f"{resultado}, {frame_atual}/{total_frames}")
    
    if(resultado > limiar): # Se for uma troca de cena, eu coloco aqui
        # A heuristica que escolhemos para achar o quadro chave foi calcular o quadro médio entre uma cena e outra
        q_atual1 = int(frame_info1.split("/")[0])
        q_atual2 = int(frame_info2.split("/")[0])
        
        #Adiciono cada quadro em suas listas respectivas
        quadros_chaves.append((q_atual1+q_atual2)//2)
        quadros_identificados.append(q_atual1)

        # Como trocou de cena, agora eu verifico qual é a proxima troca de cena referente ao novo frame
        frame1 = frame2 # Agora o frame antigo (frame1) vira o novo (frame2)
        frame_info1 = frame_info2 # Atualizo as informações também


quadros_identificados.append((quadros_chaves[-1]*2)-quadros_identificados[-1]) # Coloco o ultimo quadro que não é pegado pelo loop

nome_video2 = nome_do_video.split('videos/')[1].split(".mp4")[0] # Pegando só o nome

diretorio_chaves = f"cortes_chaves/{nome_video2}_cortes_chaves_{limiar}_hist.txt"
diretorio_identificados = f"cortes_identificados/{nome_video2}_{limiar}_hist.txt"

with open(diretorio_identificados, 'w') as arquivo: # Vou escrever um arquivo com os quadros identificados e chaves    
    arquivo.write(f"Titulo do video: {nome_do_video}\nLimiar: {limiar}\nTotal de Frames: {total_frames}\nSalto: {fps}\nQuadros:\n\n")
    for i in quadros_identificados:
        arquivo.write(str(i) + "\n")

with open(diretorio_chaves, 'w') as arquivo:
    arquivo.write(f"Titulo do video: {nome_do_video}\nLimiar: {limiar}\nTotal de Frames: {total_frames}\nSalto: {fps}\nQuadros:\n\n")
    for i in quadros_chaves:
        arquivo.write(str(i) + "\n")


