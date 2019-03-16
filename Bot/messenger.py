import json
import requests,re

from bottle import debug, request, route, run

GRAPH_URL = "https://graph.facebook.com/v2.6"
VERIFY_TOKEN = 'YOUR_VERIFY_TOKEN'
PAGE_TOKEN='EAAljQZC3NPJABAOXft46ZB1VRwhYB8aZCPZBlsIKIP9mbDf3jifoXSwrkIsAGBVGZA17YKd3XyY6cUpq4qWgChaaCF8sKpmbiW0NpdNLX1YfDaZBZAbQS5HnYP7vw4ZAQiJ90nVHG7092Yc3g7ZCR46OQlCqGSjzoPtZAtYLo1QgUpEgZDZD'
def send_to_messenger(ctx):
    url = "{0}/me/messages?access_token={1}".format(GRAPH_URL, PAGE_TOKEN)
    response = requests.post(url, json=ctx)

@route('/chat', method=["GET", "POST"])
def bot_endpoint():
    if request.method.lower() == 'get':
        verify_token = request.GET.get('hub.verify_token')
        hub_challenge = request.GET.get('hub.challenge')
        if verify_token == VERIFY_TOKEN:
            url = "{0}/me/subscribed_apps?access_token={1}".format(GRAPH_URL, PAGE_TOKEN)
            response = requests.post(url)
            return hub_challenge
    else:
        body = json.loads(request.body.read())
        user_id = body['entry'][0]['messaging'][0]['sender']['id']
        page_id = body['entry'][0]['id']
        message_text = body['entry'][0]['messaging'][0]['message']['text']
        # we just echo to show it works
        # use your imagination afterwards
        if user_id != page_id:

            if bool(re.match(r'((h+e+y+(o)?)|(y+o+)|(h+(e+|a+)ll*o+)|(h+i+)|(h(a+)lo+))', message_text.lower())):
                ctx = {
                    'recipient': {
                        'id': user_id,
                    },
                    'message': {
                        'text': 'Welcome to Pet2Vet! How can I help you?\n1. Rescue a stray animal\n2. Find vets near me\n3. First Aid solutions\n4. I want to adopt an animal!\n5. I want to volunteer for an NGO\n6. Report feral animal issue\n7. I want to donate!',
                    }
                }
            elif message_text=='1':
                ctx = {
                    'recipient': {
                        'id': user_id,
                    },
                    'message': {
                        'text': 'kal dekhte hai.',
                    }
                }
            elif message_text=='2':
                ctx = {
                    'recipient': {
                        'id': user_id,
                    },
                    'message': {
                        'text': 'ghar se nikalke dhund le',
                    }
                }
            elif message_text=='3':
                ctx = {
                    'recipient': {
                        'id': user_id,
                    },
                    'message': {
                        'text': 'tu doctor hai kya?',
                    }
                }
            elif message_text=='4':
                ctx = {
                    'recipient': {
                        'id': user_id,
                    },
                    'message': {
                        'text': 'toh jaana karna'
                    }
                }
            elif message_text=='5':
                ctx = {
                    'recipient': {
                        'id': user_id,
                    },
                    'message': {
                        'text': 'kyu bey, baap k paas zyada paisa hai kya?',
                    }
                }
            elif message_text=='6':
                ctx = {
                    'recipient': {
                        'id': user_id,
                    },
                    'message': {
                        'text': 'Lunch time, baad mein aana!',
                    }
                }
            elif message_text=='7':
                ctx = {
                    'recipient': {
                        'id': user_id,
                    },
                    'message': {
                        'text': 'Baadmein aana',
                    }
                }        
            else:
                ctx = {
                    'recipient': {
                        'id': user_id,
                    },
                    'message': {
                        'text': 'We are unable to interpret. Please try again.',
                    }
                }                       
            response = send_to_messenger(ctx)
        return ''


debug(True)
run(reloader=True, port=8000)
