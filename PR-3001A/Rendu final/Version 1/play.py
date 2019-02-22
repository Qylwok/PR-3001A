# Imports
from fonctions import *
import random as r

def main():
	N = 3
	A = 3
	P = []
	InitPosition(N, P)
	AffichePosition(N, P)
	end = PlusDeCasesLibres(N,P)
	while end != 0:
		P = SaisirCoupJoueur(N,P)
		AffichePosition(N,P)
		(score, infos_joueur, infos_ordi) = EvalPosition(N,P,A)
		max_value_joueur = infos_joueur[0]
		coord_max_joueur = infos_joueur[1]
		directions_joueur = infos_joueur[2]
		max_value_ordi = infos_ordi[0]
		coord_max_ordi = infos_ordi[1]
		directions_ordi = infos_ordi[2]
		if max_value_joueur == A: 
			print("Vous avez gagne")
			break
		if score <= 0:
			max_value = max_value_ordi
			coord_max = coord_max_ordi
			directions = directions_ordi
		else:
			max_value = max_value_joueur
			coord_max = coord_max_joueur
			directions = directions_joueur
		
		if max_value == 1:
			for coord in coord_max:
				(P, place) = Placer1(P, N, max_value, coord)
				if place == 1:
					break
			if place == 0:
				PlacerAleat(P, N)
		else:
			for i in range(len(coord_max)):
				coord = coord_max[i]
				direction = directions[i]
				if direction == 0:
					(P, place) = PlacerDiagGD(P, N, max_value, coord)
				elif direction == 1:
					(P, place) = PlacerVert(P, N, max_value, coord)
				elif direction == 2:
					(P, place) = PlacerDiagDG(P, N, max_value, coord)
				else:
					(P, place) = PlacerHoriz(P, N, max_value, coord)
				if place == 1:
					break
			if place == 0:
				PlacerAleat(P,N)
		AffichePosition(N,P)
		(score, infos_joueur, infos_ordi) = EvalPosition(N,P,A)
		if infos_ordi[0] == A:
			print("L'ordinateur a gagne")
			break
		end = PlusDeCasesLibres(N,P)
		print()
		print("################################")
		print()
	print("Jeu fini. Merci pour votre participation !")


main()
