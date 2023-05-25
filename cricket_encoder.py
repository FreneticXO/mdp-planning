import numpy as np
import argparse
import math


parser = argparse.ArgumentParser()

parser.add_argument('--states', required = True)
parser.add_argument('--parameters', required = True)
parser.add_argument('--q', required = True)

args = parser.parse_args()



with open(args.states) as file:
    rows = file.readlines()

    S = 2 * len(rows) + 2
    A = 6

    T = np.zeros((S, A, S))
    R = np.zeros((S, A, S))

    balls = int(int(rows[0])/100)
    run = int(rows[0])%100


    print('numStates ' + str(S))
    print('numActions ' + str(A))
    print('end 0 ' + str(S-1))

    with open(args.parameters) as f:
        lines = f.readlines()
        lines = lines[1:]
        for row in rows:
            x = int(row)
            bb = int(x/100)
            rr = x%100

            
            

                #print('A')
            runs = [-1, 0, 1, 2, 3, 4, 6]
            for line in lines:

                line = line.split()
                #print(line)
                action = int(line[0])
                if action == 6:
                    action = 3
                line = line[1:]
                idx = 0
                for lin in line:
                    
                    
                    if lin == '0':
                        idx+=1
                        continue
                    lin = float(lin)

                    if rr-runs[idx] <= 0:
                        T[(bb-1)*run+ rr, action,S-1] += lin
                        R[(bb-1)*run+ rr, action,S-1] = 1
                        #print('transition ' + str((bb-1)*run + rr) + ' ' + str(action) + ' ' + str(S-1) + ' ' + str(lin) + ' 1') # WIN
                    elif idx == 0:
                        T[(bb-1)*run+ rr, action,0] += lin
                        #print('transition ' + str((bb-1)*run + rr) + ' ' + str(action) + ' 0 ' + str(lin) + ' 0') # LOSS
                    elif bb == 1:
                        T[(bb-1)*run+ rr, action,0] += lin
                        #print('transition ' + str((bb-1)*run + rr) + ' ' + str(action) + ' 0 ' + str(lin) + ' 0') # LOSS
                    elif bb%6 == 1 and (idx == 2 or idx == 4):      ############ dodgy ############
                        T[(bb-1)*run+ rr, action,(bb-2)*run + rr-runs[idx]] += lin
                        #print('transition ' + str((bb-1)*run + rr) + ' ' + str(action) + ' ' + str((bb-2)*run + rr-runs[idx]) + ' ' + str(lin) + ' 0') 
                
                    elif bb%6 == 1 or idx == 2 or idx == 4:

                        T[(bb-1)*run+ rr, action,S-1 -((bb-2)*run + rr-runs[idx])] += lin
                        
                        #print('transition ' + str((bb-1)*run + rr) + ' ' + str(action) + ' ' + str((bb-2)*run + rr-runs[idx]) + ' ' + str(lin) + ' 0') # swap strike when runs 1 or 3
                    else:

                        T[(bb-1)*run+ rr, action,(bb-2)*run + rr-runs[idx]] += lin
                        #print('transition ' + str((bb-1)*run + rr) + ' ' + str(action) + ' ' + str( (bb-2)*run +rr-runs[idx] ) + ' ' + str(lin) + ' 0') # GAME IN PROGRESS
                    idx += 1



                # 5 is the only action of B

                #print('B')

            runs = [-1, 0, 1]

            idx = 0

            q = float(args.q)

            if rr == 1 and bb == 1:

                T[S-1 - (bb-1)*run - rr, 5 ,S-1] += (1-q)/2
                T[S-1 - (bb-1)*run - rr, 5, 0] += 1-(1-q)/2
                R[S-1 - (bb-1)*run - rr, 5 ,S-1] = 1
                #print('transition ' + str(S-2 - (bb-1)*run - rr) + ' 5 ' + str(S-1) + ' ' + str((1-q)/2) + ' 1') # WIN
                #print('transition ' + str(S-2 - (bb-1)*run - rr) + ' 5 0 ' + str(1 - (1-q)/2) + ' 0') # LOSE

            elif rr == 1:
                T[S-1 - (bb-1)*run - rr, 5 ,S-1] += (1-q)/2
                T[S-1 - (bb-1)*run - rr, 5 ,S-1 - (bb-2)*run - rr] += (1-q)/2
                T[S-1 - (bb-1)*run - rr, 5 , 0] += q
                R[S-1 - (bb-1)*run - rr, 5 ,S-1] = 1

                #print('transition ' + str(S-2 - (bb-1)*run - rr) + ' 5 ' + str(S-1) + ' ' + str((1-q)/2) + ' 1') # WIN
            
                #print('transition ' + str(S-2 - (bb-1)*run - rr) + ' 5 ' + str(S-2 - (bb-2)*run - rr) + ' ' + str((1-q)/2) + ' 0')

                #print('transition ' + str(S-2 - (bb-1)*run - rr) + ' 5 0 ' + str(q) + ' 0') 
            
            elif bb == 1:
                T[S-1 - (bb-1)*run - rr, 5 ,0] += 1
                #print('transistion ' + str(S-2 - (bb-1)*run - rr) + ' 5 0 0')
            elif bb%6 != 1:

                T[S-1 - (bb-1)*run - rr, 5 ,S-1 - (bb-2)*run - rr] += (1-q)/2
                T[S-1 - (bb-1)*run - rr, 5 ,0] += q
                T[S-1 - (bb-1)*run - rr, 5 ,(bb-2)*run  + rr-1] += (1-q)/2

                #print('transition ' + str(S-2 - (bb-1)*run - rr) + ' 5 ' + str(S-2 - (bb-2)*run - rr) + ' ' + str((1-q)/2) + ' 0')
                #print('transition ' + str(S-2 - (bb-1)*run - rr) + ' 5 0 ' + str(q) + ' 0')
                #print('transition ' + str(S-2 - (bb-1)*run - rr) + ' 5 ' + str((bb-2)*run  + rr-1) + ' ' + str((1-q)/2) + ' 0')
            else:

                T[S-1 - (bb-1)*run - rr, 5 ,S-1 - (bb-2)*run - rr+1] += (1-q)/2
                T[S-1 - (bb-1)*run - rr, 5 ,0] += q
                T[S-1 - (bb-1)*run - rr, 5 ,(bb-2)*run + rr] += (1-q)/2

                #print('transition ' + str(S-2 - (bb-1)*run - rr) + ' 5 ' + str((bb-2)*run + rr) + ' ' + str((1-q)/2) + ' 0') #dot ball
                
                #print('transition ' + str(S-2 - (bb-1)*run - rr) + ' 5 ' + str(S-2 - (bb-2)*run - rr+1) + ' ' + str((1-q)/2) + ' 0') #1 run
                #print('transition ' + str(S-2 - (bb-1)*run - rr) + ' 5 0 ' + str(q) + ' 0') #out loss
        
    #print(T)

    for s in range(S):
        for a in range(A):
            for s_ in range(S):
                if T[s, a, s_] != 0:
                    print('transition ' + str(s) + ' ' + str(a) + ' ' + str(s_) + ' ' + str(R[s, a, s_]) + ' ' + str(T[s, a, s_]))

                
print('mdptype episodic')
print('discount 1')