import numpy as np
import argparse
import math

parser = argparse.ArgumentParser()

parser.add_argument('--value-policy', dest = 'value_policy', required = True)
parser.add_argument('--states', required = True)

args = parser.parse_args()


with open(args.value_policy) as file:

    rows = file.readlines()

    with open(args.states) as f:

        lines = f.readlines()

        runs = int(lines[0]) % 100

        for line in lines:

            bb = int(int(line)/100)
            rr = int(line) % 100
            val = rows[(bb-1)*runs + rr]
            val = val.split()
            if val[1] == '3':
                val[1] = '6'
            print(str(line.split()[0]) + ' ' + val[1] + ' ' + val[0])

