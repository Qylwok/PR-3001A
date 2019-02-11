# Imports
from fonctions import *
import random as r

def main():
	N = 4
	A = 3
	P = []
	# Qui commence ? ==> Pierre Feuille Ciseaux avec l'ordinateur ! :D à implémenter
	InitPosition(N, P)
	(P, idjoueur) = PierreFeuilleCiseaux(P, N)
	AffichePosition(N, P)
	end = PlusDeCasesLibres(N,P) 
	while end != 0:
		if idjoueur == 1:
			P = SaisirCoupJoueur(N,P)
			AffichePosition(N,P)
			end = PlusDeCasesLibres(N,P)
			print()
			print("################################")
			print()
			idjoueur = -1
			
		#print(max_value_joueur)
		# print(coord_max_joueur)
		# print(directions_joueur)
		#print(max_value_ordi)
		# print(coord_max_ordi)
		# print(directions_ordi)
		else:
			(score, infos_joueur, infos_ordi) = EvalPosition(N,P,A)
			max_value_joueur = infos_joueur[0]
			coord_max_joueur = infos_joueur[1]
			directions_joueur = infos_joueur[2]
			max_value_ordi = infos_ordi[0]
			coord_max_ordi = infos_ordi[1]
			directions_ordi = infos_ordi[2]
			#print(max_value_joueur)
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
			# print(max_value)
			#print(coord_max)
			# print(directions)
			
			if max_value == 1:
				
				for coord in coord_max:
					(P, place) = Placer1(P, N, A, max_value, coord)
					if place == 1:
						break
				if place == 0:
					PlacerAleat(P, N)
			else:
				for i in range(len(coord_max)):
					coord = coord_max[i]
					direction = directions[i]
					print(coord)
					print(direction)
					place = 0
					if direction == 0:
						if coord in CoordDiagGD(P, N, A):
							(P, place) = PlacerDiagGD(P, N, max_value, coord)
					elif direction == 1:
						(P, place) = PlacerVert(P, N, max_value, coord)
					elif direction == 2:
						if coord in CoordDiagDG(P, N, A):
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
			idjoueur = 1
	print("Jeu fini. Merci pour votre participation !")


main()
