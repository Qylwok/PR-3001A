import numpy as np
import random as r

def EvalPosition(N, P, A):
	'''
	ENTREES : 
		N : Entier
		P : Tableau NxN d'entiers
		A : Nombre de pions alignés nécessaires pour gagner

	SORTIE :
		- score : Un entier entre -1000 et 1000 évaluant la position
				-1000 : Le joueur 2 a A-1 pions alignés
				1000  : Le joueur 1 a A-1 pions alignés
			On va faire une echelle avec des pas de 1000/A
		- max_value : le nombre de pions alignés maximum
		- coord_max : en quelle position on a cet alignement
		- directions : dans quelle direction on suit la ligne : 
			0 : vers en haut à gauche
			1 : vers en haut
			2 : vers en haut à droite
			3 : vers la gauche

	FORME DE P :
		+1 si pion du joueur 1
		0  si aucun pion


	Joueur 		= 	joueur 1 	(+1)
	Ordinateur 	= 	joueur 2	(-1)
	'''

	############### CONSTRUCTION DE LA MATRICE M ###############

	M = np.zeros((N, N, 4))
	# M[i][j][0 1 2 ou 3] avec :
	# 0 : direction en haut à gauche
	# 1 : direction en haut
	# 2 : direction en haut à droite
	# 3 : direction à gauche

	M[0][0] = [0, 0, 0, 0]
	pas = 1000/A
	max_value_joueur = [0]
	max_value_ordi = [0]
	coord_max_joueur = [[0, 0]]
	coord_max_ordi = [[0, 0]]
	for i in range(N):
		for j in range(N):
			if P[i][j] != 0:
				if i-1 >= 0:
					if j-1 >=0:
						if P[i][j] == P[i-1][j-1]:
							valeur = M[i-1][j-1][0] + 1
							if P[i][j] == 1:	
								if valeur == max_value_joueur[0]:
									coord_max_joueur.append([i, j])
									max_value_joueur.append(valeur)
								elif valeur > max_value_joueur[0]:
									max_value_joueur = [valeur]
									coord_max_joueur = [[i, j]]
							elif P[i][j] == -1:
								if valeur == max_value_ordi[0]:
									max_value_ordi.append(valeur)
									coord_max_ordi.append([i, j])
								elif valeur > max_value_ordi[0]:
									max_value_ordi = [valeur]
									coord_max_ordi = [[i, j]]
							M[i][j][0] = valeur
					if P[i][j] == P[i-1][j]:
						valeur = M[i-1][j][1] + 1
						if P[i][j] == 1:	
							if valeur == max_value_joueur[0]:
								coord_max_joueur.append([i, j])
								max_value_joueur.append(valeur)
							elif valeur > max_value_joueur[0]:
								max_value_joueur = [valeur]
								coord_max_joueur = [[i, j]]
						elif P[i][j] == -1:
							if valeur == max_value_ordi[0]:
								max_value_ordi.append(valeur)
								coord_max_ordi.append([i, j])
							elif valeur > max_value_ordi[0]:
								max_value_ordi = [valeur]
								coord_max_ordi = [[i, j]]
						M[i][j][1] = valeur
					if j+1 <= N-1:
						#test
						if P[i][j] == P[i-1][j+1]:
							valeur = M[i-1][j+1][2] + 1
							if P[i][j] == 1:	
								if valeur == max_value_joueur[0]:
									coord_max_joueur.append([i, j])
									max_value_joueur.append(valeur)
								elif valeur > max_value_joueur[0]:
									max_value_joueur = [valeur]
									coord_max_joueur = [[i, j]]
							elif P[i][j] == -1:
								if valeur == max_value_ordi[0]:
									max_value_ordi.append(valeur)
									coord_max_ordi.append([i, j])
								elif valeur > max_value_ordi[0]:
									max_value_ordi = [valeur]
									coord_max_ordi = [[i, j]]
							M[i][j][2] = valeur
				if j-1 >= 0:
					if P[i][j] == P[i][j-1]:
						valeur = M[i][j-1][3] + 1
						if P[i][j] == 1:	
							if valeur == max_value_joueur[0]:
								coord_max_joueur.append([i, j])
								max_value_joueur.append(valeur)
							elif valeur > max_value_joueur[0]:
								max_value_joueur = [valeur]
								coord_max_joueur = [[i, j]]
							elif P[i][j] == -1:
								if valeur == max_value_ordi[0]:
									max_value_ordi.append(valeur)
									coord_max_ordi.append([i, j])
								elif valeur > max_value_ordi[0]:
									max_value_ordi = [valeur]
									coord_max_ordi = [[i, j]]
						M[i][j][3] = valeur
				if np.all(M[i][j] == 0):
					valeur = 1
					if P[i][j] == 1:
						if valeur == max_value_joueur[0]:
							coord_max_joueur.append([i, j])
							max_value_joueur.append(valeur)
						elif valeur > max_value_joueur[0]:
							max_value_joueur = [valeur]
							coord_max_joueur = [[i, j]]
					elif P[i][j] == -1:
						if valeur == max_value_ordi[0]:
							max_value_ordi.append(valeur)
							coord_max_ordi.append([i, j])
						elif valeur > max_value_ordi[0]:
							max_value_ordi = [valeur]
							coord_max_ordi = [[i, j]]
					M[i][j] = [1, 1, 1, 1]
			else:
				M[i][j] = [0, 0, 0, 0]

	############### DETERMINATION DE LA POSITION DU JOUEUR ###############
	
	score = 0
	for coord_joueur in coord_max_joueur:
		for coord_ordi in coord_max_ordi:
			score = score + pas * (max_value_joueur[0]-max_value_ordi[0])

	directions_joueur = [np.argmax(M[coord[0]][coord[1]]) for coord in coord_max_joueur]
	directions_ordi = [np.argmax(M[coord[0]][coord[1]]) for coord in coord_max_ordi]
	infos_joueur = [max_value_joueur, coord_max_joueur, directions_joueur]
	infos_ordi = [max_value_ordi, coord_max_ordi, directions_ordi]
	return ( score, infos_joueur, infos_ordi)
def InitPosition(N, P):
	"""
		P = list()
		N = dimension du tableau
	Initialise P avec des 0
		==> P tableau NxN de 0
	"""
	for i in range(N):
		P.append(list())
		for j in range(N):
			P[i].append(0)
	return P

def AffichePosition(N, P):
	"""
		Affiche dans la console le tableau P
	"""
	print("Tableau P position : ")
	for i in range(N):
		ligne  = "\t"
		for j in range(N):
			if P[i][j] == -1:
				ligne += "X  "
			elif P[i][j] == 0:
				ligne += ".  "
			else:
				ligne += "O  "
		print(ligne)
		print()

def PlusDeCasesLibres(N, P):
	"""
		Retourne:
			- 1 si le jeu n'est pas fini
			- 0 si le jeu est fini
	"""
	for i in range(N):
		for j in range(N):
			if P[i][j] == 0:
				return 1
	return 0

def SaisirCoupJoueur(N, P):
	"""
		Demande des coordonnées au joueur et pet un pion aux coordonnées entrées
	"""
	print("Entrez les coordonnees de ou vous voulez mettre votre pion")
	x = int(input("\tX => "))-1
	y = int(input("\tY => "))-1
	while x>N or y>N or x<0 or y<0 or P[x][y] != 0 : 	
		print("Coordonnees incorrectes, reessayez :")
		x = int(input("\tX => "))-1
		y = int(input("\tY => "))-1
	P[x][y] = 1
	return P


def Coord_cases_vides(N,P):
	coords = []
	for i in range(N):
		for j in range(N):
			if P[i][j] == 0:
				coords.append((i,j))
	return coords

def Placer1(P, N, A, max_value, coord_max):
	if coord_max in CoordDiagGD(P, N, A):
		(P, place) = PlacerDiagGD(P, N, max_value, coord_max)
		if place == 1:
			return (P, place)
	if coord_max in CoordDiagDG(P, N, A):
		(P, place) = PlacerDiagDG(P, N, max_value, coord_max)
		if place == 1:
			return (P, place)
	(P, place) = PlacerHoriz(P, N, max_value, coord_max)
	if place == 1:
		return (P, place)
	(P, place) = PlacerVert(P, N, max_value, coord_max)
	return (P, place)



def PlacerDiagGD(P, N, max_value, coord_max):
	place = 0
	x = coord_max[0]
	y = coord_max[1]
	if x + 1  < N:
		if y + 1 < N:
			if P[x+1][y+1] == 0:
				P[x+1][y+1] = -1
				place = 1
				return (P, place)
	if x - max_value >= 0:
		if y - max_value >= 0:
			if P[x-max_value][y-max_value] == 0:
				P[x-max_value][y-max_value] = -1
				place = 1
				return (P,place)
	return (P, place)



def PlacerDiagDG(P, N, max_value, coord_max):
	place = 0
	x = coord_max[0]
	y = coord_max[1]
	if x + 1  < N:
		if y - 1 >= 0:
			if P[x+1][y-1] == 0:
				P[x+1][y-1] = -1
				place = 1
				return (P, place)
	if x - max_value >= 0:
		if y + max_value < N:
			if P[x-max_value][y+max_value] == 0:
				P[x-max_value][y+max_value] = -1
				place = 1
				return (P,place)
	return (P, place)


def PlacerVert(P, N, max_value, coord_max):
	place = 0
	x = coord_max[0]
	y = coord_max[1]
	if x + 1  < N:
		if P[x+1][y] == 0:
			P[x+1][y] = -1
			place = 1
			return (P, place)
	if x - max_value >= 0:
		if P[x-max_value][y] == 0:
			P[x-max_value][y] = -1
			place = 1
			return (P,place)
	return (P, place)


def PlacerHoriz(P, N, max_value, coord_max):
	place = 0
	x = coord_max[0]
	y = coord_max[1]
	if y + 1  < N:
		if P[x][y+1] == 0:
			P[x][y+1] = -1
			place = 1
			return (P, place)
	if y - max_value >= 0:
		if P[x][y-max_value] == 0:
			P[x][y-max_value] = -1
			place = 1
			return (P,place)
	return (P, place)


def PlacerAleat(P, N):
	coord_vides = Coord_cases_vides(N,P)
	coord_alea_vide = coord_vides[r.randint(0,len(coord_vides)-1)]
	x = coord_alea_vide[0]
	y = coord_alea_vide[1]
	P[x][y] = -1
