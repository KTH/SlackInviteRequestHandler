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
        result = {}
        try:
            result = handle_invite_request(data)
        except:
            self.assertFalse(True)
        self.assertEqual(result['email'], 'u1x7uslm@kth.se')
        self.assertEqual(result['slack_user'], 'U01CD0UC9A4')
        self.assertEqual(result['member_type'], 'Full Member')
        self.assertEqual(result['name'], 'Test')

    def test_send_slack_message(self):
        send_slack_message({
            'email': 'u1x7uslm@kth.se',
            'slack_user': 'U01CD0UC9A4'
        })