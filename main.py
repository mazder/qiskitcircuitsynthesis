import numpy as np
import sys
import circuit
from qiskit import *
from qiskit import QuantumCircuit

def main():

    circ = circuit.qcircuit(3)
    #circ.insert_gate_at('H', 0, [-1], [0])
    #circ.insert_gate_at('H', 0, [-1], [0])
    #circ.insert_gate_at('TF', 1, [0,1], [2])
    #circ.print_circuit()
    #qcirc = circ.get_qcirc()
    #qcirc.qasm(formatted = True)

    #qcirc=circ.decompose_toffoli(qcirc)
    #print(circ.check_qcircuit_identity())

    #circ.write_qasm_circuit('circuit.qasm')

    #mycirc = circuit.qcircuit(0)
    #qcirc = circ.read_qasm_circuit('tt.qasm')
    #qcirc.qasm(formatted = True)

    qcirc = circ.read_qasm_circuit('id4.qasm')
    qcirc.qasm(formatted = True)
    qcirc.draw(output='mpl', filename='id4.png')
    print(circ.check_identity(qcirc))


    print("Program End")


if __name__ == "__main__":
    main()
