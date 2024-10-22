import copy

def read_netlist(filename):
    netlist = []
    flip_flops = []
    
    with open(filename, 'r') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            parts = line.split()
            gate_type = parts[0]
            
            if gate_type.startswith('dff'):
                flip_flops.append(parts)  # Store flip-flop information
            else:
                netlist.append(parts)
    
    return netlist, flip_flops


def remove_flip_flops_and_reverse(netlist, flip_flops):
    # Prepare lists for pseudo inputs and outputs
    pseudo_inputs = []
    pseudo_outputs = []
    input_mapping = {}
    output_mapping = {}

    pseudo_input_index = 1
    pseudo_output_index = 1

    # Loop through flip-flops to generate pseudo mappings
    for flip_flop in flip_flops:
        output_node = flip_flop[1]
        input_node = flip_flop[2]

        # if 'in' in input_node or output_node:
        #     input_mapping[input_node] = f"{input_node}"
        #     output_mapping[output_node] = f"{output_node}"

        
        # Assign new pseudo outputs (which were inputs) and vice versa
        if input_node not in output_mapping:
            output_mapping[input_node] = f"pseudo_output_{pseudo_output_index}"
            pseudo_output_index += 1

        if output_node not in input_mapping:
            input_mapping[output_node] = f"pseudo_input_{pseudo_input_index}"
            pseudo_input_index += 1

        # if output_node not in output_mapping:
        #     output_mapping[output_node] = f"pseudo_output_{pseudo_output_index}"
        #     pseudo_output_index += 1

        # if input_node not in input_mapping:
        #     input_mapping[input_node] = f"pseudo_input_{pseudo_input_index}"
        #     pseudo_input_index += 1
        
    # Now replace the inputs and outputs in the netlist
    modified_netlist = []
    for line in netlist:
        new_line = copy.deepcopy(line)
        
        # Replace nodes in the line if they are mapped to pseudo inputs/outputs
        for i in range(1, len(line)):
            if line[i] in input_mapping:
                new_line[i] = input_mapping[line[i]]
            elif line[i] in output_mapping:
                new_line[i] = output_mapping[line[i]]
        
        modified_netlist.append(new_line)
    
    return modified_netlist, input_mapping, output_mapping


def write_netlist(filename, netlist, input_mapping, output_mapping):
    with open(filename, 'w') as f:
        f.write('# Modified combinational netlist (with reversed pseudo inputs/outputs)\n')
        
        # Write the modified netlist
        for line in netlist:
            f.write(' '.join(line) + '\n')
        
        # Write the pseudo primary inputs and outputs (reversed)
        # f.write('\n# Pseudo Primary Outputs (from inputs): {}\n'.format(', '.join(output_mapping.values())))
        # f.write('# Pseudo Primary Inputs (from outputs): {}\n'.format(', '.join(input_mapping.values())))


def main(input_filename, output_filename):
    # Read the original netlist
    netlist, flip_flops = read_netlist(input_filename)
    
    # Remove D flip-flops and reverse pseudo inputs/outputs
    modified_netlist, input_mapping, output_mapping = remove_flip_flops_and_reverse(netlist, flip_flops)
    
    # Write the new netlist to the output file
    write_netlist(output_filename, modified_netlist, input_mapping, output_mapping)


# Usage
input_filename = 'sequential_netlist.txt'
output_filename = 'without_dff.txt'

main(input_filename, output_filename)
