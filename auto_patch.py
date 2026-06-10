import subprocess

def run(cmd):
    print(f"Running: {cmd}")
    subprocess.run(cmd, shell=True, check=False)

# Step 1: Scan
run("pip-audit")

# Step 2: Fix
run("pip-audit --fix")

# Step 3: Run tests
run("pytest")
