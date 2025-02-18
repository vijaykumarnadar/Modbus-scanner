import threading
from pymodbus.client import ModbusTcpClient as ModbusClient
from pymodbus.exceptions import ModbusIOException
from concurrent.futures import ThreadPoolExecutor
import time

# Configuration
MODBUS_SERVER_IP = '192.168.0.228'  # IP address of the Modbus server
MODBUS_PORT = 502  # Default Modbus TCP port
START_ADDR = 0  # Starting address to enumerate
END_ADDR = 100  # Ending address to enumerate (adjust based on your device)
MAX_THREADS = 20  # Max number of threads for parallelism
TIMEOUT = 1  # Timeout for Modbus read requests in seconds

# Modbus TCP Client Connection
client = ModbusClient(MODBUS_SERVER_IP, port=MODBUS_PORT, timeout=TIMEOUT)

# Dictionary to store results for all slaves
network_data = {}

# Function to read coils concurrently for a specific slave
def read_coils(slave_id, results):
    print(f"Reading coils for Slave ID: {slave_id}")
    for addr in range(START_ADDR, END_ADDR):
        try:
            print(f"Reading coil at address {addr} for Slave ID: {slave_id}")
            response = client.read_coils(address=addr, count=1, slave=slave_id)
            if response.isError():
                print(f"Error reading coil at address {addr} for Slave ID: {slave_id}")
            else:
                results['coils'].append((addr, response.bits[0]))
        except ModbusIOException as e:
            print(f"Modbus I/O Error reading coil at address {addr} for Slave ID: {slave_id}: {e}")

# Function to read discrete inputs concurrently for a specific slave
def read_discrete_inputs(slave_id, results):
    print(f"Reading discrete inputs for Slave ID: {slave_id}")
    for addr in range(START_ADDR, END_ADDR):
        try:
            print(f"Reading discrete input at address {addr} for Slave ID: {slave_id}")
            response = client.read_discrete_inputs(address=addr, count=1, slave=slave_id)
            if response.isError():
                print(f"Error reading discrete input at address {addr} for Slave ID: {slave_id}")
            else:
                results['discrete_inputs'].append((addr, response.bits[0]))
        except ModbusIOException as e:
            print(f"Modbus I/O Error reading discrete input at address {addr} for Slave ID: {slave_id}: {e}")

# Function to read holding registers concurrently for a specific slave
def read_holding_registers(slave_id, results):
    print(f"Reading holding registers for Slave ID: {slave_id}")
    for addr in range(START_ADDR, END_ADDR):
        try:
            print(f"Reading holding register at address {addr} for Slave ID: {slave_id}")
            response = client.read_holding_registers(address=addr, count=1, slave=slave_id)
            if response.isError():
                print(f"Error reading holding register at address {addr} for Slave ID: {slave_id}")
            else:
                results['holding_registers'].append((addr, response.registers[0]))
        except ModbusIOException as e:
            print(f"Modbus I/O Error reading holding register at address {addr} for Slave ID: {slave_id}: {e}")

# Function to read input registers concurrently for a specific slave
def read_input_registers(slave_id, results):
    print(f"Reading input registers for Slave ID: {slave_id}")
    for addr in range(START_ADDR, END_ADDR):
        try:
            print(f"Reading input register at address {addr} for Slave ID: {slave_id}")
            response = client.read_input_registers(address=addr, count=1, slave=slave_id)
            if response.isError():
                print(f"Error reading input register at address {addr} for Slave ID: {slave_id}")
            else:
                results['input_registers'].append((addr, response.registers[0]))
        except ModbusIOException as e:
            print(f"Modbus I/O Error reading input register at address {addr} for Slave ID: {slave_id}: {e}")

# Function to read Modbus data for a specific slave concurrently
def read_modbus_data(slave_id):
    print(f"Starting to read all data types for Slave ID: {slave_id}")
    results = {
        'slave_id': slave_id,
        'coils': [],
        'discrete_inputs': [],
        'holding_registers': [],
        'input_registers': []
    }

    # Create a thread pool to read coils, discrete inputs, holding registers, and input registers concurrently
    with ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
        print(f"Submitting threads to read coils, discrete inputs, holding registers, and input registers for Slave ID: {slave_id}")
        executor.submit(read_coils, slave_id, results)
        executor.submit(read_discrete_inputs, slave_id, results)
        executor.submit(read_holding_registers, slave_id, results)
        executor.submit(read_input_registers, slave_id, results)

    print(f"Completed reading all data types for Slave ID: {slave_id}")
    return results

# Function to scan a specific slave and check if it's responsive
def scan_slave(slave_id):
    print(f"Scanning Slave ID: {slave_id} to check for responsiveness...")
    try:
        # Attempt to read a simple coil (address 0) to see if the slave responds
        response = client.read_coils(address=0, count=1, slave=slave_id)
        if not response.isError():
            print(f"Slave ID: {slave_id} responded successfully. Starting data collection.")
            return read_modbus_data(slave_id)
        else:
            print(f"Error: Slave ID: {slave_id} did not respond to initial coil read.")
            return None
    except ModbusIOException as e:
        print(f"Modbus I/O Error scanning Slave ID: {slave_id}: {e}")
        return None

# Function to scan all possible slave IDs (1 to 247) and gather data from responding slaves
def scan_all_slaves():
    print(f"Starting scan for all slaves (ID 1 to 247)...")
    # Establish the connection to the Modbus server
    client.connect()
    print(f"Connection established to Modbus server at {MODBUS_SERVER_IP}:{MODBUS_PORT}")

    # Create a thread pool to scan slaves concurrently
    with ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
        futures = {executor.submit(scan_slave, slave_id): slave_id for slave_id in range(1, 248)} #248 is the maximum number of slaves

        print(f"Scanning all slaves concurrently...")
        for future in futures:
            slave_data = future.result()
            if slave_data:
                print(f"Slave ID {slave_data['slave_id']} data collected successfully.")
                network_data[slave_data['slave_id']] = slave_data
            else:
                print(f"Slave ID {futures[future]} did not respond.")

    # Close the connection once scanning is complete
    print(f"Scan complete. Closing connection to Modbus server.")
    client.close()

# Function to display the results in a structured way
def display_results():
    print("\nDisplaying results...")
    if not network_data:
        print("No slaves responded.")
        return

    for slave_id, data in network_data.items():
        print(f"Slave ID: {slave_id}")
        print("  Coils:")
        for addr, value in data['coils']:
            print(f"    Address {addr}: {value}")

        print("  Discrete Inputs:")
        for addr, value in data['discrete_inputs']:
            print(f"    Address {addr}: {value}")

        print("  Holding Registers:")
        for addr, value in data['holding_registers']:
            print(f"    Address {addr}: {value}")

        print("  Input Registers:")
        for addr, value in data['input_registers']:
            print(f"    Address {addr}: {value}")

        print("-" * 50)

# Main function to run the entire scan and display the results
def main():
    print("Starting Modbus network scan...")
    start_time = time.time()
    scan_all_slaves()  # Scan all slaves in the network
    end_time = time.time()

    print(f"\nEnumeration completed in {end_time - start_time:.2f} seconds.")
    display_results()  # Display the collected data in a structured format

if __name__ == "__main__":
    main()
