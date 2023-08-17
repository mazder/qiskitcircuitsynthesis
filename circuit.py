import numpy as np
import sys
from qiskit import *
from qiskit import *

#import matplotlib inline
#https://qiskit.org/documentation/_modules/qiskit/circuit/quantumcircuit.html
# Import Aer
from qiskit import Aer
from qiskit.quantum_info.operators import Operator, Pauli
from qiskit import QuantumRegister, ClassicalRegister, QuantumCircuit
from qiskit.visualization import plot_histogram
from qiskit.visualization import plot_state_city

#from qiskit.dagcircuit import DAGCircuit
from qiskit.converters import circuit_to_dag


class qcircuit:

    def __init__(self, n):
        self.controls = []
        self.target = []
        self.gate = []
        self.qcirc = QuantumCircuit(n)

    #return qiskit circuit
    def get_qcirc(self):
        return self.qcirc

    #insert gate at position pos
    def insert_gate_at(self, gate, pos, ct, t):
        self.controls.insert(pos, ct)
        self.target.insert(pos, t)
        #print (self.controls)
        #print (self.target)
        if(gate == 'H'):
            self.gate.insert(pos, 'H')
            self.qcirc.h(t[0])
        if(gate == 'TF'):
            self.gate.insert(pos, 'T')
            self.qcirc.ccx(ct[0], ct[1], t[0])

    #qiskit Circuit is written into circuit.png
    def print_circuit(self):
        print("Qiskit Circuit is written into circuit.png")
        self.qcirc.draw(output='mpl', filename='circuit.png')

    #return a vector of qubits index
    def find_qubits(self):
        dag = circuit_to_dag(self.qcirc)
        qubits = [qubit.index for qubit in self.qcirc.qubits]
        return qubits

    #return a vector of active qubits index
    def find_active_qubits(self):
        dag = circuit_to_dag(self.qcirc)
        active_qubits = [qubit.index for qubit in self.qcirc.qubits
                            if qubit not in dag.idle_wires()]
        return active_qubits

    #return a vector of ancilla qubits index
    def find_ancilla_qubits(self):
        dag = circuit_to_dag(self.qcirc)
        ancilla_qubits = [qubit.index for qubit in self.qcirc.qubits
                            if qubit in dag.idle_wires()]
        return ancilla_qubits

    #return true if two qcirc are equivalent
    def check_qcirc_equivalent(self, qcirc_a, qcirc_b):
        au = Operator(qcirc_a)
        bu = Operator(qcirc_b)
        #print(au)
        #print(bu)
        return au.dim == bu.dim and np.allclose(au.data, bu.data)

    #return true if qcircuit is an identity
    def check_qcircuit_identity(self):
        qubits=self.find_qubits()
        circ_id = QuantumCircuit(len(qubits))
        return self.check_qcirc_equivalent(self.qcirc, circ_id)

    def get_inverse_quantum_toffoli(self, circ, x, y, z):
        circ.cx(x,y)
        circ.t(y)
        circ.tdg(x)
        circ.h(z)
        circ.cx(x,y)
        circ.tdg(z)
        circ.tdg(y)
        circ.cx(x,z)
        circ.t(z)
        circ.cx(y,z)
        circ.tdg(z)
        circ.cx(x,z)
        circ.t(z)
        circ.cx(y,z)
        circ.h(z)
        return circ;

    def get_reverse_quantum_toffoli(self, circ, x, y, z):
        circ.cx(x,y)
        circ.tdg(y)
        circ.t(x)
        circ.h(z)
        circ.cx(x,y)
        circ.t(z)
        circ.t(y)
        circ.cx(x,z)
        circ.tdg(z)
        circ.cx(y,z)
        circ.t(z)
        circ.cx(x,z)
        circ.tdg(z)
        circ.cx(y,z)
        circ.h(z)
        return circ;

    def get_quantum_toffoli(self, circ, x, y, z):
        circ.h(z)
        circ.cx(y,z)
        circ.tdg(z)
        circ.cx(x,z)
        circ.t(z)
        circ.cx(y,z)
        circ.tdg(z)
        circ.cx(x,z)
        circ.t(y)
        circ.t(z)
        circ.cx(x,y)
        circ.h(z)
        circ.t(x)
        circ.tdg(y)
        circ.cx(x,y)
        return circ;

    def decompose_toffoli(self, circ):
        temp_circ = QuantumCircuit(circ.num_qubits)
        for inst in circ.data:
            #for x in range(len(inst.qubits)):
                #qubit_index=circ.find_bit(inst.qubits[x]).index
                #print(qubit_index)
            controls_target = [circ.find_bit(inst.qubits[x]).index for x in range(len(inst.qubits))]
            print(controls_target)
            print(inst.operation.name)
            if(inst.operation.name=='ccx'):
                quantum_toffoli = QuantumCircuit(circ.num_qubits)
                quantum_toffoli = self.get_quantum_toffoli(quantum_toffoli, controls_target[0],controls_target[1],controls_target[2])
                temp_circ=temp_circ.compose(quantum_toffoli, qubits=quantum_toffoli.qubits)
            elif (inst.operation.name=='cx'):
                temp_circ.cx(controls_target[0],controls_target[1])
            elif (inst.operation.name=='h'):
                temp_circ.h(controls_target[0])
            elif (inst.operation.name=='t'):
                temp_circ.t(controls_target[0])
            elif (inst.operation.name=='tdg'):
                temp_circ.tdg(controls_target[0])
            else:
                sys.exit("Unrecognized gate in circuit to decompose!")
        circ=temp_circ.copy()
        print("Toffoli decomposed qiskit circuit is written into decomposedcircuit.png")
        circ.draw(output='mpl', filename='decomposedcircuit.png')
        circ.qasm(formatted = True)

        return circ

    def write_qasm_circuit(self, qcirc, filename):
        qcirc.qasm(formatted = True, filename = filename)

    def read_qasm_circuit(self, filename):
        return QuantumCircuit.from_qasm_file(filename)
