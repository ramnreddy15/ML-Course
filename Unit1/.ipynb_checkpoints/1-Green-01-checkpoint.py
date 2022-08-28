import numpy as np
file = open("./test.csv")
csvFile = np.loadtxt(file, delimiter=",", skiprows=0)
n = csvFile.shape[0]
A = np.ones((n,2))
A[:,0] = csvFile[:,0]
B = csvFile[:,1]

M = csvFile[:,0:2]
R = np.corrcoef(M, rowvar = False)[0,1]
print("R^2:",R*R)

Q, R = np.linalg.qr(A, mode='complete')
QTB = (Q.T.dot(B))
B0 =QTB[1]/R[1,1]
B1 = (QTB[0]-R[0,1]*B0)/R[0,0]
print("B0:",B0)
print("B1:",B1)

# Get complement
A[:,0] = csvFile[:,1]
B = csvFile[:,0]

Q, R = np.linalg.qr(A, mode='complete')
QTB = (Q.T.dot(B))
B0 =QTB[1]/R[1,1]
B1 = (QTB[0]-R[0,1]*B0)/R[0,0]
print("B0':",B0)
print("B1':",B1)

sig = np.cov(M, rowvar=False, bias= True)
print("xy:",sig[0][1])
print("y^2:",sig[1,1])

