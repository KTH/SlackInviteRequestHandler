__author__ = 'tinglev'

import os
import json
import unittest
from mock import patch, call
from run import handle_invite_request, send_slack_message

class UnitTests(unittest.TestCase):

    def test_handle_invite_request(self):
        data = None
        with open('testdata.json') as json_file:
            data = json.load(json_file)
        try:
            handle_invite_request(data)
        except:
            self.assertFalse(True)

    def test_send_slack_message(self):
        send_slack_message()