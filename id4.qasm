OPENQASM 2.0;
include "qelib1.inc";
qreg q[2];
t q[0];
cx q[0],q[1];
tdg q[0];
cx q[0],q[1];