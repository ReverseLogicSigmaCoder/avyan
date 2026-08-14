import socket
import struct

def read_modbus_holding_registers(target_ip, start_register=0, count=2, timeout=3.0):
    """
    Real-World Modbus TCP Raw Packet Injector & Response Dissector.
    Sends raw MBAP header to inspect physical PLC registers.
    """
    port = 502
    transaction_id = 0x0001
    protocol_id = 0x0000  # Modbus TCP
    length = 0x0006       # Remaining bytes
    unit_id = 0x01        # PLC Unit ID
    function_code = 0x03  # Read Holding Registers
    
    # Pack binary MBAP header and PDU (12 bytes total)
    request_packet = struct.pack(
        ">HHHBBHH",
        transaction_id,
        protocol_id,
        length,
        unit_id,
        function_code,
        start_register,
        count
    )

    print(f"[*] Sending Raw Binary Frame to {target_ip}:{port}...")
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        sock.connect((target_ip, port))
        sock.send(request_packet)
        
        response = sock.recv(1024)
        sock.close()

        if len(response) >= 9:
            rx_trans, rx_proto, rx_len, rx_unit, rx_func, byte_count = struct.unpack(">HHHBBB", response[:9])
            if rx_func == 0x03:
                register_data = response[9:9+byte_count]
                print(f"[+] REAL SCADA RESPONSE RECEIVED!")
                print(f"    - Function Code: {rx_func} (Valid Read)")
                print(f"    - Raw Register Bytes: {register_data.hex()}")
                return {"status": "SUCCESS", "data_hex": register_data.hex()}
            else:
                print(f"[-] Modbus Exception Code: {rx_func}")
                return {"status": "MODBUS_EXCEPTION", "code": rx_func}
        else:
            print("[-] Invalid / Short response from host.")
            return {"status": "INVALID_RESPONSE"}

    except socket.timeout:
        print("[-] Target IP did not respond (Filtered or Closed).")
        return {"status": "TIMEOUT"}
    except Exception as e:
        print(f"[-] Connection Error: {e}")
        return {"status": "ERROR", "message": str(e)}

if __name__ == "__main__":
    # Test on target IP / local gateway
    read_modbus_holding_registers("127.0.0.1")
  
