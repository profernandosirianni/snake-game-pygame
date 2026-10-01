import asyncio
import pygame
import random

# Inicializa o Pygame
pygame.init()

# Configurações da tela
LARGURA, ALTURA = 600, 400

# TAMANHO DO BLOCO: Reduzido para aumentar a resolução da grade (ex: 10 pixels)
# O quadrado da malha, a cobrinha e a maçã usarão essa mesma dimensão.
TAMANHO_BLOCO = 10 
FPS = 12

# Definição de Cores (RGB)
VERDE = (50, 205, 50)
VERMELHO = (220, 20, 60)

# Cores em dois tons de azul para a malha quadriculada
AZUL_CLARO = (135, 206, 235)
AZUL_ESCURO = (100, 149, 237)

# Configuração da janela
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Snake Game - Web (Xadrez Azul)")
relogio = pygame.time.Clock()

def gerar_comida():
    x = random.randint(0, (LARGURA - TAMANHO_BLOCO) // TAMANHO_BLOCO) * TAMANHO_BLOCO
    y = random.randint(0, (ALTURA - TAMANHO_BLOCO) // TAMANHO_BLOCO) * TAMANHO_BLOCO
    return x, y

def desenhar_tabuleiro():
    """Desenha o fundo quadriculado alternando entre azul claro e azul mais escuro."""
    colunas = LARGURA // TAMANHO_BLOCO
    linhas = ALTURA // TAMANHO_BLOCO
    for linha in range(linhas):
        for coluna in range(colunas):
            # Se a soma da linha + coluna for par, usa azul claro; se for ímpar, usa azul escuro
            cor = AZUL_CLARO if (linha + coluna) % 2 == 0 else AZUL_ESCURO
            pygame.draw.rect(
                tela, 
                cor, 
                (coluna * TAMANHO_BLOCO, linha * TAMANHO_BLOCO, TAMANHO_BLOCO, TAMANHO_BLOCO)
            )

async def main():
    # Posição inicial centralizada com o novo tamanho de bloco
    cobra = [(300, 200), (300 - TAMANHO_BLOCO, 200), (300 - (2 * TAMANHO_BLOCO), 200)]
    dx, dy = TAMANHO_BLOCO, 0
    comida_x, comida_y = gerar_comida()
    pontuacao = 0

    rodando = True
    while rodando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_UP and dy == 0:
                    dx, dy = 0, -TAMANHO_BLOCO
                elif evento.key == pygame.K_DOWN and dy == 0:
                    dx, dy = 0, TAMANHO_BLOCO
                elif evento.key == pygame.K_LEFT and dx == 0:
                    dx, dy = -TAMANHO_BLOCO, 0
                elif evento.key == pygame.K_RIGHT and dx == 0:
                    dx, dy = TAMANHO_BLOCO, 0

        nova_cabeca = (cobra[0][0] + dx, cobra[0][1] + dy)

        # Colisão com as paredes ou corpo
        if (nova_cabeca[0] < 0 or nova_cabeca[0] >= LARGURA or
            nova_cabeca[1] < 0 or nova_cabeca[1] >= ALTURA or
            nova_cabeca in cobra):
            rodando = False
            break

        cobra.insert(0, nova_cabeca)

        # Comer a comida
        if nova_cabeca[0] == comida_x and nova_cabeca[1] == comida_y:
            pontuacao += 1
            comida_x, comida_y = gerar_comida()
        else:
            cobra.pop()

        # 1. Desenha o fundo quadriculado xadrez
        desenhar_tabuleiro()

        # 2. Desenha a cobra
        for segmento in cobra:
            pygame.draw.rect(tela, VERDE, (segmento[0], segmento[1], TAMANHO_BLOCO, TAMANHO_BLOCO))

        # 3. Desenha a maçã
        pygame.draw.rect(tela, VERMELHO, (comida_x, comida_y, TAMANHO_BLOCO, TAMANHO_BLOCO))

        pygame.display.flip()
        relogio.tick(FPS)
        
        await asyncio.sleep(0)

asyncio.run(main())
