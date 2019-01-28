# Imports
from fonctions import *
import random as r

def main():
	N = 3
	A = 3
	P = []
	# Qui commence ? ==> Pierre Feuille Ciseaux avec l'ordinateur ! :D à implémenter
	InitPosition(N, P)
	AffichePosition(N, P)
	end = PlusDeCasesLibres(N,P)
	while end != 0:
		P = SaisirCoupJoueur(N,P)
		AffichePosition(N,P)
		(score, max_value, coord_max, directions) = EvalPosition(N,P)
		if score <= 0:
			if len(coord_max) == 1:		# Un seul qui a l'avantage : lui
				if directions[0] = 0: 	# Alignés en haut à gauche
					i = coord_max[0][0]
					j = coord_max[0][1]
					try:
						if P[i+1][j+1] == 0:
							P[i+1][j+1] = -1
						else:
							k = 1/0 # Force une exception ==> go dans le except
					except:
						try:
							if P[i-max_value][j-max_value] == 0:
								P[i-max_value][j-max_value] = -1
							else:
								k = 1/0
						except:
							coord_vides = Coord_cases_vides(N,P)
							coord_alea_vide = coord_vides[r.randint(0,len(coord_vides))]
							x = coord_alea_vide[0]
							y = coord_alea_vide[1]
							P[x][y] = -1

			else: # Plusieurs directions
				coord_max_j = []
				coord_max_o = []
				for coord in coord_max:
					x = coord[0]
					y = coord[1]
					if P[x][y] == -1:
						coord_max_o.append([x, y])
					else:
						coord_max_j.append([x, y])
				for coord in coord_max_o:
					x = coord[0]
					y = coord[1]
					if x+1<N and y+1<N:
						if P[x+1][y]

		end = PlusDeCasesLibres(N,P)
		print()
		print("################################")
		print()
	print("Jeu fini. Merci pour votre participation !")


main()