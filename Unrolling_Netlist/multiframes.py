import copy

def read_netlist_from_file(filename):
    netlist = []
    pseudo_inputs = set()  # Use set to avoid duplicates
    pseudo_outputs = set()

    with open(filename, 'r') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue

            parts = line.split()

            # Parse gate definitions and extract inputs and outputs
            gate_name = parts[0]
            gate_output = parts[1]  # The first node after the gate is the output
            gate_inputs = parts[2:]  # All other nodes after the output are inputs

            # Store the netlist parts
            netlist.append(parts)

            # Check if the gate output is a pseudo output
            if 'pseudo_output' in gate_output:
                pseudo_outputs.add(gate_output)

            # Check if any gate input is a pseudo input
            for gate_input in gate_inputs:
                if 'pseudo_input' in gate_input:
                    pseudo_inputs.add(gate_input)

    return netlist, list(pseudo_inputs), list(pseudo_outputs)



# def replicate_netlist(netlist, pseudo_inputs, pseudo_outputs, timeframes=4):
#     replicated_netlist = []
#     last_pseudo_connections = {}

#     # Keep track of pseudo inputs and outputs for each timeframe
#     first_pseudo_inputs = copy.deepcopy(pseudo_inputs)
#     last_pseudo_outputs = copy.deepcopy(pseudo_outputs)

#     for t in range(timeframes):
#         current_netlist = []

#         # For intermediate timeframes, combine pseudo outputs from t-1 with pseudo inputs of t
#         if t > 0:
#             # print(t)
#             if t == timeframes - 1:
#                 # For the last timeframe, retain original pseudo outputs
#                 last_pseudo_connections = {output: f"{output}_t{t}" for output in pseudo_outputs}
#             else:
#                 print(len(pseudo_inputs))
#                 # Combine pseudo outputs of t-1 with pseudo inputs of t
#                 for i in range(len(pseudo_inputs)):
#                     combined_name = f"pseudo_int_t{t-1}_t{t}_{i+1}"
#                     last_pseudo_connections[pseudo_outputs[i]] = combined_name
#                     pseudo_inputs[i] = combined_name  # Update pseudo inputs to use combined names

#         # Replicate gates for the current timeframe
#         for line in netlist:
#             new_line = copy.deepcopy(line)

#             # Update gate name to include timeframe
#             new_line[0] = f"{new_line[0]}_t{t}"

#             # Update node names in the line to include timeframe or carry forward pseudo connections
#             for i in range(1, len(new_line)):
#                 node = new_line[i]

#                 if node in last_pseudo_connections:
#                     new_line[i] = last_pseudo_connections[node]
#                 else:
#                     new_line[i] = f"{node}_t{t}"

#             current_netlist.append(new_line)

#         replicated_netlist.extend(current_netlist)

#         # Update the last pseudo outputs for this timeframe to use in the next timeframe
#         last_pseudo_outputs = [f"{output}_t{t}" for output in pseudo_outputs]

#     return replicated_netlist, first_pseudo_inputs, last_pseudo_outputs


def replicate_netlist(netlist, pseudo_inputs, pseudo_outputs, timeframes=4):
    replicated_netlist = []
    last_pseudo_connections = {}
    first_pseudo_connections = {}

    # Keep track of pseudo inputs and outputs for each timeframe
    first_pseudo_inputs = copy.deepcopy(pseudo_inputs)
    last_pseudo_outputs = copy.deepcopy(pseudo_outputs)

    for t in range(timeframes):
        current_netlist = []

        # For intermediate timeframes, combine pseudo outputs from t-1 with pseudo inputs of t
        if t >= 0:
            # Handle pseudo inputs and outputs correctly for each intermediate timeframe
            new_pseudo_inputs = []
            if t==0:
                # print(min(len(pseudo_inputs), len(pseudo_outputs)))
                first_pseudo_connections = {input: f"{input}_t{t}" for input in pseudo_inputs}
                for i in range(min(len(pseudo_inputs), len(pseudo_outputs))):
                    combined_name = f"pseudo_int_t{t}_t{t+1}_{i+1}"
                    first_pseudo_connections[pseudo_outputs[i]] = combined_name

            elif t == timeframes - 1:
                # For the last timeframe, retain original pseudo outputs
                last_pseudo_connections = {output: f"{output}_t{t}" for output in pseudo_outputs}
            else:
                # Combine pseudo outputs of t-1 with pseudo inputs of t
                for i in range(min(len(pseudo_inputs), len(pseudo_outputs))):
                    combined_name = f"pseudo_int_t{t}_t{t+1}_{i+1}"
                    last_pseudo_connections[pseudo_outputs[i]] = combined_name
                    # new_pseudo_inputs.append(combined_name)  # Store updated pseudo inputs for this timeframe

                    combined_name_ip = f"pseudo_int_t{t-1}_t{t}_{i+1}"
                    first_pseudo_connections[pseudo_inputs[i]] = combined_name_ip
                    new_pseudo_inputs.append(combined_name_ip) 
            # pseudo_inputs = new_pseudo_inputs  # Update pseudo inputs for the next timeframe

        # Replicate gates for the current timeframe
        for line in netlist:
            new_line = copy.deepcopy(line)

            # Update gate name to include timeframe
            new_line[0] = f"{new_line[0]}_t{t}"

            # Update node names in the line to include timeframe or carry forward pseudo connections
            for i in range(1, len(new_line)):
                node = new_line[i]

                if node in last_pseudo_connections:
                    new_line[i] = last_pseudo_connections[node]
                elif node in first_pseudo_connections:
                    new_line[i] = first_pseudo_connections[node]
                else:
                    new_line[i] = f"{node}_t{t}"

            current_netlist.append(new_line)

        replicated_netlist.extend(current_netlist)

        # Update the last pseudo outputs for this timeframe to use in the next timeframe
        last_pseudo_outputs = [f"{output}_t{t}" for output in pseudo_outputs]
        first_pseudo_inputs = [f"{input}_t{t}" for input in pseudo_inputs]

    return replicated_netlist, first_pseudo_inputs, last_pseudo_outputs



def write_replicated_netlist(filename, replicated_netlist, first_pseudo_inputs, last_pseudo_outputs):
    with open(filename, 'w') as f:
        f.write('# Replicated combinational netlist with timeframes\n')
        
        # Write the modified netlist
        for line in replicated_netlist:
            f.write(' '.join(line) + '\n')
        
        # Write the first timeframe pseudo inputs and last timeframe pseudo outputs
        f.write('\n# First Timeframe Pseudo Inputs: {}\n'.format(', '.join(first_pseudo_inputs)))
        f.write('# Last Timeframe Pseudo Outputs: {}\n'.format(', '.join(last_pseudo_outputs)))


def main(input_filename, output_filename):
    # Read netlist from text file
    netlist, pseudo_inputs, pseudo_outputs = read_netlist_from_file(input_filename)

    # Replicate the netlist for 4 timeframes
    replicated_netlist, first_pseudo_inputs, last_pseudo_outputs = replicate_netlist(netlist, pseudo_inputs, pseudo_outputs, timeframes=4)

    # Write the replicated netlist to the output file
    write_replicated_netlist(output_filename, replicated_netlist, first_pseudo_inputs, last_pseudo_outputs)


# Usage
input_filename = 'without_dff.txt'  # Provide your text file here
output_filename = 'replicated_netlist.txt'

main(input_filename, output_filename)
