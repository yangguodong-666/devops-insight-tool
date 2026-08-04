## Configuration
# Edit `config/servers.yaml` and `config/jenkins.yaml` before running.

# ## Use Case
# This tool is designed for:
# - DevOps engineers managing multi-server environments
# - Teams practicing CI/CD with Jenkins
# - Global teams requiring bilingual/multilingual reporting

# ## Author
# Project Manager turned DevOps Engineer, fluent in English, Cantonese, and Spanish.
# Focused on delivery efficiency and cross-regional cloud operations.

# ---
# *“Automation is not about replacing people; it's about freeing them to solve real problems.”*

from core.ssh_client import SSHClient
from core.jenkins_client import JenkinsClient
from core.reporter import Reporter
import os
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# print(BASE_DIR)

def main():

    servers_config = os.path.join(BASE_DIR, "config", "servers.yaml") # 说明绝对路径
    jenkins_config = os.path.join(BASE_DIR, "config", "jenkins.yaml") # 说明绝对路径

    reports_dir = os.path.join(BASE_DIR, "reports")
    os.makedirs(reports_dir, exist_ok=True)

    ssh = SSHClient(config_path=servers_config)
    ssh_data = ssh.run_all()

    jenkins = JenkinsClient(config_path=jenkins_config)
    jenkins_data = jenkins.collect()

    reporter = Reporter(ssh_data, jenkins_data, reports_dir)
    reporter.save()

if __name__ == "__main__":
    main()



