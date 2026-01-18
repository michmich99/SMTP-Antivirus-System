# SMTP-Antivirus-System

SMTP Antivirus System is a Python-based email protection platform designed to detect spam messages and malicious attachments before they reach the recipient. The system implements a custom SMTP server and a graphical client application that analyze email content in real time using local signature scanning and online verification. By combining multiple detection techniques, the project provides a practical approach to securing email communication in a controlled environment.


## Key Features

- Spam Detection Engine - scans email content for predefined suspicious keywords and blocks unwanted messages  
- Virus Signature Scanning - checks attachments against a local database of known malware signatures  
- VirusTotal Integration - cloud-based verification using the VirusTotal API for advanced threat detection  
- Custom SMTP Server - fully implemented mail server that processes and validates incoming emails  
- GUI Email Client - user-friendly interface for composing messages and attaching files  
- Multi-Layer Protection - combines local and online analysis for better accuracy  
- Configurable Word Lists - easy editing of spam keywords and virus signatures  
- Real-Time Feedback - clear server responses explaining why a message was blocked or accepted  
- Cross-Platform Support - built with Python and Tkinter, compatible with major operating systems

## How It Works

1. The user sends an email through the GUI client  
2. The SMTP server receives the message and performs several checks:  
   - Spam word analysis in the email body  
   - Attachment scanning using local virus signatures  
   - Verification via VirusTotal  
3. If a threat is detected, the email is blocked and the user receives a detailed warning  
4. Safe messages are delivered normally

## Security Checks Performed

- Spam Filter - searches for blacklisted words in the email content  
- Signature Scan - compares attachments with known malware patterns  
- Online Scan - queries VirusTotal for additional verification  
- Validation Logic - prevents delivery of suspicious messages

## Setup Instructions

The project was developed and tested in a virtual machine running Ubuntu 18.04 LTS.

### 1. Install Python 3

If Python 3 is not installed, run:

```bash
sudo apt update
sudo apt install python3
```

### 2. Install Tkinter for the GUI

```bash
sudo apt-get install python3-tk
```

### 3. Run the System

Open two terminal windows:

- One for the server side  
- One for the client side  

Start the server:

```bash
python3 Server.py
```

Start the client:

```bash
python3 Client.py
```

The graphical client interface will open, allowing the user to compose emails, attach files, and send messages for security analysis.

## Limitations

- Virus signature database requires manual updates  
- VirusTotal responses may occasionally be delayed  
- Spam word list is static and user-defined

## Project Structure

- **Server.py** - SMTP server responsible for email validation and security checks  
- **Client.py** - graphical email client for composing and sending messages  
- **spamWords** - list of keywords considered as spam  
- **signatures** - database of known virus signatures  
- **infected** - sample file used for demonstration and testing

## Purpose

This project was developed to explore:

- SMTP protocol implementation  
- Email security mechanisms  
- Antivirus detection methods  
- Python GUI development  
- Client–server architecture
