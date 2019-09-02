import os.path
import yaml
import boto3
from kubernetes import client, config
from auth import EKSAuth

# Configure your cluster name and region here
KUBE_FILEPATH = '/tmp/kubeconfig'
CLUSTER_NAME = 'simba'
REGION = 'us-east-1'

# We assume that when the Lambda container is reused, a kubeconfig file exists.
# If it does not exist, it creates the file.

if not os.path.exists(KUBE_FILEPATH):
    kube_content = dict()
    # Get data from EKS API
    eks_api = boto3.client('eks', region_name=REGION)
    cluster_info = eks_api.describe_cluster(name=CLUSTER_NAME)
    certificate = cluster_info['cluster']['certificateAuthority']['data']
    endpoint = cluster_info['cluster']['endpoint']

    # Generating kubeconfig
    kube_content = dict()

    kube_content['apiVersion'] = 'v1'
    kube_content['clusters'] = [
        {
            'cluster':
                {
                    'server': endpoint,
                    'certificate-authority-data': certificate
                },
            'name': 'Kubernetes'

        }]

    kube_content['contexts'] = [
        {
            'context':
                {
                    'cluster': 'Kubernetes',
                    'user': 'aws'
                },
            'name': 'Kubernetes'
        }]

    kube_content['current-context'] = 'Kubernetes'
    kube_content['Kind'] = 'config'
    kube_content['users'] = [
        {
            'name': 'aws',
            'user': 'lambda'
        }]

    # Write kubeconfig
    with open(KUBE_FILEPATH, 'w') as outfile:
        yaml.dump(kube_content, outfile, default_flow_style=False)


def handler(event, context):
    interactWK8s()

def interactWK8s():
    # Get Token
    eks = EKSAuth(CLUSTER_NAME)
    token = eks.get_token()
    # Configure
    print("############")
    file_o = open(KUBE_FILEPATH)
    content = file_o.read()
    print(content)
    file_o.close()
    config.load_kube_config(KUBE_FILEPATH)
    configuration = client.Configuration()
    configuration.api_key['authorization'] = token
    configuration.api_key_prefix['authorization'] = 'Bearer'
    # API
    api = client.ApiClient(configuration)
    v1 = client.CoreV1Api(api)

    # Get all the pods
    ret = v1.list_namespaced_pod("default")

    for i in ret.items:
       print("%s\t%s\t%s" % (i.status.pod_ip, i.metadata.namespace, i.metadata.name))

    # ret = v1.list_node()
    # for i in ret.items:
    #     print("%s" % (i.metadata.name))
