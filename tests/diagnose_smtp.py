import socket
import smtplib
import ssl

def check_dns():
    print("1. Checking DNS Resolution for smtp.gmail.com...")
    try:
        ip = socket.gethostbyname("smtp.gmail.com")
        print(f"   [PASS] Resolved to {ip}")
        return True
    except Exception as e:
        print(f"   [FAIL] DNS Resolution failed: {e}")
        return False

def check_port(port):
    print(f"\n2. Checking Connectivity to smtp.gmail.com:{port}...")
    try:
        sock = socket.create_connection(("smtp.gmail.com", port), timeout=5)
        print(f"   [PASS] Connection established on port {port}")
        sock.close()
        return True
    except Exception as e:
        print(f"   [FAIL] Connection timed out or refused on port {port}: {e}")
        return False

def check_smtp_handshake(port):
    print(f"\n3. Attempting SMTP Handshake on port {port}...")
    try:
        if port == 465:
            context = ssl.create_default_context()
            server = smtplib.SMTP_SSL("smtp.gmail.com", port, context=context, timeout=10)
        else:
            server = smtplib.SMTP("smtp.gmail.com", port, timeout=10)
            server.starttls()
        
        print(f"   [PASS] Handshake successful on port {port}")
        server.quit()
    except Exception as e:
        print(f"   [FAIL] Handshake failed on port {port}: {e}")

if __name__ == "__main__":
    print("--- SMTP Diagnostic Tool ---")
    if check_dns():
        p587 = check_port(587)
        p465 = check_port(465)
        
        if p587: check_smtp_handshake(587)
        if p465: check_smtp_handshake(465)
        
    print("\n--- Diagnosis Complete ---")
