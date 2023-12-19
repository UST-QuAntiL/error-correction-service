import unittest
import os, sys
import json

parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from app import create_app


class FlaskClientTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app("testing")
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client(use_cookies=True)

    def tearDown(self):
        self.app_context.pop()

    def test_apply_ecc(self):
        response = self.client.post(
            "/applyECC",
            data=json.dumps(
                {
                    "circuit": "OPENQASM 2.0;\ninclude \"qelib1.inc\";qreg q[2];\ncreg c[2];\nh q[0];\ncx q[0], q[1];\n",
                    "errorCorrectionCode": "Q7Steane",
                    "eccFrequency": "20",
                }
            ),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        print(response.get_json())


