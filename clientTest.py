import unittest
from kubernetes import client, config
from kubernetes.stream import stream

import main



def localConfig():
    config.load_kube_config()
    api = client.CoreV1Api()
    print("listing nodes:")
    ret = api.list_node()
    for i in ret.items:
        print("%s" % (i.metadata.name))


class MyTestCase(unittest.TestCase):
    def testLocalConfig(self):
        localConfig()

    def testRemoteConfig(self):
        main.interactWK8s()

if __name__ == '__main__':
    unittest.main()
