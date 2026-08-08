import socket
import struct
import json

class SCADAProtocolProber:
    def __init__(self, timeout=3.0):
        self.timeout = timeout

    def probe_modbus_tcp(self, ip, port=502):
        """Sends a raw Modbus TCP Read Holding Registers PDU (Unit ID: 1, Reg: 0, Count: 1)"""
        # Modbus ADU: Transaction ID (2B), Protocol ID (2B), Length (2B), Unit ID (1B), Function Code (1B), Data (4B)
        modbus_pdu = b'\x00\x01\x00\x00\x00\x06\x01\x03\x00\x00\x00\x01'
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(self.timeout)
            sock.connect((ip, port))
            sock.send(modbus_pdu)
            response = sock.recv(1024)
            sock.close()
            if len(response) >= 9 and response[7] == 0x03:
                return {"status": "ACTIVE_HANDSHAKE", "details": "Modbus PLC Responsive"}
            elif len(response) >= 9 and response[7] > 0x80:
                return {"status": "MODBUS_EXCEPTION", "details": "PLC Responded with Exception Code"}
            return {"status": "PORT_OPEN_NO_MODBUS", "details": "Non-Modbus protocol active on port"}
        except socket.timeout:
            return {"status": "TIMEOUT", "details": "No response from PLC endpoint"}
        except Exception as e:
            return {"status": "CONNECTION_FAILED", "details": str(e)}

    def run_probe(self, target_ip):
        modbus_res = self.probe_modbus_tcp(target_ip)
        return {"target": target_ip, "modbus_audit": modbus_res}

if __name__ == "__main__":
    prober = SCADAProtocolProber()
    print(prober.run_probe("127.0.0.1"))
              
