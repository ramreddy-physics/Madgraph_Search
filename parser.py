# Stores events in events[i][j][k]. i = event #, j = particle #, k = particle attributes 
import numpy as np
import random

#open the simulated data file and read the relevant observable momenta into a csv file to be imported into python

with open("unweighted_events.lhe", "r") as f:
    search = f.readlines()

global events

events = []

cnt = 0

m = 0

for i, line in enumerate(search):

    if "<event>" in line and cnt < 600000:
      n = 0
      m += 1      
      events.append([])
      j = i + 2 # Skip 2 lines from "<event>"

      while "<mgrwt>" not in search[j]:
        n += 1
        events[m-1].append([])
        b = search[j].split()
        for k in range(len(b)):
           events[m-1][n-1].append(float(b[k]))
        j += 1
      cnt = cnt + 1

## Relevant HEP functions for transforming the observables

def Get4mom(a): return np.array([a[9],a[6],a[7],a[8]])
def Fourdot(P1,P2): return P1[0]*P2[0]-P1[1]*P2[1]-P1[2]*P2[2]-P1[3]*P2[3]
def MomSq(P): return Fourdot(P,P)
def InvMass(P): return np.sqrt(MomSq(P))

def Getmij(a, b) : return MomSq(a + b)

##Reading out the momenta for further transformations

phasespace = []
for i in range(len(events)):
  for j in range(len(events[i])):
    if events[i][j][0] == -11.0:
      temp1 = events[i][j]
    elif events[i][j][0] == 11.0:
      temp2 = events[i][j]
  phasespace.append([temp1, temp2])
    
  
#phasespace is (e+, e-)

momenta = []
for i in range(len(phasespace)):
  momenta.append([Get4mom(phasespace[i][0]), Get4mom(phasespace[i][1])])

#coin toss assignment of 1 and 2: only to be implemented when particles have combinatorial ambiguity

#Explicitly picking px, py, pz. For complicated models, you must pick transformations given by the HEP functions. For example when the mass gaps are too small.

phasespace2 = []
for i in range(len(momenta)):
  phasespace2.append([ momenta[i][0][1], momenta[i][0][2], momenta[i][0][3], momenta[i][1][1], momenta[i][1][2], momenta[i][1][3]])


from numpy import savetxt
savetxt('sig.csv', phasespace2, delimiter=',')