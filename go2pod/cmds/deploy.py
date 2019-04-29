from go2pod.action import Action
from go2pod.ensure import (
    ensure_kube,
    ensure_podyaml,
)


def create_or_update_pod(client, pod_yaml_path):
    with Action('Creating pod').start() as action:
        pod_exists = client.get(pod_yaml_path)
        if pod_exists:
            client.delete(pod_yaml_path)
        action.ensure_true(client.create(pod_yaml_path),
                           'Create pod failed')


def run():
    pod_yaml_path = ensure_podyaml()
    kube_client = ensure_kube()
    create_or_update_pod(kube_client, pod_yaml_path)
