# Imports
from fonctions import *
import random as r
degre_minmax = 3

def main():
	global degre_minmax
	N = 4
	A = 3
	P = []
	InitPosition(N, P)
	(P, idjoueur) = PierreFeuilleCiseaux(P, N)
	AffichePosition(N, P)
	end = PlusDeCasesLibres(N,P) 
	while end != 0:
		if idjoueur == 1:
			P = SaisirCoupJoueur(N,P)
			AffichePosition(N,P)
			(M, Mt, score, infos_joueur, infos_ordi) = EvalPosition(N, P, A)
			if infos_joueur[0][0] == A:
				print("Vous avez gagne")
				break
			end = PlusDeCasesLibres(N,P)
			print()
			print("################################")
			print()
			idjoueur = -1
			

		else:
			(M, Mt, (score, coord_meilleur_coup), infos_joueur, infos_ordi) = MinMax(N,P,A, idjoueur, degre_minmax)
			max_value_joueur = infos_joueur[0]
			coord_max_joueur = infos_joueur[1]
			directions_joueur = infos_joueur[2]
			type_lignes_joueur = infos_joueur[3]
			max_value_ordi = infos_ordi[0]
			coord_max_ordi = infos_ordi[1]
			directions_ordi = infos_ordi[2]
			type_lignes_ordi = infos_ordi[3]
			
			(x, y) = coord_meilleur_coup
			P[x][y] = idjoueur
			AffichePosition(N,P)
			idjoueur = 1
			(M, Mt, score, infos_joueur, infos_ordi) = MinMax(N,P,A, idjoueur, degre_minmax)
			if infos_ordi[0][0] == A:
				print("L'ordinateur a gagne")
				break
			end = PlusDeCasesLibres(N,P)
			print()
			print("################################")
			print()
	print("Jeu fini. Merci pour votre participation !")


main()
