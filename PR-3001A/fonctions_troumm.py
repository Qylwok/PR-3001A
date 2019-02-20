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
	Mt = np.zeros((N, N, 4))
	# M[i][j][0 1 2 ou 3] avec :
	# 0 : direction en haut à gauche
	# 1 : direction en haut
	# 2 : direction en haut à droite
	# 3 : direction à gauche

	M[0][0] = [0, 0, 0, 0]
	Mt[0][0] = [0, 0, 0, 0]
	pas = 1000/A
	max_value_joueur = [0]
	max_value_ordi = [0]
	directions_joueur = []
	coord_max_joueur = [[]]
	coord_max_ordi = [[]]
	directions_ordi = []
	type_ligne_joueur = []
	type_ligne_ordi = []
	coord_diag_GD = CoordDiagGD(P,N,A) 
	coord_diag_DG = CoordDiagDG(P,N,A)
	for i in range(N):
		for j in range(N):
			if P[i][j] != 0:
				M[i][j] = [1, 1, 1, 1]
				if i-1 >= 0:
					if j-1 >=0:
						#test
						if P[i][j] == P[i-1][j-1]:
							valeur = M[i-1][j-1][0] + 1
							M[i][j][0] = valeur
					#test
					if P[i][j] == P[i-1][j]:
						valeur = M[i-1][j][1] + 1
						M[i][j][1] = valeur
					if j+1 <= N-1:
						#test
						if P[i][j] == P[i-1][j+1]:
							valeur = M[i-1][j+1][2] + 1
							M[i][j][2] = valeur
				if j-1 >= 0:
					#test
					if P[i][j] == P[i][j-1]:
						valeur = M[i][j-1][3] + 1
						M[i][j][3] = valeur
					
			else:
				M[i][j] = [0, 0, 0, 0]

	############### DETERMINATION DE LA POSITION DU JOUEUR ###############
	# for i in range(N):
	# 	for j in range(N):
	# 		print("ligne %d colonne %d : " % (i, j), M[i][j])
	# max_value_joueur += 1
	# max_value_ordi +=1
	score = 0
	# if len(coord_max) == 1:
	# 	score = pas * (max_value) * P[coord_max[0][0]][coord_max[0][1]]
	# else:
	# 	score = 0
	# 	for coord in coord_max:
	# 		score += pas * (max_value) * P[coord[0]][coord[1]] / len(coord_max)
	# directions = [np.argmax(M[coord[0]][coord[1]]) for coord in coord_max]
	# return (score, max_value, coord_max, directions)
	
	for i in range(N):
		for j in range(N):
			if [i, j] not in coord_diag_GD:
				# print("GD, i j = ", i, j)
				M[i][j][0] = 0
			if [i, j] not in coord_diag_DG:
				# print("DG, i j = ", i, j)
				M[i][j][2] = 0


	M = blocage(N, P, M)

	for i in range(N-1, -1, -1):
		for j in range(N-1, -1, -1):
			valeurs = M[i][j]
			couleura = P[i][j]
			for dir in range(4):
				val = valeurs[dir]
				if val > 0:
					if dir == 0:
						if i-A+1 >= 0 and j-A+1 >= 0:
							cpttrou = 0
							cptcouleur = 0
							for k in range(A):
								couleurb = P[i-k][j-k]
								if couleurb == 0:
									cpttrou += 1
									
								elif couleura != couleurb:
									Mt[i][j][dir] = 0
									break
								else:
									cptcouleur += 1
							if cpttrou > cptcouleur:
								Mt[i][j][dir] = 0
							else: 
								Mt[i][j][dir] = cptcouleur
							
					elif dir == 1:
						if i-A+1 >= 0:
							cpttrou = 0
							cptcouleur = 0
							for k in range(A):
								couleurb = P[i-k][j]
								if couleurb == 0:
									cpttrou += 1
								elif couleura != couleurb:
									Mt[i][j][dir] = 0
									break
								else:
									cptcouleur += 1
							if cpttrou > cptcouleur:
								Mt[i][j][dir] = 0
							else: 
								Mt[i][j][dir] = cptcouleur
							
					elif dir == 2:
						if i-A+1 >= 0 and j+A-1 < N:
							cpttrou = 0
							cptcouleur = 0
							for k in range(A):
								couleurb = P[i-k][j+k]
								if couleurb == 0:
									cpttrou += 1
								elif couleura != couleurb:
									Mt[i][j][dir] = 0
									break
								else:
									cptcouleur += 1
							if cpttrou > cptcouleur:
								Mt[i][j][dir] = 0
							else:
								Mt[i][j][dir] = cptcouleur
							
					else:
						if j-A+1 >= 0:
							cpttrou = 0
							cptcouleur = 0
							for k in range(A):
								couleurb = P[i][j-k]
								if couleurb == 0:
									cpttrou += 1
								elif couleura != couleurb:
									Mt[i][j][dir] = 0
									break
								else:
									cptcouleur += 1
							if cpttrou > cptcouleur:
								Mt[i][j][dir] = 0
							else:
								Mt[i][j][dir] = cptcouleur
							

	for i in range(N):
		for j in range(N):
			directionsn = M[i, j] 
			directionst = Mt[i, j]
			for k in range(4): 
				valeurn = directionsn[k]
				valeurt = directionst[k]
				if P[i][j] == 1:	
					if valeurn == max_value_joueur[0]:
						coord_max_joueur.append([i, j])
						max_value_joueur.append(valeurn)
						directions_joueur.append(k)
						type_ligne_joueur.append("n")
					elif valeurn > max_value_joueur[0]:
						max_value_joueur = [valeurn]
						coord_max_joueur = [[i, j]]
						directions_joueur = [k]
						type_ligne_joueur = ["n"]
					if valeurt == max_value_joueur[0]:
						coord_max_joueur.append([i, j])
						max_value_joueur.append(valeurt)
						directions_joueur.append(k)
						type_ligne_joueur.append("t")
					elif valeurt > max_value_joueur[0]:
						max_value_joueur = [valeurt]
						coord_max_joueur = [[i, j]]
						directions_joueur = [k]
						type_ligne_joueur = ["t"]
				elif P[i][j] == -1:
					if valeurn == max_value_ordi[0]:
						max_value_ordi.append(valeurn)
						coord_max_ordi.append([i, j])
						directions_ordi.append(k)
						type_ligne_ordi.append("n")
					elif valeurn > max_value_ordi[0]:
						max_value_ordi = [valeurn]
						coord_max_ordi = [[i, j]]
						directions_ordi = [k]
						type_ligne_ordi = ["n"]
					if valeurt == max_value_ordi[0]:
						max_value_ordi.append(valeurt)
						coord_max_ordi.append([i, j])
						directions_ordi.append(k)
						type_ligne_ordi.append("t")
					elif valeurt > max_value_ordi[0]:
						max_value_ordi = [valeurt]
						coord_max_ordi = [[i, j]]
						directions_ordi = [k]
						type_ligne_ordi = ["t"]


	for coord_joueur in coord_max_joueur:
		for coord_ordi in coord_max_ordi:
			score = score + pas * (max_value_joueur[0]-max_value_ordi[0])
	score = score/(len(max_value_joueur)+len(max_value_ordi))
	# directions_joueur = [np.argmax(M[coord[0]][coord[1]]) for coord in coord_max_joueur]
	# directions_ordi = [np.argmax(M[coord[0]][coord[1]]) for coord in coord_max_ordi]
	infos_joueur = [max_value_joueur, coord_max_joueur, directions_joueur, type_ligne_joueur]
	infos_ordi = [max_value_ordi, coord_max_ordi, directions_ordi, type_ligne_ordi]
	return ( M, Mt, score, infos_joueur, infos_ordi)

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
		Demande des coordonnées au joueur et met un pion aux coordonnées entrées
	"""
	print("Entrez les coordonnees de ou vous voulez mettre votre pion")
	x = EntrezUnNombre("\tX => ")-1
	y = EntrezUnNombre("\tY => ")-1
	# !!! CAS OU (INPUT != INT) A PRENDRE EN COMPTE
	while x>N or y>N or x<0 or y<0 or P[x][y] != 0 : 	# or (type(x) != type(int())) or (type(y) != type(int())):
		print("Coordonnees incorrectes, reessayez :")
		x = EntrezUnNombre("\tX => ")-1
		y = EntrezUnNombre("\tY => ")-1
	P[x][y] = 1
	return P

def EntrerUnNombre(message):
	while True:
		try:
			valeur_entree = int(input(message))
		except ValueError:
			print("Entrez un entier")
			continue
		else:
			return valeur_entree
			break

def PierreFeuilleCiseaux(P, N):
	print("Jouez à Pierre Feuille Ciseaux pour déterminer le premier joueur")
	print("Entrez Pierre, Feuille ou Ciseaux")
	val_joueur = input().capitalize()
	print("Vous avez joué : ", val_joueur)
	PFC = ["Pierre", "Feuille", "Ciseaux"]
	if val_joueur == "Pierre":
		val_ordi = PFC[r.randint(1,2)]
	if val_joueur == "Feuille":
		val_ordi = PFC[r.randint(0,1)*2]
	if val_joueur == "Ciseaux":
		val_ordi = PFC[r.randint(0,1)]	
	
	print("L'ordinateur a joué : ", val_ordi)
	# while val_joueur == val_ordi:
	# 	print("Egalité, recommencez")
	# 	val_joueur = input().capitalize()
	# 	print("Vous avez joué : ", val_joueur)
	# 	val_ordi = PFC[r.randint(0,2)]
	# 	print("L'ordinateur a joué : ", val_ordi)
	if (val_joueur == "Pierre" and val_ordi == "Ciseaux") or (val_joueur == "Ciseaux" and val_ordi == "Feuille") or (val_joueur == "Feuille" and val_ordi == "Pierre"): 
		print("Vous avez gagné, vous commencez")
		return (P, 1) 
	else:
		print("L'ordinateur a gagné, il commence")
		P = OrdiCommence(P,N)
		return (P,1)

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

def DiagGD(P, N, max_value, coord_max):
	place = 0
	bloque = 1
	# print("coord_max  :", coord_max)
	x = coord_max[0]
	y = coord_max[1]
	if x + 1  < N:
		if y + 1 < N:
			if P[x+1][y+1] == 0:	
				place = 1
				bloque = 1
			elif P[x+1][y+1] == P[x][y]:
				bloque = 1
			else:
				bloque = 0	
	if x - max_value >= 0:
		if y - max_value >= 0:
			if P[x-max_value][y-max_value] == 0:
				place = 2
				bloque = 2
			elif P[x-max_value][y-max_value] == P[x][y]:
				bloque = 2	
			else:
				bloque = 0
	return (place, bloque)

def PlacerDiagGD(P, N, max_value, coord_max):
	(place, bloque) = DiagGD(P, N, max_value, coord_max)

	x = coord_max[0]
	y = coord_max[1]
	if place == 1:
		P[x+1][y+1] = -1
		return (P, 1)
	elif place == 2:
		P[x-max_value][y-max_value] = -1
		return (P, 1)
	else:
		return (P, 0)

def PlacerDiagGDTrou(P, N, A, coord_max):
	x = coord_max[0]
	y = coord_max[1]
	for i in range(A):
		val = P[x-i][y-i]
		if val == 0:
			P[x-i][y-i] = -1
			return (P, 1)
	return (P, 0)

def DiagDG(P, N, max_value, coord_max):
	place = 0
	bloque = 1
	x = coord_max[0]
	y = coord_max[1]
	if x + 1  < N:
		if y - 1 >= 0:
			if P[x+1][y-1] == 0:
				place = 1
				bloque = 1
			elif P[x+1][y-1] == P[x][y]:
				bloque = 1
			else:
				bloque = 0
	if x - max_value >= 0:
		if y + max_value < N:
			if P[x-max_value][y+max_value] == 0:
				place = 2 
				bloque = 2
			elif P[x-max_value][y+max_value] ==P[x][y]:	
				bloque = 2
			else:
				bloque = 0
	return (place, bloque)

def PlacerDiagDG(P, N, max_value, coord_max):
	(place, bloque) = DiagDG(P, N, max_value, coord_max)
	x = coord_max[0]
	y = coord_max[1]
	if place == 1:
		P[x+1][y-1] = -1
		return (P, 1)
	elif place == 2:
		P[x-max_value][y+max_value] = -1
		return (P, 1)
	else:
		return (P, 0)

def PlacerDiagDGTrou(P, N, A, coord_max):
	x = coord_max[0]
	y = coord_max[1]
	for i in range(A):
		val = P[x-i][y+i]
		if val == 0:
			P[x-i][y+i] = -1
			return (P, 1)
	return (P, 0)

def Vert(P, N, max_value, coord_max):
	place = 0
	bloque = 1
	x = coord_max[0]
	y = coord_max[1]
	if x + 1  < N:
		if P[x+1][y] == 0:
			place = 1
			bloque = 1
		elif P[x+1][y] == P[x][y]:
			bloque = 1
		else:
			bloque = 0	
	if x - max_value >= 0:
		if P[x-max_value][y] == 0:
			place = 2
			bloque = 2
		elif P[x-max_value][y] == P[x][y]:
			bloque = 2
		else:
			bloque = 0		
	return (place, bloque)

def PlacerVert(P, N, max_value, coord_max):
	(place, bloque) = Vert(P, N, max_value, coord_max)
	x = coord_max[0]
	y = coord_max[1]
	if place == 1:
		P[x+1][y] = -1
		return (P, 1)
	elif place == 2:
		P[x-max_value][y] = -1
		return (P, 1)
	else:
		return (P, 0)

def PlacerVertTrou(P, N, A, coord_max):
	x = coord_max[0]
	y = coord_max[1]
	for i in range(A):
		val = P[x-i][y]
		if val == 0:
			P[x-i][y] = -1
			return (P, 1)
	return (P, 0)

def Horiz(P, N, max_value, coord_max):
	place = 0 
	bloque = 1
	x = coord_max[0]
	y = coord_max[1]
	if y + 1  < N:
		if P[x][y+1] == 0:
			place = 1 
			bloque = 1
		elif P[x][y+1] == P[x][y]:
			bloque = 1
		else:
			bloque = 0
	if y - max_value >= 0:
		if P[x][y-max_value] == 0:
			place = 2
			bloque = 2
		elif P[x][y-max_value] == P[x][y]:
			bloque = 2
		else:
			bloque = 0
	return (place, bloque)

def PlacerHoriz(P, N, max_value, coord_max):
	(place, bloque) = Horiz(P, N, max_value, coord_max)
	x = coord_max[0]
	y = coord_max[1]
	if place == 1:
		P[x][y+1] = -1
		return (P, 1)
	elif place == 2:
		P[x][y-max_value] = -1
		return (P, 1)
	else:
		return (P, 0)

def PlacerHorizTrou(P, N, A, coord_max):
	x = coord_max[0]
	y = coord_max[1]
	for i in range(A):
		val = P[x][y-i]
		if val == 0:
			P[x][y-i] = -1
			return (P, 1)
	return (P, 0)	

def PlacerAleat(P, N):
	coord_vides = Coord_cases_vides(N,P)
	coord_alea_vide = coord_vides[r.randint(0,len(coord_vides)-1)]
	x = coord_alea_vide[0]
	y = coord_alea_vide[1]
	P[x][y] = -1

def OrdiCommence(P, N):
	x = r.randint(0, N-1)
	print("x =", x)
	y = r.randint(0, N-1)
	print("y = ", y)
	P[x][y] = -1
	return P

def CoordDiagGD(P, N, A):
	coord = []
	k = N - A
	for i in range(N):
		for j in range(N):
			if abs(i-j) <= k:
				coord.append([i, j])
	return coord

def CoordDiagDG(P, N, A):
	coordDG = CoordDiagGD(P, N, A)
	coord = []
	k = int(N/2)
	for elt in coordDG:
		x = elt[0]
		y = elt[1]
		yp = (N-1-y)%N
		coord.append([x, yp])
	return coord
	
def blocage(N, P, M):
	for i in range(N-1, -1, -1):
		for j in range(N-1, -1, -1):
			if P[i][j] != 0:
				directions = M[i][j]
				# print("directions = ", directions)
				for k in range(len(directions)):
					
					
					val = int(directions[k])
					
					# if j == 0:
					# print("i, j = ", i, j)
					# 	print("k = ", k)
					# 	print("val = ", val)
					if k == 0:						
						(place, bloque) = DiagGD(P, N, val, [i, j])
						# print("bloque = ", bloque)
						if bloque == 0:
							for l in range(val):
								M[i-l][j-l][0] = 0 
					elif k == 1:
						(place, bloque) = Vert(P, N, val, [i, j])
						# print("bloque = ", bloque)
						if bloque == 0:
							for l in range(val):
								M[i-l][j][1] = 0
					elif k == 2:
						(place, bloque) = DiagDG(P, N, val, [i, j])
						# print("bloque = ", bloque)
						if bloque == 0:
							for l in range(val):
								M[i-l][j+l][2] = 0
					else:
						(place, bloque) = Horiz(P, N, val, [i, j])
						# print("bloque = ", bloque)
						if bloque == 0:
							for l in range(val):
								M[i][j-l][3] = 0
	return M

def minimax(N, position, A, degre_actuel, degre_voulu, joueur):
	# print("Entrée minimax")
	# print("Tour de : ", joueur)
	# print("################################")
	# print()
	# print("Position : ", position)
	# print()

	# Condition d'arrêt
	if degre_actuel == degre_voulu:
		return EvalPosition(N, position, A)[2]

	# On regarde toutes les prochaines positions possibles (au degré 1)
	# print("Calcul des prochaines positions")
	(next_positions, position_coups) = Prochaines_positions_possibles(N, position, A, joueur)
	eval_next_positions = []
	# for posss in next_positions:
		# print("Une prochaine position : ")
		# AffichePosition(N, posss)
	# print()

	# Et on les évalue
	# Si on a atteint le degré voulu, on a juste à faire 
	# 	 un EvalPosition pour chaque nouvelle position
	if degre_actuel + 1 == degre_voulu:
		# print("EvalPosition sur chaque position")
		for pos in next_positions:
			# print("Evaluation de la position : ")
			# AffichePosition(N, pos)
			evaluation = EvalPosition(N, pos, A)[2]
			eval_next_positions.append(evaluation)
	# Sinon on doit refaire un minimax pour avoir l'évaluation de la position (récursion)
	else:
		# print("minimax sur chaque position")
		# print()
		for pos in next_positions:
			evaluation = minimax(N, pos, A, degre_actuel + 1, degre_voulu, -joueur)[0]
			eval_next_positions.append(evaluation)
	# print()
	# Maintenant qu'on a toutes les prochaines positions et leur évaluation, 
	# on ne considère que celle qui avantage le plus le joueur courrant
	# Si c'est l'ordinateur, on essaye de se rapprocher le plus de -1000
	# Si c'est le joueur, on essaye de se rapprocher le plus de 1000
	# print("Eval_next_positions : ", eval_next_positions)
	if joueur == 1: # Cas du joueur
		arg = np.argmax(eval_next_positions)
		return (eval_next_positions[arg], position_coups[arg])
	else: # Cas de l'ordinateur
		# print("Score : ", min(eval_next_positions))
		arg = np.argmin(eval_next_positions)
		return (eval_next_positions[arg], position_coups[arg])

def MinMax(N, position, A, joueur, degre):
	(M, Mt, score, infos_joueur, infos_ordi) = EvalPosition(N, position, A)
	nb_cases_vides = len(Coord_cases_vides(N, position))
	if degre > nb_cases_vides:
		return (M, Mt, minimax(N, position, A, 0, nb_cases_vides, joueur), infos_joueur, infos_ordi)
	else:
		return (M, Mt, minimax(N, position, A, 0, degre, joueur), infos_joueur, infos_ordi)

def Prochaines_positions_possibles(N, P, A, joueur):
	cases_vides = Coord_cases_vides(N, P)
	next_P = []
	coords = []
	for coord in cases_vides:
		(x, y) = coord
		new_P = InitPosition(N, [])
		for i in range(len(P)):
			for j in range(len(P[0])):
				new_P[i][j] = P[i][j]
		new_P[x][y] = joueur
		next_P.append(new_P)
		coords.append(coord)
	return (next_P, coords)

			



# def main():

# 	N = 5
# 	P = [[-1, 0, 1, 0, -1], [1, 0, -1, 1, 0], [-1, 1, -1, 1, 0], [0, 1, -1, 1, -1], [-1, 0, 1, -1 ,1]]
# 	A = 4
# 	print("N = %d" % N)
# 	for i in range(N):
# 		for j in range(N):
# 			print("P : ligne %d colonne %d : " % (i, j), P[i][j])
# 	print("A = %d" % A)
# 	print("Entree EvalPosition")
# 	(score, max_value, coord_max, M) = EvalPosition(N, P, A)
# 	print()
# 	print("max_value = %d" % max_value)
# 	print("coord_max = ", coord_max)
# 	for i in range(N):
# 		for j in range(N):
# 			print("ligne %d colonne %d : " % (i, j), M[i][j])
# 	print("score = ", score)

# main()