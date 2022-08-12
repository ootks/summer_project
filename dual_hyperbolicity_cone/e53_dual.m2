loadPackage("Resultants")
R = QQ[x1,x2,x3,x4,x5]

J = ideal(x1*x2*x3 + x1*x2*x4 + x1*x2*x5 + x1*x3*x4 + x1*x3*x5 + x1*x4*x5 + x2*x3*x4 + x2*x3*x5 + x2*x4*x5 + x3*x4*x5)

V = dualVariety(J, AssumeOrdinary=>true)

