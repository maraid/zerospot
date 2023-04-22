import unittest
from unittest.mock import patch
import zerospot
import random


# Credentials
USERNAME = 'my_username'
PASSWORD = 'my_password'

# Remote device
DEVICE_ID = 'ce8d71004f9597141d4b5940bd1bb2dc52a35dae'
DEVICE_KEY = 'U6+5+tIcqTzlX8Z6CA+DDGXgiIB270+D4l1gu4EUyKMS1g4j2JpdLu8xNWkw9uyKcvSvn/nKBCusEzaRIDJXau9GMCR+QdN9Iu2MM0/ME5flWUvOnq+O16mkK2IvD9GY'

# Expected results
BLOB = b'bf89Nle0zsD533CKWCKYeEqlnBrYHjtVhu0S3QuMl9Y='
ENCRYPTED_BLOB = b'/VHeE0bLLVmNRNLwXRRMHr43xQi9eAGgWcpHOSOv5KMfl9Wz'


class TestBlobEncryption(unittest.TestCase):
    def setUp(self):
        random.seed(0x42)
        with patch('secrets.randbits', new=random.getrandbits):
            self.b = zerospot.BlobBuilder(
                zerospot.Credentials(USERNAME, PASSWORD),
                DEVICE_ID,
                DEVICE_KEY)

    def test_build_blob(self):
        self.b._build()
        self.assertEqual(BLOB, self.b._blob)
        
    def test_encrypt_blob(self):
        self.b._encrypt()
        self.assertEqual(ENCRYPTED_BLOB, self.b._encrypted_blob)


if __name__ == '__main__':
    unittest.main()