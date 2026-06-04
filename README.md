SecureDropX
Zero-Knowledge Secure File Transfer Platform

SecureDropX is a cybersecurity research project demonstrating how Operational Security (OPSEC), client-side encryption, and anonymous file sharing can be combined into a secure file transfer system.

The platform ensures that files are encrypted before upload and can only be decrypted by users possessing the correct encryption key.

Features
Client-Side AES Encryption

Files are encrypted inside the browser before being uploaded.

Benefits:

Server cannot read uploaded files
Reduced impact of server compromise
Zero-knowledge architecture
Token-Based Access Control

Uploads require valid one-time tokens.

Benefits:

Controlled access
Reduced abuse
Operational flexibility
Tor Hidden Service Compatibility

Can be deployed behind a Tor Onion Service.

Benefits:

Anonymous access
Hidden server location
Enhanced privacy
Auto File Expiration

Files are automatically deleted after a configurable period.

Benefits:

Reduced forensic footprint
Lower storage requirements
Improved OPSEC
Secure File Retrieval

Files are identified using randomly generated UUIDs.

Benefits:

No predictable file paths
Improved confidentiality
Architecture
User Browser
      │
      ▼
Client-Side AES Encryption
      │
      ▼
Flask Application
      │
      ▼
Encrypted Storage
      │
      ▼
Authorized Retrieval
Security Model
Server Knows
File UUID
Upload timestamp
Server Does Not Know
File contents
Encryption keys
Plaintext data
Use Cases
Cybercrime investigations
Anonymous reporting systems
Whistleblower platforms
Secure evidence submission
Privacy-focused communications
Technologies Used
Python
Flask
JavaScript Web Crypto API
AES-GCM Encryption
Tor Hidden Services
Linux
Installation
Clone Repository
git clone https://github.com/USERNAME/SecureDropX.git
cd SecureDropX
Create Virtual Environment
python3 -m venv venv
source venv/bin/activate
Install Requirements
pip install -r requirements.txt
Run Application
python app.py
Disclaimer

This project is intended for educational, research, and defensive cybersecurity purposes only.

Users are responsible for complying with all applicable laws, regulations, and organizational policies.

Author

Lav Chaudhary

Cybersecurity Researcher | Cybercrime Investigator | Security Engineer

Founder — GCS Islet

📄 requirements.txt

Create:

Flask
📄 .gitignore

Create:

venv/
__pycache__/
uploads/
tokens.txt
file_map.txt
*.pyc

This is very important because:

❌ Never upload:

tokens.txt
uploads/
encryption keys
investigation data
