######
import base64
import boto3
from botocore.signers import RequestSigner
import re


class EKSAuth(object):
    METHOD = 'GET'
    EXPIRES = 60
    EKS_HEADER = 'x-k8s-aws-id'
    EKS_PREFIX = 'k8s-aws-v1.'
    STS_URL = 'sts.amazonaws.com'
    #STS_ACTION = 'Action=GetCallerIdentity&Version=2012-10-17'
    STS_ACTION = 'Action=GetCallerIdentity&Version=2011-06-15'

    def __init__(self, cluster_id, region='us-east-1'):
        self.cluster_id = cluster_id
        self.region = region

    def get_token(self):
        """
        Return bearer token
        """
        session = boto3.session.Session()
        # Get ServiceID required by class RequestSigner
        client = session.client("sts", region_name=self.region)
        service_id = client.meta.service_model.service_id

        signer = RequestSigner(
            service_id,
            session.region_name,
            'sts',
            'v4',
            session.get_credentials(),
            session.events
        )

        params = {
            'method': self.METHOD,
            'url': 'https://' + self.STS_URL + '/?' + self.STS_ACTION,
            'body': {},
            'headers': {
                self.EKS_HEADER: self.cluster_id
            },
            'context': {}
        }

        signed_url = signer.generate_presigned_url(
            params,
            region_name=session.region_name,
            expires_in=self.EXPIRES,
            operation_name=''
        )

        base64_enc = base64.urlsafe_b64encode(signed_url.encode('utf-8')).decode('utf-8')
        #print("url encoded: " + base64_enc)
        newbase64_nopadding = re.sub(r'=*', '', base64_enc)
        print("ulr not padded: " + newbase64_nopadding)
        return self.EKS_PREFIX + newbase64_nopadding
