from hashlib import sha256
from sys import exit
from bisect import bisect_left as bisectLeft
from operator import itemgetter
import string
import random

objects = {}

class ConsistentHashRing:

	def __init__(self,numMachines,numReplicas):
		
		self.HASH_MODULO = 10**9 + 7
		self.machineTuples = []
		self.machines = {}
		self.machineIndexCounter = 0
		self.objects = {}
		self.numMachines = numMachines
		self.numReplicas = numReplicas

		for machine in xrange(self.numMachines):
			self.addMachine()

	def _randomString(self,size=15,chars=string.ascii_uppercase + string.digits):
		return ''.join(random.choice(chars) for x in range(size))

	def _getHash(self,key):

		hashVal = int(sha256(key).hexdigest(),16) % self.HASH_MODULO / float(self.HASH_MODULO)
		return hashVal

	def addMachine(self):

		newMachine = {}
		newMachine['index'] = self.machineIndexCounter
		newMachine['replicas'] = numReplicas
		newMachine['key'] = str(self.machineIndexCounter) + "::" + self._randomString()
		newMachine['hash'] = self._getHash(newMachine['key'])
	
		self.machines[self.machineIndexCounter] = newMachine
		self.machineIndexCounter += 1
	
		self.machineTuples.append(newMachine)
		self.sortMachines()

		return self.machineIndexCounter - 1

	def removeMachine(self,machineIndex):

		if machineIndex not in self.machines:
			return 0

		machine = self.machines[machineIndex]
		machineKeyHash = machine['hash']
		del self.machines[machineIndex]

		machinesHash = [machine['hash'] for machine in self.machineTuples]
		machineIndex = bisectLeft(machinesHash,machineKeyHash)

		del self.machineTuples[machineIndex]

		return 1

	def sortMachines(self):
	
		self.machineTuples.sort(key=itemgetter('hash'))

	def printMachines(self):

		for machine in self.machineTuples:
			print machine

	def getMachine(self,key):

		if len(self.machineTuples) == 0:
			return -1

		keyHash = self._getHash(key)

		machineIndex = 0
		if keyHash < self.machineTuples[-1]['hash']:
			machinesHash = [machine['hash'] for machine in self.machineTuples]
			machineIndex = bisectLeft(machinesHash,keyHash)
		
		self.addObjectToMachine(key,self.machineTuples[machineIndex]['index'])
		return self.machineTuples[machineIndex]['index']

	def addObjectToMachine(self,key,machineIndex):

		if machineIndex in self.objects:
			self.objects[machineIndex].add(key)
		else:
			self.objects[machineIndex] = set()
			self.objects[machineIndex].add(key)
	
	def removeObjectFromMachine(self,key,machineIndex):

		if key in self.objects[machineIndex]:
			self.objects[machineIndex].remove(key)

class Object:
	
	def __init__(self,key,machineIndex):

		self.HASH_MODULO = 10**9 + 7
		self.key = key
		self.hash = self._getHash()
		self.machine = machineIndex

	def _getHash(self):

		hashVal = int(sha256(self.key).hexdigest(),16) % self.HASH_MODULO / float(self.HASH_MODULO)
		return hashVal
	
	def updateMachine(self,machineIndex):

		self.machine = machineIndex

def remapObjectsOnMachineDelete(hashRing,machineIndex):

	hashRing.printMachines()
	if machineIndex in hashRing.objects:
		for key in hashRing.objects[machineIndex]:
			newMachineIndex = hashRing.getMachine(key)
			print "Key: %s moved from %s to machine %s"%(key,machineIndex,newMachineIndex)
			objects[key].updateMachine(newMachineIndex)
		hashRing.objects[machineIndex].clear()
		del hashRing.objects[machineIndex]

def remapObjectsOnMachineInsert(hashRing,machineIndex):
	
	hashRing.printMachines()

	machineKeyHash = hashRing.machines[machineIndex]['hash']
	machinesHash = [machine['hash'] for machine in hashRing.machineTuples]

	prevMachineIndex = bisectLeft(machinesHash,machineKeyHash) + 1
	if prevMachineIndex >= len(hashRing.machineTuples):
		prevMachineIndex = 0
	prevMachineIndex = hashRing.machineTuples[prevMachineIndex]['index']

	if prevMachineIndex in hashRing.objects:
		for key in list(hashRing.objects[prevMachineIndex]):
			if objects[key].hash < machineKeyHash:
				hashRing.removeObjectFromMachine(key,prevMachineIndex)
				hashRing.addObjectToMachine(key,machineIndex)
				print "Key: %s moved from %s to machine %s"%(key,prevMachineIndex,machineIndex)
				objects[key].updateMachine(machineIndex)

def runScan(hashRing):

	while 1:
		command = raw_input().split()
		if command[0] == 'exit':
			exit(0)
		elif command[0] == 'new':
			machineIndex = hashRing.addMachine()
			remapObjectsOnMachineInsert(hashRing,machineIndex)
		elif command[0] == 'del':
			try:
				machineIndex = int(command[1])
			except:
				print 'Machine index not entered or not an integer....'
				continue
			if hashRing.removeMachine(machineIndex):
				remapObjectsOnMachineDelete(hashRing,machineIndex)
			else:
				print 'Machine not Found....'
		elif command[0] == 'add':
		  	try:
				key = command[1]
			except:
			 	print 'Enter KeyName also....'
			 	continue
			machineIndex = hashRing.getMachine(key)
			if machineIndex == -1:
			 	print 'No Machines Found....'
			else:
				objects[key] = Object(key,machineIndex)
				print objects[key].hash,objects[key].machine
		else:
			print 'Bad Input....'
			

if __name__ == '__main__':
	
	numMachines = input('Initial Number of Machines : ')
	numReplicas = input('Number of Replicas : ')

	hashRing = ConsistentHashRing(numMachines,numReplicas)
	hashRing.printMachines()
	runScan(hashRing)

