import requests

from .blob import BlobBuilder
from .helpers import Credentials, int_to_b64str

class ZeroconfConnect:
    def __init__(self, uri: str, username: str, password: str):
        self.uri = uri
        self.credentials = Credentials(username, password)

    def connect(self):
        device_id, device_key = self._get_info()
        builder = BlobBuilder(self.credentials, device_id, device_key)
        blob = builder.build()
        r = self._add_user(
            self.credentials.username.decode('ascii'),
            int_to_b64str(builder.dh_keys.public_key),
            blob)

        return r.json() == {'spotifyError': 0, 'status': 101, 'statusString': 'ERROR-OK'}

    def _get_info(self): # -> tuple(str, str)
        info = requests.get(self.uri, params={'action': 'getInfo'}).json()
        return info['deviceID'], info['publicKey']

    def _add_user(self, username: str, client_key: str, blob: str): # -> bool
        respone = requests.post(
            self.uri,
            headers={
                'Content-Type': 'application/x-www-form-urlencoded'
            },
            params={
                'action': 'addUser',
                'userName': username,
                'clientKey': client_key,
                'blob': blob
            }
        )
        return respone
