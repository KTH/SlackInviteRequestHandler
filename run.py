__author__ = 'tinglev@kth.se'

import json
import re
import os
import ssl
import logging
from smtplib import SMTP as SMTP
from email.mime.text import MIMEText
from flask import Flask, jsonify, request
import requests
app = Flask(__name__)

@app.route('/invite-handler/_monitor', methods=['GET'])
def monitor():
    return 'APPLICATION_STATUS: OK'

@app.route('/invite-handler/event', methods=['POST'])
def challenge():
    logger = logging.getLogger(__name__)
    logging.basicConfig(level=logging.DEBUG, format='%(message)s')
    req_json = request.get_json()
    logger.debug('Got json: %s', json.dumps(req_json))
    if req_json and req_json.get('challenge'):
        return jsonify({'challenge': req_json.get('challenge')})
    elif req_json:
        mail_sent = handle_invite_request(req_json)
        if mail_sent:
            send_slack_message()
    return jsonify({'challenge': ''})

def send_slack_message():
    token = os.environ.get('SLACK_TOKEN')
    response = requests.post(
        'https://slack.com/api/chat.postMessage',
        headers={
            'Content-Type': 'application/json; charset=utf-8',
            'Authorization': f'Bearer {token}'
        },
        json={
            "channel": "#user-invitation-requests",
            "text": "I sent a mail for this request"
        }
    )
    print(json.dumps(response.json()))

def handle_invite_request(req_json):
    logger = logging.getLogger(__name__)
    name, email, member_type = None, None, None
    name_email_regex = re.compile(r'\*Name\*: (.+)\*Email\*: <mailto:(.+)\|(.+)>')
    member_regex = re.compile(r'\*Account type\*: <(.+)\|(.+)>')
    if 'event' in req_json and 'text' in req_json['event']:
        event = req_json['event']
        if 'requested to invite' not in event['text']:
            logger.info('Got message that wasnt invite request - skipping')
            return False
        elif 'attachments' not in event:
            logger.info('Got message without attachments - skipping')
            return False
        else:
            attachments = event['attachments']
            for attachment in attachments:
                if 'text' not in attachment:
                    logger.debug('Attachment missing text - going to next one')
                    continue
                text = attachment['text'].replace('\n', '')
                logger.debug('Text is %s', text)
                name_regex_result = name_email_regex.match(text)
                member_regex_result = member_regex.match(text)
                if name_regex_result:
                    logger.debug('Matched name_regex')
                    name = name_regex_result.group(1)
                    email = name_regex_result.group(2)
                elif member_regex_result:
                    logger.debug('Matched member_regex')
                    member_type = member_regex_result.group(2)
            logger.info('Got name, email, member: %s, %s, %s', name, email, member_type)
            send_email(email)
            return True
    logger.info('Got message that had no event or event -> text')
    return False

def send_email(email):
    email_text = """
    Hej!
    Du har bjudit in en ny användare till Slack. Eftersom Slack vid KTH är en avgiftsbelagd tjänst måste användare istället beställas via detta formulär: 
    https://intra.kth.se/it/arbeta-pa-distans/chatt/slack/access-to-slack  
    ----
    Hello
    You have invited a new user to Slack. Since Slack is a paid service at KTH you must instread fill out this order form: 
    https://intra.kth.se/en/it/arbeta-pa-distans/chatt/slack/access-to-slack
    """
    smtp_user = str(os.environ.get('SMTP_USER'))
    smtp_password = str(os.environ.get('SMTP_PASSWORD'))
    with SMTP(host=str(os.environ.get('SMTP_HOST')), port=587) as conn:
        ctx = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
        ctx.load_default_certs()
        conn.starttls(context=ctx)
        conn.login(smtp_user, smtp_password)
        msg = MIMEText(email_text, 'plain')
        sender = 'noreply@kth.se'
        msg['Subject'] = 'Slackinbjudan/Slack invite'
        msg['From'] = sender
        # Remove this after testing
        if (email == 'u1x7uslm@kth.se'):
            conn.sendmail(sender, email, msg.as_string())
