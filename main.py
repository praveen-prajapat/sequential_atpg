import logging
from pathlib import Path
from logic_blocks import *
from d_alg import D_Algorithm
from itertools import chain
from multi_logic import FiveValue
from writer import TikZWriter


def main():
    # Set up logging to output to both console and a file
    log_file = Path(__file__).parent / "output_log.txt"
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ]
    )

    logging.info("Starting the circuit simulation...")

    # Inputs
    n_4, n_5, n_6, n_1, n_2, z_1, n_1_2, n_2_2, z_2, \
    n_1_3, z_3, n_2_3, n_9_44, n_8_44, n_1_4, z_4, n_2_4, n_2_4_out = [
        Line(name=name) for name in [
            "n_4", "n_5", "n_6", "n_1", "n_2", "z_1", "n_1_2", "n_2_2", 
            "z_2", "n_1_3", "z_3", "n_2_3", "n_9_44", "n_8_44", "n_1_4", 
            "z_4", "n_2_4", "n_2_4_out"
        ]
    ]

    # Intermediate lines for the second set
    n_3_1, n_3_1_, n_5_1_, n_6_1_, int1_1, int2_1, n_t_1, n_9_1, n_8_1, \
    n_2_1, n_3_2, n_3_2_, n_5_2_, n_6_2_, int1_2, n_t_2, n_9_2, n_8_2, \
    n_2_2_out, n_9_33, n_8_33, n_3_3, n_6_3_, n_5_3_, n_3_3_, int1_3, \
    int2_3, n_t_3, n_2_33, n_3_4, n_6_4_, n_5_4_, n_3_4_, int1_4, n_t_4 = [
        Line(name=name) for name in [
            "n_3_1", "n_3_1_", "n_5_1_", "n_6_1_", "int1_1", "int2_1", 
            "n_t_1", "n_9_1", "n_8_1", "n_2_1", "n_3_2", "n_3_2_", 
            "n_5_2_", "n_6_2_", "int1_2", "n_t_2", "n_9_2", "n_8_2", 
            "n_2_2_out", "n_9_33", "n_8_33", "n_3_3", "n_6_3_", 
            "n_5_3_", "n_3_3_", "int1_3", "int2_3", "n_t_3", 
            "n_2_33", "n_3_4", "n_6_4_", "n_5_4_", "n_3_4_", "int1_4", "n_t_4"
        ]
    ]



    with Network() as net:
    # First section of the circuit
        or1 = OR([n_1, n_4], n_9_1)          # or (n_9_1, n_1, n_4)
        nand1 = NAND([n_4, n_5], n_8_1)      # nand (n_8_1, n_4, n_5)
        not1 = NOT([n_1], n_3_1)             # not (n_3_1, n_1)
        not2 = NOT([n_6], n_6_1_)            # not (n_6_1_, n_6)
        not3 = NOT([n_5], n_5_1_)            # not (n_5_1_, n_5)
        not4 = NOT([n_3_1], n_3_1_)          # not (n_3_1_, n_3_1)

        and1 = AND([n_6_1_, n_5_1_], int1_1) # and (int1_1, n_6_1_, n_5_1_)
        and2 = AND([int1_1, n_3_1_], int2_1) # and (int2_1, int1_1, n_3_1_)
        not5 = NOT([int2_1], z_1)            # not (z_1, int2_1)

        not6 = NOT([n_2], n_t_1)             # not (n_t_1, n_2)
        not7 = NOT([n_t_1], n_2_1)           # not (n_2_1, n_t_1)

        # Second section of the circuit
        or2 = OR([n_1_2, n_2_1], n_9_2)      # or (n_9_2, n_1_2, n_2_1)
        nand2 = NAND([n_2_1, n_9_1], n_8_2)  # nand (n_8_2, n_2_1, n_9_1)
        not8 = NOT([n_1_2], n_3_2)           # not (n_3_2, n_1_2)
        not9 = NOT([n_8_1], n_6_2_)          # not (n_6_2_, n_8_1)
        not10 = NOT([n_9_1], n_5_2_)         # not (n_5_2_, n_9_1)
        not11 = NOT([n_3_2], n_3_2_)         # not (n_3_2_, n_3_2)

        and3 = AND([n_6_2_, n_5_2_], int1_2) # and (int1_2, n_6_2_, n_5_2_)
        and4 = AND([int1_2, n_3_2_], z_2)    # and (int2_2, int1_2, n_3_2_)
        not12 = NOT([n_2_2], n_t_2) 
        not12 = NOT([n_t_2], n_2_2_out) 

        # third iteration
        or11 = OR([n_1_3, n_2_2_out], n_9_33)          # or (n_9_1, n_1, n_4)
        nand11 = NAND([n_2_2_out, n_9_2], n_8_33)      # nand (n_8_1, n_4, n_5)
        not11 = NOT([n_1_3], n_3_3)             # not (n_3_1, n_1)
        not12 = NOT([n_8_2], n_6_3_)            # not (n_6_1_, n_6)
        not13 = NOT([n_9_2], n_5_3_)            # not (n_5_1_, n_5)
        not14 = NOT([n_3_3], n_3_3_)          # not (n_3_1_, n_3_1)

        and11 = AND([n_6_3_, n_5_3_], int1_3) # and (int1_1, n_6_1_, n_5_1_)
        and12 = AND([int1_3, n_3_3_], int2_3) # and (int2_1, int1_1, n_3_1_)
        not15 = NOT([int2_3], z_3)            # not (z_1, int2_1)

        not16 = NOT([n_2_3], n_t_3)             # not (n_t_1, n_2)
        not17 = NOT([n_t_3], n_2_33)           # not (n_2_1, n_t_1)

        # fourth
        or12 = OR([n_1_4, n_2_33], n_9_44)      # or (n_9_2, n_1_2, n_2_1)
        nand12 = NAND([n_2_33, n_9_33], n_8_44)  # nand (n_8_2, n_2_1, n_9_1)
        not18 = NOT([n_1_4], n_3_4)           # not (n_3_2, n_1_2)
        not19 = NOT([n_8_33], n_6_4_)          # not (n_6_2_, n_8_1)
        not110 = NOT([n_9_33], n_5_4_)         # not (n_5_2_, n_9_1)
        not111 = NOT([n_3_4], n_3_4_)         # not (n_3_2_, n_3_2)

        and13 = AND([n_6_4_, n_5_4_], int1_4) # and (int1_2, n_6_2_, n_5_2_)
        and14 = AND([int1_4, n_3_4_], z_4)    # and (int2_2, int1_2, n_3_2_)
        not112 = NOT([n_2_4], n_t_4) 
        not112 = NOT([n_t_4], n_2_4_out) 
            # Set up output directory
        out_path = Path(__file__).parent / "out"
        out_path.mkdir(exist_ok=True, parents=True)
        writer = TikZWriter(net)

        format_str = "{{:>{}}} - {{}}: ".format(max(len(line.name) for line in net.lines))
        sep_str = "\n" + " " * len(format_str.format("", " " * 5))

        # Iterate over all lines in the network
        for line in net.lines:
            for stuck_at in (False, True):
                sa_name = "s.a.1" if stuck_at else "s.a.0"
                if D_Algorithm(net, line, stuck_at):
                    result = format_str.format(line.name, sa_name) + sep_str.join(
                        f"{'IO'[line.is_output()]}: {line.name}, {line.value}"
                        for line in chain(net.outputs(), net.inputs())
                        if line.value != FiveValue.UNKNOWN
                    )

                    # Log result to console and file
                    logging.info(result)

                    # Write the TikZ diagram for the D-Algorithm result
                    writer.write_full(out_path / f"{line.name}_{sa_name.replace('.', '')}.tex")
                else:
                    result = format_str.format(line.name, sa_name) + "No D-algorithm assignment found."
                    
                    # Log result to console and file
                    logging.info(result)

    logging.info("Simulation completed.")


if __name__ == "__main__":
    main()