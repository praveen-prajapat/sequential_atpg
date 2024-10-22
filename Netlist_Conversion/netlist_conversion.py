def parse_netlist(netlist):
    gates = []
    for line in netlist.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue

        parts = line.split()
        gate_type = parts[0][:-3]  # Remove '_tx' where x is the timeframe number
        output_node = parts[1]
        input_nodes = parts[2:]
        
        if gate_type.startswith("not"):
            gates.append(f"not{parts[0][-1]} = NOT([{input_nodes[0]}], {output_node})")
        elif gate_type.startswith("nand"):
            gates.append(f"nand{parts[0][-1]} = NAND([{', '.join(input_nodes)}], {output_node})")
        elif gate_type.startswith("or"):
            gates.append(f"or{parts[0][-1]} = OR([{', '.join(input_nodes)}], {output_node})")
        elif gate_type.startswith("and"):
            gates.append(f"and{parts[0][-1]} = AND([{', '.join(input_nodes)}], {output_node})")
    
    return gates

def format_output(gates):
    formatted_circuit = []
    current_section = 1
    for i, gate in enumerate(gates):
        if i > 0 and i % 10 == 0:  # Adjust section size if necessary
            current_section += 1
        if i % 10 == 0:
            formatted_circuit.append(f"# Section {current_section}\n")
        formatted_circuit.append(f"    {gate}")
    
    return "\n".join(formatted_circuit)

def convert_netlist_from_file(input_file, output_file):
    # Read the netlist from a file
    with open(input_file, 'r') as file:
        netlist = file.read()

    # Parse and format the netlist
    gates = parse_netlist(netlist)
    formatted_netlist = format_output(gates)

    # Write the formatted netlist to the output file
    with open(output_file, 'w') as file:
        file.write(formatted_netlist)

    print(f"Netlist successfully converted and saved to {output_file}")

# Usage
input_file = 'netlist.txt'  # Input .txt file containing the netlist
output_file = 'formatted_netlist.txt'  # Output file to save the formatted netlist
convert_netlist_from_file(input_file, output_file)
