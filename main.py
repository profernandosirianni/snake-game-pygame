import asyncio
import pygame
import random

# Inicializa o Pygame
pygame.init()
pygame.font.init()

# Configurações da tela e grade
LARGURA, ALTURA = 600, 400
TAMANHO_BLOCO = 10 
FPS = 12

# Cores (RGB)
VERDE_ESCURO = (34, 139, 34)
VERMELHO = (220, 20, 60)
BRANCO = (255, 255, 255)
AMARELO = (255, 215, 0)
AZUL_CLARO = (135, 206, 235)
AZUL_ESCURO = (100, 149, 237)

# Configuração da janela e fonte
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Snake Game - Versão Final")
relogio = pygame.time.Clock()
fonte = pygame.font.SysFont("arial", 18, bold=True)
fonte_grande = pygame.font.SysFont("arial", 28, bold=True)

def gerar_comida():
    x = random.randint(0, (LARGURA - TAMANHO_BLOCO) // TAMANHO_BLOCO) * TAMANHO_BLOCO
    y = random.randint(0, (ALTURA - TAMANHO_BLOCO) // TAMANHO_BLOCO) * TAMANHO_BLOCO
    return x, y

def desenhar_tabuleiro():
    colunas = LARGURA // TAMANHO_BLOCO
    linhas = ALTURA // TAMANHO_BLOCO
    for linha in range(linhas):
        for coluna in range(colunas):
            cor = AZUL_CLARO if (linha + coluna) % 2 == 0 else AZUL_ESCURO
            pygame.draw.rect(
                tela, 
                cor, 
                (coluna * TAMANHO_BLOCO, linha * TAMANHO_BLOCO, TAMANHO_BLOCO, TAMANHO_BLOCO)
            )

async def main():
    recorde = 0
    
    while True:  # Loop principal do jogo/menu
        # Estado do Jogo: 'MENU', 'JOGANDO', 'GAMEOVER'
        estado = 'MENU'
        
        cobra = [(300, 200), (290, 200), (280, 200)]
        dx, dy = TAMANHO_BLOCO, 0
        comida_x, comida_y = gerar_comida()
        pontuacao = 0
        
        # Variáveis do efeito piscar (estilo Dinossauro do Google)
        piscar_frames = 0
        
        rodando = True
        while rodando:
            # 1. Eventos e Entradas
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    return
                elif evento.type == pygame.KEYDOWN:
                    if estado == 'MENU' and evento.key == pygame.K_SPACE:
                        estado = 'JOGANDO'
                    elif estado == 'GAMEOVER' and evento.key == pygame.K_SPACE:
                        rodando = False  # Reinicia o loop principal
                    elif estado == 'JOGANDO':
                        # Suporte a Setas Direcionais e WASD
                        if (evento.key in (pygame.K_UP, pygame.K_w)) and dy == 0:
                            dx, dy = 0, -TAMANHO_BLOCO
                        elif (evento.key in (pygame.K_DOWN, pygame.K_s)) and dy == 0:
                            dx, dy = 0, TAMANHO_BLOCO
                        elif (evento.key in (pygame.K_LEFT, pygame.K_a)) and dx == 0:
                            dx, dy = -TAMANHO_BLOCO, 0
                        elif (evento.key in (pygame.K_RIGHT, pygame.K_d)) and dx == 0:
                            dx, dy = TAMANHO_BLOCO, 0

            # 2. Lógica do Jogo
            if estado == 'JOGANDO':
                nova_cabeca = (cobra[0][0] + dx, cobra[0][1] + dy)

                # Colisão
                if (nova_cabeca[0] < 0 or nova_cabeca[0] >= LARGURA or
                    nova_cabeca[1] < 0 or nova_cabeca[1] >= ALTURA or
                    nova_cabeca in cobra):
                    estado = 'GAMEOVER'
                    if pontuacao > recorde:
                        recorde = pontuacao

                if estado == 'JOGANDO':
                    cobra.insert(0, nova_cabeca)

                    # Comer a maçã
                    if nova_cabeca[0] == comida_x and nova_cabeca[1] == comida_y:
                        pontuacao += 1
                        comida_x, comida_y = gerar_comida()
                        # Dispara o efeito de piscar a cada 10 pontos
                        if pontuacao % 10 == 0:
                            piscar_frames = 18  # Pisca durante ~1.5 segundos (18 frames)
                    else:
                        cobra.pop()

            # 3. Renderização
            desenhar_tabuleiro()

            if estado == 'MENU':
                texto_menu = fonte_grande.render("Pressione ESPAÇO para Jogar", True, BRANCO)
                tela.blit(texto_menu, (LARGURA // 2 - texto_menu.get_width() // 2, ALTURA // 2 - 20))
                
            elif estado in ('JOGANDO', 'GAMEOVER'):
                # Desenha a cobra com bordas arredondadas (border_radius)
                for segmento in cobra:
                    pygame.draw.rect(
                        tela, VERDE_ESCURO, 
                        (segmento[0], segmento[1], TAMANHO_BLOCO, TAMANHO_BLOCO),
                        border_radius=3
                    )

                # Desenha a maçã arredondada
                pygame.draw.rect(
                    tela, VERMELHO, 
                    (comida_x, comida_y, TAMANHO_BLOCO, TAMANHO_BLOCO),
                    border_radius=4
                )

                # Placar com efeito de piscar a cada 10 pontos
                exibir_placar = True
                cor_placar = BRANCO
                
                if piscar_frames > 0:
                    piscar_frames -= 1
                    cor_placar = AMARELO
                    # Alterna a exibição a cada 3 frames para dar o efeito pisca-pisca
                    if (piscar_frames // 3) % 2 == 0:
                        exibir_placar = False

                if exibir_placar:
                    txt_pontos = fonte.render(f"Pontos: {pontuacao}", True, cor_placar)
                    tela.blit(txt_pontos, (10, 10))

                txt_recorde = fonte.render(f"Recorde: {recorde}", True, BRANCO)
                tela.blit(txt_recorde, (LARGURA - txt_recorde.get_width() - 10, 10))

                if estado == 'GAMEOVER':
                    txt_over = fonte_grande.render("GAME OVER", True, VERMELHO)
                    txt_reiniciar = fonte.render("Pressione ESPAÇO para Reiniciar", True, BRANCO)
                    tela.blit(txt_over, (LARGURA // 2 - txt_over.get_width() // 2, ALTURA // 2 - 30))
                    tela.blit(txt_reiniciar, (LARGURA // 2 - txt_reiniciar.get_width() // 2, ALTURA // 2 + 10))

            pygame.display.flip()
            relogio.tick(FPS)
            await asyncio.sleep(0)

asyncio.run(main())
