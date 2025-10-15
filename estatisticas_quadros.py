import sys

def calcula_estatisticas(arquivo, manual, qid, salto, total_frames): # Função que criamos automatiza o calculo das estatisticas do relatório 
    nao_identificados = []
    corretamente_identificados = []

    quadros_total_manual = len(manual)
    quadros_total_algoritmo = len(qid)
  
    for elem in manual: # Primeiro tiro todos os exatos pra poder ter certeza que não vai pegar o frame errado (primeiro filtro)
        if(elem in qid):# Verifico se tem exatamente o valor do frame especifico
            #Se tem, eu simplesmente coloco no corretamente identificados e tiro da lista dos q_id
            indice = qid.index(elem) # Pego o indice de onde ele ta
            corretamente_identificados.append(elem) # Coloco na lista de corretamente identificados
            qid.pop(indice) # Tirando ele do qid
            
        
    # Agora repito todo o processo com o q sobrou
    for elem in manual:
        if(elem in corretamente_identificados): # Verifico se já pegou pelo primeiro filtro
           pass

        #Se não tiver exatamente o valor, eu posso verificar se ele está entre o intervalo de -"salto" ou -"salto"
        else:
            naoIdentificado = True
            for frameValor in qid: # Verifico para todos os valores de qid
                if(elem == frameValor + salto or elem == frameValor - salto): # Ta dentro do intervalo
                    corretamente_identificados.append(elem) # Coloco na lista de corretamente indentificados
                    indice = qid.index(frameValor) # Pego o indice de onde ele ta
                    qid.pop(indice) # Tiro ele da lista
                    naoIdentificado = False # Marco que ele é identificado
                    break # Saio do loop
            if(naoIdentificado == True): # Se ele pertencer aos frames não indentificados, eu coloco na lista de não indentificados
                nao_identificados.append(elem) # No caso, é do manual 

    # Chegando aqui, o que tiver sobrado em qid, é somente os elementos que foram erroneamente detectados como corte

    detectados_incorretamente = qid

    vp = len(corretamente_identificados) # Verdadeiro positivo
    fp = len(detectados_incorretamente) # Falso positivo
    fn = len(nao_identificados) # Falso negativo
    vn = total_frames - (vp + fp + fn) # Verdadeiro negativo
    acuracia = ((vp + vn)/(vn + vp + fp + fn))*100

    arquivo.write(f"Acuracia: (({vp} + {vn})/({vn} + {vp} + {fp} + {fn})) = {vp + vn}/{vp+vn+fp+fn} = {acuracia:.2f}%")
    arquivo.write(f"Quadros Totais (Manual): {quadros_total_manual}\n")
    arquivo.write(f"Quadros detectados no total: {quadros_total_algoritmo}\n")
    arquivo.write(f"Quadros corretamente detectados (Verdadeiro Positivo): {vp}\n")
    arquivo.write(f"Quadros detectados incorretamente (Falso Positivo): {fp}\n")
    arquivo.write(f"Quadros nao detectados (Falso Negativo): {fn}\n")
    arquivo.write(f"Quadros nao-cortes corretamente identificados (Verdadeiro Negativo): {total_frames} - {vp} - {fp} - {fn} =  {vn}\n")
    arquivo.write(f"Total de Frames: {total_frames}\n")

    #Em baixo eu printo os quadros identificados corretamente, não identificados e incorretamente identificados 
    #arquivo.write(f"Corretamente identificados: {corretamente_identificados}\n")
    #arquivo.write(f"Nao identificados: {nao_identificados}\n")
    #arquivo.write(f"Detectados incorretamente: {detectados_incorretamente}\n\n")

    arquivo.write(f"\n\nQUADROS NAO IDENTIFICADOS\n\n")
    for elem in nao_identificados:
        arquivo.write(f"{elem}\n")

    arquivo.write(f"\nQUADROS CORRETAMENTE IDENTIFICADOS\n\n")
    for elem in corretamente_identificados:
        arquivo.write(f"{elem}\n")

    arquivo.write(f"\n\nQUADROS INCORRETAMENTE IDENTIFICADOS\n\n")
    for elem in detectados_incorretamente:
        arquivo.write(f"{elem}\n")

if(len(sys.argv) != 3):
    print("A sáida deve ser assim: arquivo.py arquivo_manual.txt arquivo_identificadosID.txt")
    exit(1)

manual = []
quadros_identificados = []
caminho_arquivo_manual = sys.argv[1]
caminho_arquivo_quadrosId = sys.argv[2]

with open(caminho_arquivo_quadrosId, 'r') as arquivo: # Vou ler todos os quadros identificados e colocar em uma lista
    linhas = arquivo.readlines()
    limiar = linhas[1].split(':')[1].split()[0] # Pego o limiar e também tiro o \n
    salto = int(linhas[3].split(":")[1]) # Lendo o salto
    total_frames = int(linhas[2].split(":")[1]) # Lendo o total de frames
    for linha in linhas[5:]: # Já começa a ler a partir dos quadros (pulando titulo, limiar, total de frames, salto e quadro)
        quadros_identificados.append(int(linha.strip()))

with open(caminho_arquivo_manual, 'r') as arquivo: # Agora vou ler o arquivo que tem os frames coletados manualmente e colocar na lista
    linhas = arquivo.readlines()
    for linha in linhas:
        manual.append(int(linha.strip()))

print(caminho_arquivo_manual)
nome_resultado = caminho_arquivo_manual.split("_manual.txt")[0] # Tiro a parte do manual
nome_resultado = nome_resultado.split("cortes_manuais/")[1] # Tiro a parte do caminho que vem antes
nome_resultado = f"estatisticas/{nome_resultado}_estatistica_{limiar}.txt"

with open(nome_resultado, 'w') as arquivo: # Agora vou criar um arquivo com todo o resultado e calculos da estatistica
    calcula_estatisticas(arquivo, manual, quadros_identificados, salto, total_frames)
