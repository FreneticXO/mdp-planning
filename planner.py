import argparse
import numpy as np
from pulp import *
import random
import math


parser = argparse.ArgumentParser()

parser.add_argument('--mdp', required = True)
parser.add_argument('--algorithm')
parser.add_argument('--policy')

args = parser.parse_args()

def storeMDP(mdpPath):
    with open(mdpPath) as file:
        rows = file.readlines()

    num_S = int(rows[0].split()[1])
    num_A = int(rows[1].split()[1])
    end = [int(ending) for ending in rows[2].split()[1:]] # end is an array

    T = np.zeros((num_S, num_A, num_S))
    R = np.zeros((num_S, num_A, num_S))


    discount = float(rows[-1].split()[1])
    typ = rows[-2].split()[1]
    
    for row in rows[3:]:

        if row.split()[0] == 'transition':
            row = row.split()
            s = int(row[1])
            a = int(row[2])
            s_ = int(row[3])
            rew = float(row[4])
            p = float(row[5])



            T[s, a, s_] = p
            R[s, a, s_] = rew



    return num_S, num_A, T, R, end, typ, discount


def valueIteration(S, A, T, R, discount):

    V = np.random.uniform(0, 1, S)
    V_ = np.random.uniform(0, 1, S)*0.5
    pi = np.zeros(S)

    while np.linalg.norm(V-V_) > 1e-9:
        V_ = V.copy()

        for s in range(S):
            max_val = 0
            actions = []
            for a in range(A):
                curr_sum = 0
                for s_ in range(S):
                    p = T[s, a, s_]

                    curr_sum += p*(R[s, a, s_] + discount * V[s_])
                actions.append(curr_sum)
                max_val = max(max_val, curr_sum)
            V[s] = max_val
            pi[s] = int(np.argmax(actions))

    ppi = pi.astype(int)
    return V, ppi

def LinearProgramming(S, A, T, R, discount):

    problem = LpProblem('MDP', LpMinimize)
    V = LpVariable.dicts('V',list(range(S)))

    problem += lpSum([V[s] for s in range(S)])
    pi = np.zeros(S)

    for s in range(S):
        for a in range(A):
            exp = 0
            for s_ in range(S):
                if T[s, a, s_] != 0:
                    exp += T[s, a, s_]*(R[s, a, s_] + discount*V[s_])
            problem += lpSum([exp])<=V[s]


    problem.solve(PULP_CBC_CMD(msg=0))
    for s in range(S):
        V[s] = pulp.value(V[s])
    V = np.array(list(V.values()), dtype=float)

    for s in range(S):
        actions = []
        for a in range(A):
            exp = 0
            for s_ in range(S):
                exp += T[s, a, s_]*(R[s, a, s_]  + discount*V[s_])
            actions.append(exp)
        pi[s] = np.argmax(actions)

    ppi = pi.astype(int)

    return V, ppi


def PolicyIteration(S, A, T, R, discount):

    V = np.zeros(S)
    pi = np.zeros(S)

    prev_policy = np.zeros(S)
    policy = [0 for s in range(S)]



    change = True

    while change:
        count = 0
        change = False

        for s in range(S):
            V[s] = sum([T[s,policy[s],s_] * (R[s,policy[s],s_] + discount*V[s_]) for s_ in range(S)])
        
        
        for s in range(S):
            best = V[s]
            for a in range(A):
                what = sum([T[s, a, s_] * (R[s, a, s_] + discount*V[s_]) for s_ in range(S)])
                if what > best:
                    count += 1
                    change = True
                    policy[s] = a
                    best = what        
    return V, policy

def calcPolicy(policyPath, S):

    policy = []

    with open(policyPath) as file:
        rows = file.readlines()


    for row in rows:
        policy.append(int(row))


    return policy


def PolicyEvaluation(S, A, T, R, discount, policy):

    policy = calcPolicy(policy, S)
    V = np.zeros(S)

    while True:
        delta = 0
        for s in range(S):
            v = 0
            a = policy[s]
            for s_ in range(S):
                
                v += T[s, a, s_] * (R[s, a, s_] + discount * V[s_])
            delta = max(delta, np.abs(v-V[s]))
            V[s] = v

        if delta < 1e-8:
            break

    return V, policy
if __name__ == '__main__':
    mdpPath = args.mdp

    S, A, T, R, end, mdp_type, discount = storeMDP(mdpPath)
    #print(valueIteration(S, A, T, R, discount))

    if  args.policy:
        polPath = args.policy
        V, pi = PolicyEvaluation(S, A, T, R, discount, polPath)

    elif args.algorithm:

        if args.algorithm == 'vi':
            V, pi = valueIteration(S, A, T, R, discount)
        elif args.algorithm == 'lp':
            V, pi = LinearProgramming(S, A, T, R, discount)
        elif args.algorithm == 'hpi':
            V, pi = PolicyIteration(S, A, T, R, discount)
    else:
        V, pi = LinearProgramming(S, A, T, R, discount)

    for s in range(S):
        print("{0:6f}".format(V[s]), pi[s])


