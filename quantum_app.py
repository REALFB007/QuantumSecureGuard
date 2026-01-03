# quantum_app.py
from flask import Flask, render_template, request, send_file
from quantum_scanner import scan_quantum_risk
from quantum_report import generate_report
import os

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        url = request.form['url']
        if not url.startswith('http'):
            url = 'https://' + url
        
        findings, risk, risk_msg, fixes = scan_quantum_risk(url)
        
        # Kyber code (key exchange)
        kyber_code = """from oqs import KeyEncapsulation

kem = KeyEncapsulation("Kyber512")
public_key = kem.generate_keypair()
ciphertext, shared_secret = kem.encap_secret(public_key)
# Use shared_secret for symmetric encryption (AES-256)"""

        # Dilithium code (signature)
        dilithium_code = """from oqs import Signature

sig = Signature("Dilithium2")
public_key = sig.generate_keypair()
message = b"Hello quantum-safe world"
signature = sig.sign(message)
# Verify: sig.verify(message, signature)"""

        # Generate PDF
        pdf_path = generate_report(url, risk, risk_msg, findings, fixes, kyber_code, dilithium_code)
        pdf_filename = os.path.basename(pdf_path)
        
        return render_template('result.html', 
                              url=url, 
                              risk=risk, 
                              message=risk_msg, 
                              findings=findings, 
                              fixes=fixes, 
                              kyber_code=kyber_code,
                              dilithium_code=dilithium_code,
                              pdf_filename=pdf_filename)
    
    return render_template('index.html')

@app.route('/download/<path:filename>')
def download(filename):
    return send_file(os.path.join("reports", filename), as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
