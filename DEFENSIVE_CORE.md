# 🛡️ PROJECT AVYAN: Defensive Core Fundamentals & System Architecture

This document serves as the foundational technical reference for System Administration, Defensive Hardening, and Core Networking Protocols within Project AVYAN.

---

## 🌐 1. Core Networking Architecture

### TCP/IP 4-Layer Model
1. **Link Layer (Layer 1):** Handles physical transmission and MAC addressing (Ethernet, 802.11 Wi-Fi).
2. **Internet Layer (Layer 2):** Responsible for packet routing across networks using IPv4/IPv6 and ICMP.
3. **Transport Layer (Layer 3):**
   - **TCP (Transmission Control Protocol):** Connection-oriented protocol providing reliable, ordered delivery via the 3-Way Handshake (`SYN` -> `SYN-ACK` -> `ACK`).
   - **UDP (User Datagram Protocol):** Connectionless, lightweight protocol prioritized for speed over reliability.
4. **Application Layer (Layer 4):** High-level protocols including HTTP, HTTPS, DNS, and SSH.

### Defensive HTTP Security Headers
- **Strict-Transport-Security (HSTS):** Enforces HTTPS connections and prevents SSL stripping attacks.
- **Content-Security-Policy (CSP):** Restricts resource loading to trusted domains to mitigate Cross-Site Scripting (XSS).
- **X-Frame-Options:** Prevents Clickjacking by restricting framing permissions.

### TLS/SSL Handshake Lifecycle
1. **Negotiation:** Client and server exchange supported cipher suites.
2. **Authentication:** Server presents its X.509 certificate for CA verification.
3. **Key Exchange:** Asymmetric encryption establishes a shared secret.
4. **Symmetric Encryption:** Bulk session data is encrypted using AES/ChaCha20.

---

## 🐧 2. Linux Hardening & Audit Standards

### Process Inspection
- `ps aux`: Displays all running processes with user attribution and resource usage.
- `top` / `htop`: Provides real-time process hierarchy and CPU/RAM consumption monitoring.
- `kill -9 <PID>`: Terminates unresponsive or non-compliant process IDs.

### System Audit Logs (`/var/log`)
- `/var/log/auth.log` (or `/var/log/secure`): Logs authentication attempts and SSH activity.
- `/var/log/syslog`: Captures central system events and service diagnostics.
- `journalctl -u <service_name>`: Queries systemd service logs for operational auditing.

### Principle of Least Privilege (PoLP)
- **Permissions Structure:** `rwx` (Read=4, Write=2, Execute=1).
- **File Security:** Critical configuration files should adhere to restrictive modes (e.g., `chmod 600` or `chmod 644`).
- **Execution Isolation:** Services must run under dedicated unprivileged system users rather than root.
