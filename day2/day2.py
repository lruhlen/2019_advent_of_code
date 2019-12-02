def run_program(vals):
    # Fetch consecutive blocks of 4 array vals
    block_len = 4
    max_idx = int(len(vals) / block_len)
    opcode1 = 1
    opcode2 = 2
    stopcode = 99

    for i in range(max_idx):
        start_idx = block_len * i
        end_idx = block_len * (i + 1)
        chunk = vals[start_idx: end_idx]


        op_code = chunk[0]
        input1_pos = chunk[1]
        input2_pos = chunk[2]
        output_pos = chunk[3]

        input1_val = vals[input1_pos]
        input2_val = vals[input2_pos]

        if op_code == opcode1:
            vals[output_pos] = input1_val + input2_val
        elif op_code == opcode2:
            vals[output_pos] = input1_val * input2_val
        elif op_code == stopcode:
            #print("Done!")
            break
        else:
            #print("Error! Aborting")
            break

    # Program output 'stored' at the head of the array.
    return vals[0]


def get_program():
    with open("inputs.txt", 'r') as f:
        vals = f.readline().split(',')
        vals = [int(x.strip()) for x in vals]

    return vals


def gridsearch_inputs():
    target_output = 19690720
    original_program = get_program()
    
    # Some loop goes here
    for n in range(100):
        for v in range(100):
            vals = original_program.copy()
            vals[1] = n
            vals[2] = v
            result = run_program(vals)
            if result == target_output:
                return (n, v)

    return "Error! No answer found"


