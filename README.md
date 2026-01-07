# Burp_ctf
Web security practice using Burp for beginner

This repository contains intentionally vulnerable web challenges designed to practice HTTP request/response manipulation using Burp Suite.

⚠️ This code is intentionally insecure.
For educational / CTF practice only.
⚠️ Do NOT deploy to production.

## Requirements
- Python 3.10+ recommended
- Burp Suite (Community or Professional)

## Setup
```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python app.py

## Challenges Overview
Login Tampering (body / Intruder)
Cookie + Method Tampering
User-Agent Header + Response Header Inspection

No solutions are provided in this repository.
