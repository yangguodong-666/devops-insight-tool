# 功能一：批量服务器巡检（SSH）
# 目标：连接多台服务器，采集：
# 运行时间（uptime）
# 磁盘使用率（df -h）
# 内存使用率（free -m）

import paramiko
import yaml

class SSHClient:
    def __init__(self, config_path="config/servers_example.yaml"):
        with open(config_path, 'r', encoding='utf-8') as f:
            self.servers = yaml.safe_load(f)["servers"]

    def check_server(self, server):
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        result = {}

        try:
            ssh.connect(server["ip"], username=server["user"], password=server["password"], timeout=5)
            for cmd in ["uptime", "df -h", "free -m"]:
                stdin, stdout, stderr = ssh.exec_command(cmd)
                result[cmd] = stdout.read().decode().strip()
        finally:
            ssh.close()

        return result

    def run_all(self):
        return {s["name"]: self.check_server(s) for s in self.servers}
