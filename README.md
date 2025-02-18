
# Modbus Scanner

This Python application performs concurrent Modbus network scanning and enumeration of multiple Modbus slaves. The script scans all potential slave devices (IDs 1 to 247) on a Modbus TCP network and collects data from different registers: coils, discrete inputs, holding registers, and input registers. The results are displayed in a structured format for further analysis.

## Features

- Scans all slave IDs (1 to 247) to detect responsive Modbus devices.
- Collects and displays data from the following types of Modbus registers:
  - Coils
  - Discrete Inputs
  - Holding Registers
  - Input Registers
- Uses Python's `ThreadPoolExecutor` to execute multiple reading operations concurrently, increasing performance.
- Handles Modbus TCP communication using the `pymodbus` library.
- Handles Modbus I/O errors gracefully.

## Requirements

- Python 3.7+
- `pymodbus` library

You can install the required dependencies with:

```bash
pip install pymodbus
```

## Configuration

Modify the following constants in the script to suit your network configuration:

- `MODBUS_SERVER_IP`: IP address of the Modbus server.
- `MODBUS_PORT`: Modbus TCP port (default is 502).
- `START_ADDR`: Starting address for enumeration.
- `END_ADDR`: Ending address for enumeration.
- `MAX_THREADS`: Maximum number of threads to use for concurrent operations.
- `TIMEOUT`: Timeout in seconds for Modbus read requests.

## Usage

Run the script by executing the following command:

```bash
python modbus_scanner.py
```

This will start scanning all possible slave IDs and collect data for any responding devices. Once the scan is complete, the results will be printed to the console.

### Example Output

```text
Scan complete. Closing connection to Modbus server.

Enumeration completed in 68.64 seconds.

Displaying results...
Slave ID: 10
  Coils:
    Address 0: False
    Address 1: False
    Address 2: True
    Address 3: False
    Address 4: False
    Address 5: False
    Address 6: False
    Address 7: False
    Address 8: False
    Address 9: False
  Discrete Inputs:
    Address 0: False
    Address 1: False
    Address 2: True
    Address 3: False
    Address 4: False
    Address 5: False
    Address 6: False
    Address 7: False
    Address 8: False
    Address 9: False
  Holding Registers:
    Address 0: 0
    Address 1: 0
    Address 2: 0
    Address 3: 0
    Address 4: 0
    Address 5: 10101
    Address 6: 0
    Address 7: 0
    Address 8: 0
    Address 9: 0
  Input Registers:
--------------------------------------------------
...
```

## Contributing

Feel free to fork this project and submit pull requests. If you encounter any issues, please open an issue on the GitHub repository.

## License

This project is licensed under the MIT License.
