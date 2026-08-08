import struct

class ModbusPacketInspector:
    def __init__(self):
        pass

    def parse_mbap_header(self, raw_bytes):
        """
        MBAP Header Structure (7 bytes):
        - Transaction ID: 2 bytes
        - Protocol ID: 2 bytes (0x0000 for Modbus)
        - Length: 2 bytes
        - Unit ID: 1 byte
        """
        if len(raw_bytes) < 7:
            return {"valid": False, "error": "Packet too short for MBAP header"}

        transaction_id, protocol_id, length, unit_id = struct.unpack(">HHHB", raw_bytes[:7])
        
        function_code = raw_bytes[7] if len(raw_bytes) > 7 else None
        
        return {
            "valid": True,
            "transaction_id": transaction_id,
            "protocol_id": protocol_id,
            "is_standard_modbus": (protocol_id == 0),
            "payload_length": length,
            "unit_id": unit_id,
            "function_code": function_code,
            "anomalous_len": length != (len(raw_bytes) - 6)
        }

if __name__ == "__main__":
    inspector = ModbusPacketInspector()
    # Sample Modbus Read Holding Registers frame
    sample_frame = b'\x00\x01\x00\x00\x00\x06\x01\x03\x00\x00\x00\x01'
    parsed = inspector.parse_mbap_header(sample_frame)
    print("[+] Modbus Frame Telemetry Inspection:", parsed)
