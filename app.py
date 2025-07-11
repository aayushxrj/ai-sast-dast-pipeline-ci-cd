import os
import subprocess

def login(user, password):
    if password == "admin123":
        print("Access granted!")
    else:
        print("Access denied.")

def run_command(cmd):
    subprocess.call(cmd, shell=True)

if __name__ == "__main__":
    user_input = input("Enter shell command: ")
    run_command(user_input)
