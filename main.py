import numpy as np
import sys
import circuit


def main():

    circ = circuit.qcircuit(3)
    circ.insert_gate_at('H', 0, [-1], [0])
    circ.insert_gate_at('TF', 1, [0,1], [2])
    circ.print_circuit()

    qcirc = circ.get_qcirc()
    qcirc=circ.decompose_toffoli(qcirc)

    

   # print(circ.check_qcircuit_identity())
    
    print("Program End")


if __name__ == "__main__":
    main()