# quantum_scanner.py — FINAL DNS FIX
import subprocess
import re

def scan_quantum_risk(url):
    try:
        # Strip http/https
        host = url.replace("https://", "").replace("http://", "").split('/')[0]
        
        result = subprocess.run([
            "openssl", "s_client", "-connect", f"{host}:443", "-servername", host,
            "-showcerts"
        ], input="Q\n", capture_output=True, text=True, timeout=40)

        output = result.stdout + result.stderr
        
        vulns = []
        notes = []
        fixes = []
        
        # Certificate Signature
        if re.search(r'ecdsa|ec public key|elliptic curve|secp|p-256|p-384|p-521', output, re.IGNORECASE):
            vulns.append("Certificate signature: ECC (ECDSA) — Shor-vulnerable")
            fixes.append("Replace ECC signature with Dilithium (ML-DSA)")
        if re.search(r'rsa|rsaencryption|rsa key', output, re.IGNORECASE):
            vulns.append("Certificate signature: RSA — Shor-vulnerable")
            fixes.append("Replace RSA signature with Dilithium (ML-DSA)")
        
        # Key Exchange
        if re.search(r'x25519mlkem|mlkem|kyber', output, re.IGNORECASE):
            notes.append("Key exchange: Hybrid PQC (Kyber/ML-KEM) — Quantum-safe")
            fixes.append("Key exchange already quantum-safe — keep it!")
        elif re.search(r'x25519|secp|prime256|ecdh', output, re.IGNORECASE):
            vulns.append("Key exchange: Classical ECC (X25519/ECDH) — Shor-vulnerable")
            fixes.append("Replace key exchange with Kyber/ML-KEM hybrid")
        
        # Finite-field DH
        if re.search(r'diffie-hellman', output, re.IGNORECASE) and not re.search(r'ecdh', output, re.IGNORECASE):
            vulns.append("Key exchange: Finite-field DH — Shor-vulnerable")
            fixes.append("Replace with Kyber")
        
        # TLS version
        if re.search(r'tlsv1\.[0-2]', output, re.IGNORECASE):
            vulns.append("TLS < 1.3 — Outdated")
            fixes.append("Upgrade to TLS 1.3")
        if "tlsv1.3" in output.lower():
            notes.append("TLS 1.3 — Modern")
        
        # Risk
        if vulns:
            risk = "LONG TERM POST QUANTUM CRYPTOGRAPHY" if notes else "POST QUANTUM CRYPTOGRAPHY"
            risk_msg = f"{risk} RISK — Shor-vulnerable components detected"
        else:
            risk = "LOW"
            risk_msg = "LOW RISK — No Shor-vulnerable algorithms detected"
        
        findings = vulns + notes
        if not findings:
            findings = ["Scan successful — likely quantum-safe"]
        
        return findings, risk, risk_msg, fixes
        
    except subprocess.TimeoutExpired:
        return ["Scan timed out — site may use HTTP/3 or advanced TLS"], "UNKNOWN", "Timeout", []
    except Exception as e:
        return [f"Scan failed: {str(e)}"], "UNKNOWN", "Error", []
