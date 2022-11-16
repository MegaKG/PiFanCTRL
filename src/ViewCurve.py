import matplotlib.pyplot as plt
import json
import sys

f = open(sys.argv[1],'r')
Mapping = json.loads(f.read())['Curve']
f.close()


XS = []
YS = []

class lineEq:
    def __init__(self,LinePoints):
        self.Equations = {}

        LastX = 0
        LastY = 0
        for i in sorted(list(LinePoints.keys())):
            X,Y = (int(i),LinePoints[i])

            self.Equations[int(i)] = (X,Y,LastX,LastY)

            LastX = X
            LastY = Y

    def point(self,X):
        Key = list(self.Equations.keys())[0]
        for i in self.Equations:
            if X < i:
                Key = i
                break
                
        Dat = self.Equations[Key]
        
        M = (Dat[3]-Dat[1])/(Dat[2]-Dat[0])
        return M * (X - Dat[0]) + Dat[1]

EQ = lineEq(Mapping)

for Temperature in range(1000):
    
    Y = EQ.point(Temperature/10)

    XS.append(Temperature/10)
    YS.append(Y)

plt.plot(XS,YS)

XS = []
YS = []
for i in Mapping:
    XS.append(int(i))
    YS.append(Mapping[i])
plt.scatter(XS,YS)
plt.show()



