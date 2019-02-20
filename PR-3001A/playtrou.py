# Imports
from fonctions_trou import *
import random as r

def main():
	N = 4
	A = 4
	P = []
	# Qui commence ? ==> Pierre Feuille Ciseaux avec l'ordinateur ! :D à implémenter
	InitPosition(N, P)
	(P, idjoueur) = PierreFeuilleCiseaux(P, N)
	AffichePosition(N, P)
	# print("CoorddiagGD = ", coord_diag_GD)
	# print("CoorddiagDG = ", coord_diag_DG)
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
			(M, Mt, score, infos_joueur, infos_ordi) = EvalPosition(N,P,A)
			max_value_joueur = infos_joueur[0]
			coord_max_joueur = infos_joueur[1]
			directions_joueur = infos_joueur[2]
			type_lignes_joueur = infos_joueur[3]
			max_value_ordi = infos_ordi[0]
			coord_max_ordi = infos_ordi[1]
			directions_ordi = infos_ordi[2]
			type_lignes_ordi = infos_ordi[3]
			#print(max_value_joueur)
			if max_value_joueur[0] == A: 
				print("Vous avez gagne")
				break
			if score <= 0:
				max_values = max_value_ordi + max_value_joueur
				coord_max = coord_max_ordi + coord_max_joueur
				directions = directions_ordi + directions_joueur
				type_lignes = type_lignes_ordi + type_lignes_joueur
			else:
				max_values = max_value_joueur + max_value_ordi
				coord_max = coord_max_joueur + coord_max_ordi
				directions = directions_joueur + directions_ordi
				type_lignes = type_lignes_joueur + type_lignes_ordi
			# print(max_value)
			#print(coord_max)
			# print(directions)
			
			if max_values[0] == 1:
				
				for i in range(len(coord_max)):
					coord = coord_max[i]
					max_value = int(max_values[i])
					(P, place) = Placer1(P, N, A, max_value, coord)
					if place == 1:
						break
				if place == 0:
					PlacerAleat(P, N)
			else:
				for i in range(len(coord_max)):
					coord = coord_max[i]
					direction = directions[i]
					max_value = int(max_values[i]) 
					ligne = type_lignes[i]
					place = 0
					if direction == 0:
						if ligne == "n":
							(P, place) = PlacerDiagGD(P, N, max_value, coord)
						else:
							(P, place) = PlacerDiagGDTrou(P, N, A, coord)
					elif direction == 1:
						if ligne == "n":
							(P, place) = PlacerVert(P, N, max_value, coord)
						else:
							(P, place) = PlacerVertTrou(P, N, A, coord)
					elif direction == 2:
						if ligne == "n":
							(P, place) = PlacerDiagDG(P, N, max_value, coord)
						else:
							(P, place) = PlacerDiagDGTrou(P, N, A, coord)
					else:
						if ligne == "n":
							(P, place) = PlacerHoriz(P, N, max_value, coord)
						else:
							(P, place) = PlacerHorizTrou(P, N, A, coord)
					if place == 1:
						break
				if place == 0:
					print("placement aléatoire")
					PlacerAleat(P,N)
			AffichePosition(N,P)
			(M, Mt, score, infos_joueur, infos_ordi) = EvalPosition(N,P,A)
			if infos_ordi[0][0] == A:
				print("L'ordinateur a gagne")
				break
			end = PlusDeCasesLibres(N,P)
			print()
			print("################################")
			print()
			idjoueur = 1
	print("Jeu fini. Merci pour votre participation !")


main()
