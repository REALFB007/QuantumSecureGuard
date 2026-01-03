# QuantumShield - A Step Towards Future Security
**Post-Quantum Cryptography Vulnerability Scanner**

Built in **Kali Linux** with **Python** and **Flask**

## Overview
A powerful, easy-to-use tool that scans websites for **Shor-vulnerable** cryptographic algorithms (RSA, ECC, ECDH) and recommends migration to **quantum-safe** alternatives like **Kyber** and **Dilithium**.

Built for the quantum era — detect today's risks before quantum computers break them.

##  Features

- Real-time TLS certificate analysis using OpenSSL
- Detects **RSA**, **ECC**, **ECDH**, **finite-field DH**, and outdated TLS versions
- Recognizes **hybrid PQC key exchange** (Kyber/ML-KEM)
- Smart **risk scoring**: HIGH / MEDIUM / LOW
- Generates **ready-to-use PQC code** (Kyber for key exchange, Dilithium for signatures)
- Professional **PDF report** with findings and fixes
- Clean Flask web interface

##  Demo Video

<a href="Quantum.mp4">
  <img src="quantum.jpg" alt="Click to play QuantumShield demo video" width="900" style="cursor: pointer; border-radius: 12px; box-shadow: 0 4px 8px rgba(0,0,0,0.3);"/>
</a>

## Quick Start

```bash
git clone https://github.com/REALFB007/QuantumShield.git
cd QuantumShield
python -m venv venv
source venv/bin/activate
pip install flask reportlab
python quantum_app.py
