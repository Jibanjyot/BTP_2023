
# resistance define
r_ab = 1
r_bd  = 2
r_ac = 2
r_cd = 1
r_bc = 3

# initialization loop 1
q_ab1 = 60
q_ac1 = -40
q_bc1 = 15
q1 = [q_ab1,q_ac1,q_bc1]
r1 = [r_ab,r_ac,r_bc]

# initialization loop 2
q_bc2 = -15
q_bd2 = 20
q_cd2 = -55
q2 = [q_bc2,q_bd2,q_cd2]
r2 = [r_bc,r_bd,r_cd]

while True:
    sum11 = 0
    sum12 = 0
    for i in range(len(q1)):
        sum11 = sum11 + r1[i]*abs(q1[i])*q1[i]
        sum12 = sum12 + 2*r1[i]*abs(q1[i])

    print(sum11,sum12)
    dq1 = sum11/sum12
    print(dq1)

    sum21 = 0
    sum22 = 0
    for i in range(len(q2)):
        sum21 = sum21 + r2[i]*abs(q2[i])*q2[i]
        sum22 = sum22 + 2*r2[i]*abs(q2[i])
    
    dq2 = sum21/sum22
    print(dq2)
    q_ab1 = q_ab1 - dq1
    q_ac1 = q_ac1 - dq1
    q_bc1 = q_bc1 - (dq1 - dq2)
    q_bc2 = q_bc2 - (dq2 - dq1)
    q_bd2 = q_bd2 - dq2
    q_cd2 = q_cd2 - dq2

    q1 = [q_ab1,q_ac1,q_bc1]
    q2 = [q_bc2,q_bd2,q_cd2]
    # break
    if dq1 < 1e-6 and dq2 <1e-6:
        break


print(q1)
print(q2)















