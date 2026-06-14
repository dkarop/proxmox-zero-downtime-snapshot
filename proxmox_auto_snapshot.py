import requests
import urllib3
import logging

# Απενεργοποίηση warnings για self-signed certificates στο εσωτερικό δίκτυο
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class ProxmoxManager:
    def __init__(self, host, user, password):
        self.host = host
        self.user = user
        self.password = password
        self.auth_ticket = ""
        self.csrf_token = ""
        self.headers = {}
        self.authenticate()

    def authenticate(self):
        url = f"https://{self.host}:8006/api2/json/access/ticket"
        payload = {"username": self.user, "password": self.password}
        
        try:
            response = requests.post(url, data=payload, verify=False, timeout=10)
            response.raise_for_status()
            data = response.json()['data']
            
            self.auth_ticket = data['ticket']
            self.csrf_token = data['CSRFPreventionToken']
            self.headers = {
                "Cookie": f"PVEAuthCookie={self.auth_ticket}",
                "CSRFPreventionToken": self.csrf_token
            }
            logging.info("Successfully authenticated to Proxmox API.")
        except requests.exceptions.RequestException as e:
            logging.error(f"Proxmox authentication failed: {e}")

    def create_vm_snapshot(self, node, vmid, snap_name, description="Pre-update automated snapshot"):
        """Creates a snapshot for a specific VM."""
        url = f"https://{self.host}:8006/api2/json/nodes/{node}/qemu/{vmid}/snapshot"
        payload = {
            "snapname": snap_name,
            "description": description,
            "vmstate": 1 # Περιλαμβάνει τη μνήμη RAM (zero-downtime rollback)
        }
        
        try:
            response = requests.post(url, headers=self.headers, data=payload, verify=False)
            response.raise_for_status()
            logging.info(f"Snapshot '{snap_name}' triggered for VM {vmid} on node {node}.")
        except requests.exceptions.RequestException as e:
            logging.error(f"Failed to create snapshot for VM {vmid}: {e}")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    # Χρήση σε παραγωγή: Τα credentials θα πρέπει να καλούνται από Environment Variables
    px = ProxmoxManager(host="10.0.0.5", user="root@pam", password="SuperSecretPassword")
    
    # Λήψη snapshot στο παραγωγικό VM με ID 105 (π.χ. SQL Server)
    px.create_vm_snapshot(node="pve-cluster-01", vmid="105", snap_name="pre_db_migration")
