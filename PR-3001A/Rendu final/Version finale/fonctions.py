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


	M = blocage(P, N, A, M)

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
									cpttrou = 0
									break
								else:
									cptcouleur += 1
							if cpttrou == 0 or M[i][j][0] == cptcouleur:
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
									cpttrou = 0
									break
								else:
									cptcouleur += 1
							if cpttrou == 0 or M[i][j][1] == cptcouleur:
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
									cpttrou = 0
									break
								else:
									cptcouleur += 1
							if cpttrou == 0 or M[i][j][2] == cptcouleur:
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
									cpttrou = 0
									break
								else:
									cptcouleur += 1
							if cpttrou == 0 or M[i][j][3] == cptcouleur:
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
	ligne1 = "\t     "
	ligne2 = "\t    "
	for a in range(N):
		ligne1 += str(a+1) + "  " 
		ligne2 += "__ "
	print(ligne1)
	print(ligne2)
	for i in range(N):
		ligne  = "\t " + str(i+1) + " | "
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
	x = EntrerUnNombre("\tNuméro de ligne => ")-1
	y = EntrerUnNombre("\tNuméro de colonne => ")-1
	while x>N or y>N or x<0 or y<0 or P[x][y] != 0 : 	
		print("Coordonnees incorrectes, reessayez :")
		x = EntrerUnNombre("\tNuméro de ligne => ")-1
		y = EntrerUnNombre("\tNuméro de colonne => ")-1
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
	elif val_joueur == "Feuille":
		val_ordi = PFC[r.randint(0,1)*2]
	elif val_joueur == "Ciseaux":
		val_ordi = PFC[r.randint(0,1)]
	else:
		val_ordi = PFC[r.randint(0,2)]	
	
	print("L'ordinateur a joué : ", val_ordi)


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


def OrdiCommence(P, N):
	x = r.randint(0, N-1)
	y = r.randint(0, N-1)
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
	
def blocage(P, N, A, M):
	for i in range(N-1, -1, -1):
		for j in range(N-1, -1, -1):
			if P[i][j] != 0:
				directions = M[i][j]
				for k in range(len(directions)):
					val = int(directions[k])
					if val > 0:
						if k == 0:	
							cpttrou = 0
							cptcouleur = 0
							coords = []
							for l in range(A):
								ip = i-l
								jp = j-l
								if ip<0 or jp<0:
									break
								if P[ip][jp] == 0:
									cpttrou += 1
								elif P[ip][jp] == P[i][j]:
									cptcouleur += 1
									coords.append([ip, jp])
								else:
									break
							for l in range(1, A):
								ip = i+l
								jp = j+l
								if ip>=N or jp>=N:
									break
								if P[ip][jp] == 0:
									cpttrou += 1
								elif P[ip][jp] == P[i][j]:
									cptcouleur += 1
									coords.append([ip, jp])
								else:
									break
							if cptcouleur + cpttrou < A:
								for c in coords:
									M[c[0]][c[1]][0] = 0

						elif k == 1:
							cpttrou = 0
							cptcouleur = 0
							coords = []
							for l in range(A):
								ip = i-l
								if ip<0 :
									break
								if P[ip][j] == 0:
									cpttrou += 1
								elif P[ip][j] == P[i][j]:
									cptcouleur += 1
									coords.append([ip, j])
								else:
									break
							for l in range(1, A):
								ip = i+l
								if ip>=N:
									break
								if P[ip][j] == 0:
									cpttrou += 1
								elif P[ip][j] == P[i][j]:
									cptcouleur += 1
									coords.append([ip, j])
								else:
									break
							if cptcouleur + cpttrou < A:
								for c in coords:
									M[c[0]][c[1]][1] = 0
						elif k == 2:
							cpttrou = 0
							cptcouleur = 0
							coords = []
							for l in range(A):
								ip = i-l
								jp = j+l
								if ip<0 or jp>=N:
									break
								if P[ip][jp] == 0:
									cpttrou += 1
								elif P[ip][jp] == P[i][j]:
									cptcouleur += 1
									coords.append([ip, jp])
								else:
									break
							for l in range(1, A):
								ip = i+l
								jp = j-l
								if ip>=N or jp<0:
									break
								if P[ip][jp] == 0:
									cpttrou += 1
								elif P[ip][jp] == P[i][j]:
									cptcouleur += 1
									coords.append([ip, jp])
								else:
									break
							if cptcouleur + cpttrou < A:
								for c in coords:
									M[c[0]][c[1]][2] = 0
						else:
							cpttrou = 0
							cptcouleur = 0
							coords = []
							for l in range(A):
								jp = j-l
								if jp<0:
									break
								if P[i][jp] == 0:
									cpttrou += 1
								elif P[i][jp] == P[i][j]:
									cptcouleur += 1
									coords.append([i, jp])
								else:
									break
							for l in range(1, A):
								jp = j+l
								if jp>=N:
									break
								if P[i][jp] == 0:
									cpttrou += 1
								elif P[i][jp] == P[i][j]:
									cptcouleur += 1
									coords.append([i, jp])
								else:
									break
							# print("i = ", i , "j = ", j)
							# print("cptcouleur = ", cptcouleur)
							# print("cpttrou = ", cpttrou)
							if cptcouleur + cpttrou < A:
								for c in coords:
									M[c[0]][c[1]][3] = 0
	return M

def minimax(N, position, A, degre_actuel, degre_voulu, joueur, alpha, beta):
	# Condition d'arrêt (jamais atteinte en faite xd)
	if degre_actuel == degre_voulu:
		return EvalPosition(N, position, A)[2]

	# On regarde toutes les prochaines positions possibles (au degré 1)
	pos_et_coords = Prochaines_positions_possibles(N, position, A, joueur)
	(next_positions, position_coups) = pos_et_coords
	# most_valuable_score = int()
	most_valuable_coord = ()

	# Et on les évalue
	# Si on a atteint le degré voulu, on a juste à faire 
	# 	 un EvalPosition pour chaque nouvelle position
	if joueur == 1:
		most_valuable_score = -np.inf
		if degre_actuel + 1 == degre_voulu:
			for k in range(len(next_positions)):
				pos = next_positions[k]
				coord = position_coups[k]
				evaluation = EvalPosition(N, pos, A)[2]
				if evaluation > most_valuable_score:
					most_valuable_score = evaluation
					most_valuable_coord = coord
				if most_valuable_score >= beta:
					return (most_valuable_score, most_valuable_coord)
				alpha = max(alpha, most_valuable_score)
				
		# Sinon on doit refaire un minimax pour avoir l'évaluation de la position (récursion)
		else:
			for k in range(len(next_positions)):
				pos = next_positions[k]
				coord = position_coups[k]
				evaluation = minimax(N, pos, A, degre_actuel + 1, degre_voulu, -joueur, alpha, beta)[0]
				if evaluation > most_valuable_score:
					most_valuable_score = evaluation
					most_valuable_coord = coord
				if most_valuable_score >= beta:
					return (most_valuable_score, most_valuable_coord)
				alpha = max(alpha, most_valuable_score)
	else: # Cas de l'ordinateur
		most_valuable_score = np.inf
		if degre_actuel + 1 == degre_voulu:
			for k in range(len(next_positions)):
				pos = next_positions[k]
				coord = position_coups[k]
				evaluation = EvalPosition(N, pos, A)[2]
				if evaluation < most_valuable_score:
					most_valuable_score = evaluation
					most_valuable_coord = coord
				if alpha >= most_valuable_score:
					return (most_valuable_score, most_valuable_coord)
				beta = min(beta, most_valuable_score)
		# Sinon on doit refaire un minimax pour avoir l'évaluation de la position (récursion)
		else:
			for k in range(len(next_positions)):
				pos = next_positions[k]
				coord = position_coups[k]
				evaluation = minimax(N, pos, A, degre_actuel + 1, degre_voulu, -joueur, alpha, beta)[0]
				if evaluation < most_valuable_score:
					most_valuable_score = evaluation
					most_valuable_coord = coord
				if alpha >= most_valuable_score:
					return (most_valuable_score, most_valuable_coord)
				beta = min(beta, most_valuable_score)
	return (most_valuable_score, most_valuable_coord)

def MinMax(N, position, A, joueur, degre):
	(M, Mt, score, infos_joueur, infos_ordi) = EvalPosition(N, position, A)
	nb_cases_vides = len(Coord_cases_vides(N, position))
	if degre > nb_cases_vides:
		# AffichePosition(N, position)
		mm = minimax(N, position, A, 0, nb_cases_vides, joueur, -np.inf, np.inf)
		return (M, Mt, mm, infos_joueur, infos_ordi)
	else:
		# AffichePosition(N, position)
		mm = minimax(N, position, A, 0, degre, joueur, -np.inf, np.inf)
		return (M, Mt, mm, infos_joueur, infos_ordi)

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

			


