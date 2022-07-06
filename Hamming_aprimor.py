import random
from traceback import print_list 

palavra = '11010101100001110001011011111110011110001111000011101010110000111000101101111111001111000111100001110101011000011100010110111111100111100011110000111010101100001110001011011111110011110001111000011101010110000111000101101111111001111000111100001110101011000011100010110111111100111100011110000111010101100001110001011011111110011110001111000011101010110000111000101101111111001111000111100001110101011000011100010110111111100111100011110000111010101100001110001011011111110011110001111000011101010110000111000101101111111001111000111100001110101011000011100010110111111100111100011110000111010101100001110001011011111110011110001111000011101010110000111000101101111111001111000111100001110101011000011100010110111111100111100011110000111010101100001110001011011111110011110001111000011101010110000111000101101111111001111000111100001110101011000011100010110111111100111100011110000111010101100001110001011011111110011110001111000011101010110000111000101101111111001111000111100001110101011000011100010110111111100111100011110000111010101100001110001011011111110011110001111000011101010110000111000101101111111001111000111100001110101011000011100010110111111100111100011110000111010101100001110001011011111110011110001111000011101010110000111000101101111111001111000111100001110101011000011100010110111111100111100011110000111010101100001110001011011111110011110001111000011101010110000111000101101111111001111000111100001110101011000011100010110111111100111100011110000111010101100001110001011011111110011110001111000011101010110000111000101101111111001111000111100001110101011000011100010110111111100111100011110000111010101100001110001011011111110011110001111000011101010110000111000101101111111001111000111100001110101011000011100010110111111100111100011110000111010101100001110001011011111110011110001111000011101010110000111000101101111111001111000111100001110101011000011100010110111111100111100011110000111010101100001110001011011111110011110001111000011101010110000111000101101111111001111000111100001'
palavra = "".join(reversed(palavra))

# calcular o número de quadros de hamming necesssários
def calcular_quadros(palavra):
    num_tabelas = len(palavra)//11
    if len(palavra) % 11 > 0:
        num_tabelas += 1
    return num_tabelas

#dividir a palavra em conjuntos de 11 bits
def colocar_quadros(palavra, num_tabelas, bits_tabela):
    tabelas = []
    cont = 0
    for x in range (num_tabelas):
        lista = []
        for y in range(bits_tabela):
            if len(palavra) <= cont:
                lista.append("0")
            else :
                lista.append(palavra[cont])
            cont += 1
        tabelas.append(lista)
    return tabelas

#armazenar os bits com os bits de redundância
def armazenar_bits_paridade (palavra):
    bitsPar = [0,1,2,4,8]
    cont = 0
    res = []
    for x in range (16):
        if x in bitsPar:
            res.append("0")
        else:
            res.append(palavra[cont])
            cont += 1
    return res

#posição dos bits com valor 1
def posicao_bits1 (palavra):
    bits1 = []
    for x in range(len(palavra)):
        if palavra[x] == "1":
            bits1.append(x)
    return bits1

# calcular o valor dos bits de paridade
def calcular_paridade(bits1,palavra):
    temp = 0b0
    for x in bits1:
        temp = x ^ temp
    if temp != 0:
        bi = bin(temp)[2:]
        for x in range(len(bi)):
            if bi[x] == "1":
                par = "1"
                for y in range(len(bi)-x-1):
                    par += "0"
                palavra[int(par,2)] = str(int(palavra[int(par,2)]) ^ 1)
    
    #paridade geral
    bits1 = posicao_bits1(palavra)
    if len(bits1) % 2 != 0:
        palavra[0] = str(int(palavra[0]) ^ 1)

    return palavra

#arrumar erro
def correcao(bits1,palavra):
    temp = 0b0
    for x in bits1:
        temp = x ^ temp
    if temp != 0:
        if palavra[temp] == "0":
            palavra[temp] = "1"
        else:
            palavra[temp] = "0"
    return palavra

def codificar(palavra):
    palavra_final = ""
    num_tabelas = calcular_quadros(palavra)
    tabelas = colocar_quadros(palavra,num_tabelas,11)
    for x in range(len(tabelas)):
        tabelas[x] = armazenar_bits_paridade(tabelas[x])
        bits1 = posicao_bits1(tabelas[x])
        tabelas[x] = calcular_paridade(bits1,tabelas[x])
        for x in tabelas[x]:
            palavra_final += x

    return palavra_final

def remover_paridade(palavra):
    palavra_final = ""
    bitsPar = [0,1,2,4,8]
    cont = 0
    for x in palavra:
        if cont not in bitsPar:
            palavra_final += str(x)
        cont += 1

    return palavra_final

def decodificar(palavra):
    tabelas = colocar_quadros(palavra, len(palavra)//16, 16)
    palavra_final = ""
    for x in range(len(tabelas)):
        bits1 = posicao_bits1(tabelas[x])
        corrigida = correcao(bits1, tabelas[x])
        corrigida = remover_paridade(tabelas[x])
        if x == len(tabelas) - 1:
            temp = 0
            while (True):
                if corrigida[-1] == "1":
                    break
                corrigida = corrigida[:-1]
        palavra_final += corrigida
    palavra_final = "".join(reversed(palavra_final))
    return palavra_final

def ruido(palavra):
    lista = []
    for x in palavra:
        lista.append(x)
    index = random.randint(0,len(palavra)-1)
    lista[index] = str(int(lista[index]) ^ 1)
    palavra = ""
    for x in lista:
        palavra += x
    return palavra

erros = 0
acertos = 0
for x in range(100):
    palavra_codificada = codificar(palavra)
    palavra_ruido = ruido(palavra_codificada)
    decodificada = decodificar(palavra_ruido)
    palavra = "".join(reversed(palavra))
    if decodificada == palavra:
        acertos += 1
    else:
        erros += 1
print(erros)
print(acertos)
