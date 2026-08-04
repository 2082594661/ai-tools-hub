#!/usr/bin/env python3
"""Deploy to Surge.sh with automated login (Windows)"""
import sys, os, time, subprocess, shutil

def deploy():
    site_dir = r"C:\Users\龙潜\seo-website"
    domain = "ai-tools-hub.surge.sh"
    email = "2082594661@qq.com"
    password = "surge123456"
    
    surge_cmd = shutil.which("surge") or r"C:\Users\龙潜\AppData\Roaming\npm\surge.cmd"
    
    print(f"Deploying to {domain}...")
    print(f"Using surge at: {surge_cmd}")
    
    proc = subprocess.Popen(
        [surge_cmd, "--domain", domain, "."],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        cwd=site_dir,
        text=True,
        shell=True
    )
    
    output = ""
    buffer = ""
    while True:
        char = proc.stdout.read(1)
        if not char:
            break
        buffer += char
        sys.stdout.write(char)
        sys.stdout.flush()
        output += char
        
        if "email" in buffer.lower() and ":" in buffer:
            time.sleep(0.5)
            proc.stdin.write(email + "\n")
            proc.stdin.flush()
            buffer = ""
            print(f"\n>>> Sent email: {email}")
        
        if "password" in buffer.lower() and ":" in buffer:
            time.sleep(0.5)
            proc.stdin.write(password + "\n")
            proc.stdin.flush()
            buffer = ""
            print(f"\n>>> Sent password")
    
    proc.wait()
    print(f"\nExit code: {proc.returncode}")
    return proc.returncode

if __name__ == "__main__":
    sys.exit(deploy())
