from math import floor

def part1_fuel_math(x):
    tmp = floor((x/3)) - 2
    if tmp < 0:
        return 0
    return int(tmp)


def part1_main():
    with open('inputs.txt', 'r') as f:
        module_weights = f.readlines()
    
    fuel_reqs = [part1_fuel_math(int(x)) for x in module_weights]
    return sum(fuel_reqs)


def part2_fuel_math(x):
    fr = part1_fuel_math(x)
    if fr <= 0:
        # stopping condition
        return 0
    else:
        # recursion
        return (fr + part2_fuel_math(fr))
    

def part2_main():
    with open("inputs.txt", 'r') as f:
        module_weights = f.readlines()
        fuel_reqs = [part2_fuel_math(int(x)) for x in module_weights]

    return sum(fuel_reqs)
