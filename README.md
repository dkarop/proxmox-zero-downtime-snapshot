# Proxmox Zero-Downtime Snapshot Automator

## Overview
An automation script written in Python that interacts with the Proxmox VE REST API. It triggers automated, zero-downtime snapshots of production Virtual Machines (VMs) prior to critical updates or system migrations. 

By capturing the RAM state alongside the disk state, this script ensures that critical industrial servers can be rolled back instantly without disrupting active production services.

## Features
* **Stateful Snapshots:** Captures VM memory (RAM) state for true zero-downtime rollbacks.
* **API Authentication:** Securely generates and utilizes Proxmox Tickets and CSRF tokens.
* **Internal Network Support:** Bypasses self-signed certificate warnings commonly found in internal/air-gapped enterprise networks.

## Prerequisites
* Python 3.x
* `requests` and `urllib3` libraries.
* A Proxmox VE environment with API access enabled.

## Installation & Configuration
1. Clone the repository.
2. Install required Python packages:
   ```bash
   pip install requests urllib3 
3. Edit proxmox_auto_snapshot.py and configure the following parameters (or pass them via Environment Variables for production security):
host: Your Proxmox IP/Hostname.
user: Your Proxmox API user (e.g., root@pam).
password: The corresponding password or API token.

## Usage
Run the script to trigger a snapshot for a specific VM ID:
python proxmox_auto_snapshot.py
