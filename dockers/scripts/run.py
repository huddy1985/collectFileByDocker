#!/bin/python
import json
import argparse
import subprocess

def generate_repo(_config):
    repos_list = _config['repos']

    with open(repos_list, 'r') as repo_fd:
        repos = json.load(repo_fd)

    return repos


def generate_dockerfile(_config, lsb, repo):
    docker_template = _config['template']
    dockerfile = _config['dockerfile']

    with open(docker_template + '.' + lsb, 'r') as template_fd:
        template = template_fd.read()
        template = template.replace('repo', repo)

    with open(dockerfile, 'w') as dockerfile_fd:
        dockerfile_fd.write(template)


def docker_init(_config):
    image = _config['build_url']['build_url']
    cmds = ['docker', 'buildx', 'create', '--driver', 'docker-container', '--driver-pot', 'image={}'.format(image)]
    subprocess.Popen(cmds)

    cmds = ['docker', 'buildx', 'use', 'white']


def docker_mode(_config):
    """
    mode means docker working flow:
    clean mode: only pull the repo, not install any apps.
    component mode: it will install the
    :param _config:
    :return:
    """
    mode = _config['mode']
    return mode


def docker_run(_config, r):
    mode = docker_mode(_config)
    docker_cmd = None
    if mode == 'clean':
        docker_cmd = ['docker', 'run', '--rm', '--privileged', r]
    elif mode == "component":
        dockerfile = _config['dockerfile']
        share = _config['share']
        share2 = _config['share2']
        docker_cmd = ['docker', 'run', '-v', '{}:{}'.format(share, share2), '--rm', '--privileged', 'yes']

    subprocess.Popen(docker_cmd)


def parse_args():
    opt = argparse.ArgumentParser(description="parse binary file")
    opt.add_argument("-c", "--config", required=False, help="config json file path", default=None)

    option = opt.parse_args()
    config_path = option.config
    return config_path


if __name__ == "__main__":
    print "-----------start working--------------"
    config = parse_args()

    with open(config, 'r') as fd:
        config_json = json.load(fd)

    if config_json is None:
        print 'please set correct config path'

    # init image url path
    docker_init(config_json)

    repo = generate_repo(config_json)
    for r in repo:
        repo_arch = repo[r]
        if len(repo_arch) > 0:
            for k in repo_arch:
                repos = repo_arch[k]
                for _r in repos:
                    generate_dockerfile(config_json, r, _r)
                    docker_run(config_json, _r)

    print "-----------working done--------------"


