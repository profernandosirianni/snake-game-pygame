import asyncio
import pygame
import random

# Inicializa o Pygame
pygame.init()

# Configurações da tela e do jogo
LARGURA, ALTURA = 600, 400
TAMANHO_BLOCO = 20
FPS = 10

# Cores (RGB)
PRETO = (0, 0, 0)
VERDE = (0, 255, 0)
VERMELHO = (255, 0, 0)

# Configuração da janela
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Snake Game - Web")
relogio = pygame.time.Clock()

def gerar_comida():
    x = random.randint(0, (LARGURA - TAMANHO_BLOCO) // TAMANHO_BLOCO) * TAMANHO_BLOCO
    y = random.randint(0, (ALTURA - TAMANHO_BLOCO) // TAMANHO_BLOCO) * TAMANHO_BLOCO
    return x, y

# A função principal DEVE ser assíncrona (async) para rodar na Web
async def main():
    cobra = [(300, 200), (280, 200), (260, 200)]
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

        if (nova_cabeca[0] < 0 or nova_cabeca[0] >= LARGURA or
            nova_cabeca[1] < 0 or nova_cabeca[1] >= ALTURA or
            nova_cabeca in cobra):
            rodando = False
            break

        cobra.insert(0, nova_cabeca)

        if nova_cabeca[0] == comida_x and nova_cabeca[1] == comida_y:
            pontuacao += 1
            comida_x, comida_y = gerar_comida()
        else:
            cobra.pop()

        tela.fill(PRETO)

        for segmento in cobra:
            pygame.draw.rect(tela, VERDE, (segmento[0], segmento[1], TAMANHO_BLOCO, TAMANHO_BLOCO))

        pygame.draw.rect(tela, VERMELHO, (comida_x, comida_y, TAMANHO_BLOCO, TAMANHO_BLOCO))

        pygame.display.flip()
        relogio.tick(FPS)
        
        # ESSENCIAL: Permite que o navegador processe o quadro sem travar
        await asyncio.sleep(0)

# Ponto de entrada
asyncio.run(main())
