import pygame
import sys
import random
from pygame.locals import *
 
# Initialize Pygame
pygame.init()
 
# Define Colors
BLANC = (255, 255, 255)
NOIR = (0, 0, 0)
COULEUR_BOUTON = (223, 160, 174)
 
# Window Size
largeur, hauteur = 1000, 700
fenetre = pygame.display.set_mode((largeur, hauteur))
pygame.display.set_caption('Menu de sélection de niveau')
 
# Text Display Function
def afficher_texte(texte, taille, couleur, x, y):
    font = pygame.font.SysFont('Arial', taille)
    texte_surface = font.render(texte, True, couleur)
    texte_rect = texte_surface.get_rect()
    texte_rect.center = (x, y)
    fenetre.blit(texte_surface, texte_rect)
 
# Button Creation Function
def creer_bouton(texte, x, y, largeur, hauteur, couleur_texte, action=None):
    souris = pygame.mouse.get_pos()
    clic = pygame.mouse.get_pressed()
    pygame.draw.rect(fenetre, COULEUR_BOUTON, (x, y, largeur, hauteur))
    afficher_texte(texte, 30, couleur_texte, x + largeur // 2, y + hauteur // 2)
    if x < souris[0] < x + largeur and y < souris[1] < y + hauteur:
        if clic[0] == 1 and action is not None:
            return action
    return None
 
# Main Menu Function
def afficher_menu():
    menu = True
    niveau = None
    espace_entre_boutons = 100
    while menu:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        fenetre.fill(BLANC)
        afficher_texte("Sélectionnez un niveau", 40, NOIR, largeur // 2, hauteur // 4)
       
        if creer_bouton("Facile (3x3)", largeur // 2 - 100, hauteur // 2 - 50, 200, 50, NOIR, action="Facile") == "Facile":
            return 3
        if creer_bouton("Moyen (4x4)", largeur // 2 - 100, hauteur // 2 + espace_entre_boutons - 50, 200, 50, NOIR, action="Moyen") == "Moyen":
            return 4
        if creer_bouton("Difficile (5x5)", largeur // 2 - 100, hauteur // 2 + 2 * espace_entre_boutons - 50, 200, 50, NOIR, action="Difficile") == "Difficile":
            return 5
        if creer_bouton("Quitter", largeur // 2 - 100, hauteur // 2 + 3 * espace_entre_boutons - 50, 200, 50, NOIR, action="Quitter") == "Quitter":
            pygame.quit()
            sys.exit()
       
        pygame.display.update()
 
# Puzzle Game Functions
Vitesse = 1000
Vide = None
haut = 'up'
bas = 'down'
gauche = 'left'
droite = 'right'
 
def Melangepuzzle(complexite, taille):
    puzzle_resolu = [[i + j * taille + 1 for i in range(taille)] for j in range(taille)]
    puzzle_resolu[-1][-1] = Vide
    puzzle_melange = [row[:] for row in puzzle_resolu]
    for _ in range(complexite):
        directions = [gauche, droite, haut, bas]
        random.shuffle(directions)
        for direction in directions:
            if mouvementpossible(puzzle_melange, direction):
                fairemouvement(puzzle_melange, direction)
                break
    return puzzle_melange, puzzle_resolu
 
def dessintableau(ORDONNE):
    Surface.fill(COULEUR_BOUTON)
    taille = len(ORDONNE)
    for i, row in enumerate(ORDONNE):
        for j, value in enumerate(row):
            if value is not None:
                pygame.draw.rect(Surface, NOIR, (j * (1000 // taille), i * (700 // taille), 1000 // taille, 700 // taille))
                pygame.draw.rect(Surface, BLANC, (j * (1000 // taille) + 5, i * (700 // taille) + 5, 1000 // taille - 10, 700 // taille - 10))
                font = pygame.font.SysFont('arial', 30)
                text = font.render(str(value), True, NOIR)
                text_rect = text.get_rect(center=(j * (1000 // taille) + (1000 // taille) // 2, i * (700 // taille) + (700 // taille) // 2))
                Surface.blit(text, text_rect)
    pygame.display.update()
 
def placechoisi(ORDONNE, posx, posy):
    taille = len(ORDONNE)
    case_x = posx // (1000 // taille)
    case_y = posy // (700 // taille)
    if 0 <= case_x < taille and 0 <= case_y < taille:
        return case_x, case_y
    else:
        return None, None
 
def reinitialiseAnimation(ORDONNE, mouvements):
    for direction in mouvements:
        Animationmouvement(ORDONNE, direction, 'jouer', 8)
        fairemouvement(ORDONNE, direction)
 
def positioncubevide(ORDONNE):
    for i in range(len(ORDONNE)):
        for j in range(len(ORDONNE[i])):
            if ORDONNE[i][j] == Vide:
                return i, j
 
def mouvementpossible(ORDONNE, direction):
    vide_x, vide_y = positioncubevide(ORDONNE)
    taille = len(ORDONNE)
    if direction == gauche and vide_x > 0:
        return True
    elif direction == droite and vide_x < taille - 1:
        return True
    elif direction == haut and vide_y > 0:
        return True
    elif direction == bas and vide_y < taille - 1:
        return True
    else:
        return False
 
def Animationmouvement(ORDONNE, direction, jouer, valeur):
    for _ in range(valeur):
        dessintableau(ORDONNE)
        pygame.display.update()
        pygame.time.delay(50)
 
def fairemouvement(ORDONNE, direction):
    vide_x, vide_y = positioncubevide(ORDONNE)
    if direction == gauche:
        ORDONNE[vide_x][vide_y], ORDONNE[vide_x - 1][vide_y] = ORDONNE[vide_x - 1][vide_y], ORDONNE[vide_x][vide_y]
    elif direction == droite:
        ORDONNE[vide_x][vide_y], ORDONNE[vide_x + 1][vide_y] = ORDONNE[vide_x + 1][vide_y], ORDONNE[vide_x][vide_y]
    elif direction == haut:
        ORDONNE[vide_x][vide_y], ORDONNE[vide_x][vide_y - 1] = ORDONNE[vide_x][vide_y - 1], ORDONNE[vide_x][vide_y]
    elif direction == bas:
        ORDONNE[vide_x][vide_y], ORDONNE[vide_x][vide_y + 1] = ORDONNE[vide_x][vide_y + 1], ORDONNE[vide_x][vide_y]
 
def objet(nom, couleurtexte, couleurfond, top, left):
    font = pygame.font.SysFont('arial', 20)
    texte = font.render(nom, True, couleurtexte, couleurfond)
    rect = texte.get_rect()
    rect.topleft = (top, left)
    return texte, rect
 
def main():
    global temps, Surface, ecriture, SOLUTION_SURF, SOLUTION_RECT
    pygame.init()
    temps = pygame.time.Clock()
    Surface = pygame.display.set_mode((1000, 700))
    pygame.display.set_caption('PUZZLE TAQUIN')
    ecriture = pygame.font.SysFont('arial', 20)
    SOLUTION_SURF, SOLUTION_RECT = objet('Solution', BLANC, (147, 51, 0), 50, 290)
    niveau = afficher_menu()
    ORDONNE, RESOLU = Melangepuzzle(50, niveau)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    if mouvementpossible(ORDONNE, gauche):
                        fairemouvement(ORDONNE, gauche)
                elif event.key == pygame.K_DOWN:
                    if mouvementpossible(ORDONNE, droite):
                        fairemouvement(ORDONNE, droite)
                elif event.key == pygame.K_LEFT:
                    if mouvementpossible(ORDONNE, haut):
                        fairemouvement(ORDONNE, haut)
                elif event.key == pygame.K_RIGHT:
                    if mouvementpossible(ORDONNE, bas):
                        fairemouvement(ORDONNE, bas)
        Surface.fill(COULEUR_BOUTON)
        dessintableau(ORDONNE)
        pygame.display.update()
        temps.tick(30)
 
if __name__ == "__main__":
    main()