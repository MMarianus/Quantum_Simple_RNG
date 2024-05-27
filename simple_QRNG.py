from qiskit import transpile
from qiskit import QuantumCircuit, ClassicalRegister, QuantumRegister
from qiskit_aer import Aer
from qiskit_ibm_runtime import QiskitRuntimeService

def RNG(quantum = False):
    # Create a quantum circuit with one qubit and one classical bit
    control = QuantumCircuit(1, 1)
    
    # Apply gate to put the qubit in superposition
    control.h(0)
    
    # Measure the qubit and store the result in the classical bit
    control.measure(0, 0)
    
    if quantum == True:
      # Use the Quantum Computer for executing the RNG
      backend = load_ibm_account()
    else:
      # Use the QASM simulator for executing the RNG
      backend = Aer.get_backend("qasm_simulator")
    
    # Transpile the circuit for the simulator
    qctr = transpile(control, backend)
    
    # Execute the circuit with one shot
    job = backend.run(qctr,shots = 1)
    
    # Get the result of the execution
    result = job.result()
    
    # Get the counts (number of times each result was observed)
    counts = result.get_counts()
    
    # Extract the result bit from the results
    random_int = int(list(counts.keys())[0])
    
    return random_int

def load_ibm_account():
  # Connect to IBM API Service
  service = QiskitRuntimeService(
    channel='ibm_quantum',
    instance='ibm-q/open/main',
    token='<IBM-Token-Goes-Here>'   # Place your IBM API service key here, or use the quantum simulator instead
  )

  # Retrieve the least busy backend that supports the desired number of qubits
  backends = service.backends(
      filters=lambda x: x.configuration().n_qubits >= 5 and 
                        not x.configuration().simulator and x.status().operational
  )
    
  # Select the least busy quantyum backend
  backend = min(backends, key=lambda b: b.status().pending_jobs)
  return backend

if __name__ == "__main__":
  # Run and print 10 times the RNG
  for x in range(10):
    print(RNG(True))      #Change to False to use the Quantum Simulator for QRNGs
