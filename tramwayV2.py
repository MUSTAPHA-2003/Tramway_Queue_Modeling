import math
import matplotlib.pyplot as plt
import numpy as np

def lnFactorial(n):
	sum = 0
	for i in range(1, n+1):
		sum += np.log(i)
	return sum

class tramway:
	def __init__(self):
		self.nbrDePlacesDansUnTramway = 0
		self.tempsVoyageComplet = 0
		self.tempsMoyenEntreDeuxClients = 0
		self.nbrStations = 0
		self.nbrVehicules = 0
		#alpha = temps moyen de chaque client en serveur / temps voyage complet : POURCENTAGE en %
		self.alpha = 0
	def setNbrDePlacesDansUnTramway(self, nbrDePlacesDansUnTramway):
		self.nbrDePlacesDansUnTramway = nbrDePlacesDansUnTramway
	def setTempsVoyageComplet(self, tempsVoyageComplet):
		self.tempsVoyageComplet = tempsVoyageComplet
	def setTempsMoyenEntreDeuxClients(self, tempsMoyenEntreDeuxClients):
		self.tempsMoyenEntreDeuxClients = tempsMoyenEntreDeuxClients
	def setNbrStations(self, nbrStations):
		self.nbrStations = nbrStations
	def setNbrVehicules(self, nbrVehicules):
		self.nbrVehicules = nbrVehicules
	def setAlpha(self, alpha):
		self.alpha = alpha/100
	def calculateParams(self):
		self.mu = 1 / (self.tempsVoyageComplet * self.alpha * 2)
		self.lamda = 1 / (self.tempsMoyenEntreDeuxClients / self.nbrStations)
		self.serveurs = self.nbrDePlacesDansUnTramway * self.nbrVehicules
	def rho(self, s = -1):
		if s == -1:
			s = self.serveurs
		return self.lamda / (s * self.mu)
	def verifyConditions(self):
		if self.rho() < 1:
			return True
		else:
			print("Systeme non stable")
			print("nombre de clients dans le systeme : ", self.calculateL())
			print("nombre de serveurs : ", self.serveurs)
			return False
	def calculateP0(self):
		lnElement1 = 0
		lnElement2 = 0
		P0 = 0
		try:
			for i in range(self.serveurs):
				lnElement1 += self.rho(1) ** i / math.factorial(i)
			lnElement1 = np.log(lnElement1)
		except OverflowError:
			lnElement1 = self.rho(1)
		lnElement2 = (self.serveurs * np.log(self.rho(1)) - lnFactorial(self.serveurs) - np.log(abs(1 - self.rho())))*(1-self.rho())/abs(1-self.rho())
		P0 = np.exp(lnElement1) + np.exp(lnElement2)
		P0 = 1 / P0
		return P0
	def calculatePn(self, n):
		if n == 0:
			return self.calculateP0()
		elif n <= self.serveurs:
			lnElement1 = 0
			lnElement1 = lnFactorial(n) - n*np.log(self.rho(1))
			sum = 0
			try:
				for i in range(self.serveurs):
					sum += self.rho(1) ** i / math.factorial(i)
				sum = np.log(sum)
			except OverflowError:
				sum = self.rho(1)
			lnElement1 += sum
			lnElement2 = (lnFactorial(n) + (self.serveurs - n) * np.log(self.rho(1)) - lnFactorial(self.serveurs) - np.log(abs(1 - self.rho()))) * self.rho() / (1 - self.rho())
			return 1 / (np.exp(lnElement1) + np.exp(lnElement2))
		else:
			lnElement1 = 0
			lnElement1 = lnFactorial(self.serveurs) + lnFactorial(n-self.serveurs) - n*np.log(self.rho(1)) 
			sum = 0
			try:
				for i in range(self.serveurs):
					sum += self.rho(1) ** i / math.factorial(i)
				sum = np.log(sum)
			except OverflowError:
				sum = self.rho(1)
			lnElement1 += sum
			lnElement2 = (lnFactorial(n-self.serveurs) + (self.serveurs-n) * np.log(self.rho(1)) - np.log(abs(1 - self.rho()))) * self.rho() / (1 - self.rho())
			return 1 / (np.exp(lnElement1) + np.exp(lnElement2))
	def calculateLq(self, correction = 1):
		if self.verifyConditions == False:
			Lq = 0
			sum = 0
			Pn = 0
			i = 0
			middle = False
			YES = 0
			while sum < 0.99999:
				Pn = self.calculatePn(i)
				Lq += Pn * (i - self.serveurs)
				sum += Pn
				i += 1
				if Pn == 0 and YES == 0:
					i*=2
					if self.calculatePn(i) != 0:
						i = i // 2
						YES = 1
				if Pn != 0:
					middle = True
				if middle and Pn == 0:
					break
			return Lq
		Lq = 0
		lnElement1 = 0
		Element2 = (1-self.rho()) / self.rho()
		lnElement1 = lnFactorial(self.serveurs) + 2 * np.log(abs(1 - self.rho())) - np.log(self.rho()) - self.serveurs * np.log(self.rho(1))
		sum = 0
		try:
			for i in range(self.serveurs):
				sum += self.rho(1) ** i / math.factorial(i)
			sum = np.log(sum)
		except OverflowError:
			sum = self.rho(1)
		lnElement1 += sum
		Lq = 1 / (np.exp(lnElement1) + Element2)
		return Lq
	def calculateWq(self, correction = 1):
	#Dans la théorie des files d'attente M/M/c standard, la formule classique pour le temps moyen d'attente en file (Wq) est: Wq = Lq / λ
	# mais ici on a un systeme de tramway, donc il faut ajouter le temps de voyage complet
	# et le temps d'attente dans le tramway
	# donc la formule devient: Wq = Lq / λ + (tempsVoyageComplet / nbrVehicules) * 2
		if correction == 0:
			return self.calculateLq(correction=correction) / self.lamda
		return self.calculateLq() / self.lamda + self.tempsVoyageComplet/self.nbrVehicules*2
	def calculateW(self, correction = 1):
		if correction == 0:
			return self.calculateWq(correction=correction) + 1 / self.mu
		return self.calculateWq(correction=correction) + 1 / self.mu# * self.nbrVehicules
	def calculateL(self, correction = 1):
		if correction == 0:
			return self.calculateLq(correction=correction) + self.rho(1)
		return self.calculateLq(correction=correction) + self.rho(1)# * self.nbrVehicules
	def setAllParams(self, nbrDePlacesDansUnTramway, tempsVoyageComplet, tempsMoyenEntreDeuxClients, nbrStations, nbrVehicules, alpha):
		self.setNbrDePlacesDansUnTramway(nbrDePlacesDansUnTramway)
		self.setTempsVoyageComplet(tempsVoyageComplet)
		self.setTempsMoyenEntreDeuxClients(tempsMoyenEntreDeuxClients)
		self.setNbrStations(nbrStations)
		self.setNbrVehicules(nbrVehicules)
		self.setAlpha(alpha)
		self.calculateParams()
		return self.verifyConditions()
	def printResults(self):
		print("Temps moyen de chaque client en serveur : 1/2 * mu = ", 1 /(2 * self.mu))
		print("Temps moyen entre deux clients : 1/lamda = ", 1 / self.lamda)
		print("mu = ", self.mu)
		print("lamda = ", self.lamda)
		print("rho = ", round(self.rho(),5))
		print("P0 = ", round(self.calculateP0(),5))
		print("Le nombre de serveurs :                                    ", int(self.serveurs))
		print("Le nombre moyen de Clients qu'on attend est : Lambda * 60: ", int(self.lamda*60))
		print("Nombre moyen de clients dans le systeme : L = ", round(self.calculateL(),5))
		print("Nombre moyen de clients dans la file d'attente : Lq = ", round(self.calculateLq(),5))
		print("Temps moyen de chaque client dans le systeme : W/2 = ", round(self.calculateW(),5) / 2)
		print("Temps moyen de chaque client dans la file d'attente : Wq = ", round(self.calculateWq(),5))
	def getResults(self):
		return {
			"initial": {
				"nbrDePlacesDansUnTramway": self.nbrDePlacesDansUnTramway,
				"tempsVoyageComplet": self.tempsVoyageComplet,
				"tempsMoyenEntreDeuxClients": self.tempsMoyenEntreDeuxClients,
				"nbrStations": self.nbrStations,
				"nbrVehicules": self.nbrVehicules,
				"alpha": self.alpha
			},
			"mu": self.mu,
			"lamda": self.lamda,
			"rho": round(self.rho(),5),
			"P0": round(self.calculateP0(),5),
			"L": round(self.calculateL(),5),
			"Lq": round(self.calculateLq(),5),
			"W": round(self.calculateW(),5),
			"Wq": round(self.calculateWq(),5)
		}