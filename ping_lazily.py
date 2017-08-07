import shlex
import subprocess
command = 'ping -c 1 www.google.com'
args = shlex.split(command)
try:
    subprocess.check_call(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    print('Google server is up')
except subprocess.CalledProcessError:
    print('Failed to ping')
