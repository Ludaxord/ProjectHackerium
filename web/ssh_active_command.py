from utils.basic.parser import default_ssh_active_command_args
from utils.webservices.ssh import SSH

parser = default_ssh_active_command_args()

ip = parser.ip
user = parser.user
password = parser.passwd
port = parser.port

ssh = SSH()

ssh.ssh_command_line(ip, user, password, port)
