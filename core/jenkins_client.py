# 功能二：Jenkins 构建状态采集（API）

import jenkins
import yaml

class JenkinsClient:

    def __init__(self, config_path="config/jenkins_example.yaml"):
        with open(config_path, 'r', encoding='utf-8') as f:
            cfg = yaml.safe_load(f)["jenkins"]
        self.server = jenkins.Jenkins(
            cfg["url"],
            username = cfg["user"],
            password = cfg["token"]
        )
        self.jobs = cfg["jobs"]

    def get_jobs_status(self, job_name):
        info = self.server.get_job_info(job_name)
        last_build = info["lastBuild"]["number"]
        build_info = self.server.get_build_info(job_name, last_build)
        return{
            "number": last_build,
            "status": build_info["result"],
            "url": build_info["url"]
        }

    def collect(self):
        return {job: self.get_jobs_status(job) for job in self.jobs}