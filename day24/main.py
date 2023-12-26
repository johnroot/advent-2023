import os
from itertools import combinations
from sympy import Symbol
from sympy import solve_poly_system

MIN = 200000000000000
MAX = 400000000000000

with open(os.path.join(os.path.dirname(__file__), 'input.txt'), 'r') as input_file:
    hailstones = []
    for line in input_file.read().splitlines():
        pos, vel = line.split(' @ ')
        pos = tuple(int(p.strip()) for p in pos.split(','))
        vel = tuple(int(p.strip()) for p in vel.split(','))
        hailstones.append(pos + vel)

    intersections = 0
    hailstone_combinations = combinations(hailstones, r=2)
    for hailstone1, hailstone2 in hailstone_combinations:
        px1, py1, pz1, vx1, vy1, vz1 = hailstone1
        px2, py2, pz2, vx2, vy2, vz2 = hailstone2

        # I love WolframAlpha
        if vx1 * vx2 == 0:
            continue
        elif vx1 * vy2 == vy1 * vx2:
            continue

        x = (vx1*vy2*px2 - vy1*px1*vx2 + py1*vx1*vx2 - vx1*py2*vx2)/(vx1*vy2 - vy1*vx2)
        y = py1 - (vy1 * (px1 - x) / vx1)

        t1 = -(px1 - x)/vx1
        t2 = -(px2 - x)/vx2
        if t1 < 0 or t2 < 0:
            continue

        if MIN <= y <= MAX and MIN <= x <= MAX:
            intersections += 1

    print(intersections) # part 2

    # The following is entirely plagarized from https://topaz.github.io/paste/#XQAAAQBPCwAAAAAAAAA0m0pnuFI8c+qagMoNTEcTIfyUWj6FDwjYeb/2OTEpuch7ZM6w3JfTBcVQW1ku35Ks7ybi/CKFq8Xc27K4xWWdXGVKv9G8fAjoZn8OKbxv8VAsRhqHZfu9uyUOsO1MtDBf7H3AJiFefjccWDnGZlXlRvbhbpPHPKA6pndA9r39qvV8KWEoMoctrCOr0YrCiLMvGziz4EiRAvzRtr9ca8CYZbSb3kv1mVTQGRl92aaYjJI0MT6obpSuWTUtHfVTwVD6/LQGlvsmbUHqxrq5JYeLVbs8ZODdAA2i3AD6r2cLCpmtHB5nQgJ1EfEXMX30DAD6D5u8C4T3DYeaUE3A4UoideacYMpucZXeSnBTyWNmm2PF2N9ouCSdskSY3xCJHGZ5BY6S75EdIstnaGwYFZpCcvj4jijkzs5ovtmpcHEFZpewDUieQGpegwf0nPq0sQE7Z7noIgSOJXipEMS4xjxWeCt0pr8OrGPiL77pXuv24qHacVCu3cuE6AIUmRchbK0p1XQdgAC2YmXCayNI8Z8usZKiQD9W5mzzLZs7AZ49ui1UdXoOlV8RKWrwwPIM14axuOtabLmW5ftXI79w3FVb+WpMoP3WXP+xrwsmMgD8PvNh18pide+AVtUGgqVb/SD93XG6iWQ7b6qsAfmRx4m9jglU9KfNHjLkuXNik2cpDXT3RxUuoZ2RE5KhxSsnqRGp3iNvUEfOzYuba+1VW/hA+ob3TI+yD7zZ8S0Nu0zNSZx1tmaTGQOinGDwQNKuokM1cEVARF0xWGZxba9ao8ntBvWO+jOBrRSWWZJe61lx8o8bqeVVzl5xEJcR1765aVT0uhdWHq7NJXrG+ltBTMgJL2e6NQ94hPoy3EFFDHOs1sMN83SODkKdOMBW1K275fwLsLLdQkRYvHQC2D/yj6mVkfOGY3WyNCN8m9T0J4DYP5RnTgNNygZ1FflOehznnUctwOcIMnAwZoJahFSOcmLJ8HuTBdMHXbLOwkxahl4cy49iCblno9eApPdtjvMvDB4xtfeuzbyRaghc2D7sTNgTkGmSeJqsBYb1bYUJqDfXp+NKIi0XkxPdG44jm2sPiFLWDelbFyPbNV+6OL+XjRnyT/RO/YVZ0yxsze/tyBo+nIMOoz9UTZE08Lv7wJ/EgaUbs+moCG5KRhHDcmgwCjJ1glL5N8jLCtusYum5wCulFnsi8vImA2t3Ry154p/HFflEkTpQiGNyJch/lhsKUs16EbdBW9F7fahl0Pxltep1g031LDjDfSTUsGe+OtWG2nN1m/IF0oW9j0z4eTPONWvN8BxMCZ/cMTYwd1pcxRJpoSRIJvYsgb2GQtpTdpLZ6DnEClI0clrhWvcv43ifZI6mqdkwj/4H5dpU6lbN5QrK9YEu7Na+NqdbfA8G4OUm6QtB5oNbYSd/7b6WbpN3OMO/dFZJt/AgWgd+5gjHIm9l5YS43aYa+VgZDyeoLEU32vAgzssTSeG0l3ybjUVy4GQ3n6DZXHFRb9W1CT4kVvecNdNxUfgj7IhqQKGYkY7t6rDiZC0S3x4R715/wRP589FNC+EJhVPXrGMNACKJfghehjfdo26MyJGuqqXK7ndsLvsHRG2UseoDvWwAqPrpWQFip29pikdkMJFl/XddwDYdnBw90BAibjkkR2AINQeUz8LgzU9mI63aF6zk476P0m33BFuEfhZAecMYnFwuF4fahSdn79nvgGdTx0CmldhPg5ICq23gu+wjDBx+HUjQwzcpXd4CpzJJeTz0cMN2OVqwFGSVK9ChArzD/hUNlnDN6/LgFccICE68/HFSSLo6WFOl5Va2dLcrKnvT/7I8WnI=
    #Part 2 uses SymPy. We set up a system of equations that describes the intersections, and solve it.
    x = Symbol('x')
    y = Symbol('y')
    z = Symbol('z')
    vx = Symbol('vx')
    vy = Symbol('vy')
    vz = Symbol('vz')

    equations = []
    t_syms = []
    #the secret sauce is that once you have three shards to intersect, there's only one valid line
    #so we don't have to set up a huge system of equations that would take forever to solve. Just pick the first three.
    for idx, hailstone in enumerate(hailstones[:3]):
        #vx is the velocity of our throw, xv is the velocity of the shard we're trying to hit. Yes, this is a confusing naming convention.
        x0,y0,z0,xv,yv,zv = hailstone
        t = Symbol('t'+str(idx)) #remember that each intersection will have a different time, so it needs its own variable

        #(x + vx*t) is the x-coordinate of our throw, (x0 + xv*t) is the x-coordinate of the shard we're trying to hit.
        #set these equal, and subtract to get x + vx*t - x0 - xv*t = 0
        #similarly for y and z
        eqx = x + vx*t - x0 - xv*t
        eqy = y + vy*t - y0 - yv*t
        eqz = z + vz*t - z0 - zv*t

        equations.append(eqx)
        equations.append(eqy)
        equations.append(eqz)
        t_syms.append(t)

    #To my great shame, I don't really know how this works under the hood.
    result = solve_poly_system(equations,*([x,y,z,vx,vy,vz]+t_syms))
    print(result[0][0]+result[0][1]+result[0][2]) #part 2 answer