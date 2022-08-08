import logging
from os import getenv
from typing import List, Any

from api_contrib.core.utils import logger
from kubernetes import client, config
from kubernetes.client import V1Deployment

logger.setLevel(logging.INFO)
BROKER_DEPLOYMENT_NAME = 'market-service-broker'
DEPLOYMENT_NAMESPACE = 'prod'
BROKER_SYMBOL_LABEL = 'broker-symbol'

if getenv('LOAD_KUBE_CONFIG'):
    config.load_kube_config()
else:
    config.load_incluster_config()

core_api = client.CoreV1Api()


def get_replica_count() -> int:
    apps_api_v1 = client.AppsV1Api()
    dep = apps_api_v1.read_namespaced_deployment(BROKER_DEPLOYMENT_NAME, DEPLOYMENT_NAMESPACE)
    return dep.spec.replicas


def get_dep_uid() -> int:
    apps_api_v1 = client.AppsV1Api()
    dep = apps_api_v1.read_namespaced_deployment(BROKER_DEPLOYMENT_NAME, DEPLOYMENT_NAMESPACE)
    return dep.metadata.uid


def get_dep() -> V1Deployment:
    apps_api_v1 = client.AppsV1Api()
    dep = apps_api_v1.read_namespaced_deployment(BROKER_DEPLOYMENT_NAME, DEPLOYMENT_NAMESPACE)
    return dep


def scale_broker_pods(desire_size: int, increment_by: int = 1, force: bool = False) -> None:
    """
    Increase replica num for Broker deployment
    """
    apps_api_v1 = client.AppsV1Api()
    dep = apps_api_v1.read_namespaced_deployment(BROKER_DEPLOYMENT_NAME, DEPLOYMENT_NAMESPACE)

    logger.info(f"desire_size: {desire_size} dep.spec.replicas:  {dep.spec.replicas} ")

    new_size = desire_size if force else dep.spec.replicas + increment_by

    if new_size > dep.spec.replicas:
        dep.spec.replicas = new_size
        logger.info(f" patch  deployment to {dep.spec.replicas} replicas")
        apps_api_v1.patch_namespaced_deployment(dep.metadata.name, DEPLOYMENT_NAMESPACE, dep)


def get_broker_all_pods() -> dict:
    """
    Get list of pod's names for BROKER_DEPLOYMENT_NAME
    """
    core_api = client.CoreV1Api()
    return dict([
        (pod.metadata.name, pod.metadata.labels)
        for pod in
        core_api.list_namespaced_pod(DEPLOYMENT_NAMESPACE,
                                     label_selector="app.kubernetes.io/name=market-service-broker"
                                     ).items
    ])


def get_pods() -> List[Any]:
    """
    Get list of pod's names for BROKER_DEPLOYMENT_NAME
    """
    core_api = client.CoreV1Api()
    return [
        pod.metadata.name
        for pod in
        core_api.list_namespaced_pod(DEPLOYMENT_NAMESPACE,
                                     label_selector="app.kubernetes.io/name=market-service-broker"
                                     ).items
        if pod.status.phase == "Running"
    ]


def add_label_to_pod(pod_name: str, label: tuple):
    core_api = client.CoreV1Api()

    pod = core_api.read_namespaced_pod(pod_name, DEPLOYMENT_NAMESPACE)

    name, value = label
    pod.metadata.labels[name] = value

    try:
        logger.info(f"try set {name}={value} for {pod_name}")
        core_api.patch_namespaced_pod(pod_name, DEPLOYMENT_NAMESPACE, pod)
    except Exception as e:
        logger.error("Cant set label")
        logger.error(e)
        logger.info(pod)


def is_pod_running(pod_name):
    try:
        pod = core_api.read_namespaced_pod(pod_name, DEPLOYMENT_NAMESPACE)
    except Exception as e:
        logger.error(f"Error read {pod_name}: {e}")
        return False

    return pod.status.phase == 'Running'
