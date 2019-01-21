import numpy as np

def EvalPosition(N, P, A):
	'''
	ENTREES : 
		N : Entier
		P : Tableau NxN d'entiers
		A : Nombre de pions alignés nécessaires pour gagner

	SORTIE :
		Un entier entre -1000 et 1000 évaluant la position
			-1000 : Le joueur 2 a A-1 pions alignés
			1000  : Le joueur 1 a A-1 pions alignés
		On va faire une echelle avec des pas de 1000/A

	FORME DE P :
		+1 si pion du joueur 1
		0  si aucun pion
		-1 si pion du joueur 2
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
	max_value = 0
	coord_max = [[0, 0]]
	for i in range(N):
		for j in range(N):
			if P[i][j] != 0:
				if i-1 >= 0:
					if j-1 >=0:
						#test
						if P[i][j] == P[i-1][j-1]:
							valeur = M[i-1][j-1][0] + 1
							if valeur == max_value:
								coord_max.append([i, j])
							elif valeur > max_value:
								max_value = valeur
								coord_max = [[i, j]]
							M[i][j][0] = valeur
					#test
					if P[i][j] == P[i-1][j]:
						valeur = M[i-1][j][1] + 1
						if valeur == max_value:
							coord_max.append([i, j])
						elif valeur > max_value:
							max_value = valeur
							coord_max = [[i, j]]
						M[i][j][1] = valeur
					if j+1 <= N-1:
						#test
						if P[i][j] == P[i-1][j+1]:
							valeur = M[i-1][j+1][2] + 1
							if valeur == max_value:
								coord_max.append([i, j])
							elif valeur > max_value:
								max_value = valeur
								coord_max = [[i, j]]
							M[i][j][2] = valeur
				if j-1 >= 0:
					#test
					if P[i][j] == P[i][j-1]:
						valeur = M[i][j-1][3] + 1
						if valeur == max_value:
							coord_max.append([i, j])
						elif valeur > max_value:
							max_value = valeur
							coord_max = [[i, j]]
						M[i][j][3] = valeur
			else:
				M[i][j] = [0, 0, 0, 0]

	############### DETERMINATION DE LA POSITION DU JOUEUR ###############
	max_value += 1
	if len(coord_max) == 1:
		score = pas * (max_value) * P[coord_max[0][0]][coord_max[0][1]]
	else:
		score = 0
		for coord in coord_max:
			score += pas * (max_value) * P[coord[0]][coord[1]] / len(coord_max)

	return (score, max_value, coord_max, M)

def main():
	N = 5
	P = [[-1, 0, 1, 0, -1], [1, 0, -1, 1, 0], [-1, 1, -1, 1, 0], [0, 1, -1, 1, -1], [-1, 0, 1, -1 ,1]]
	A = 4
	print("N = %d" % N)
	for i in range(N):
		for j in range(N):
			print("P : ligne %d colonne %d : " % (i, j), P[i][j])
	print("A = %d" % A)
	print("Entree EvalPosition")
	(score, max_value, coord_max, M) = EvalPosition(N, P, A)
	print()
	print("max_value = %d" % max_value)
	print("coord_max = ", coord_max)
	for i in range(N):
		for j in range(N):
			print("ligne %d colonne %d : " % (i, j), M[i][j])
	print("score = ", score)

main()