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
        loc_lat,loc_long=0,0
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
                        'text': 'Please tell me your location.',
                    'quick_replies' : [{
                        'content_type': 'location',
                        "title": "My Location",
                        'payload' : 'Location',
                    }]
                    }
                }
                response=send_to_messenger(ctx)
                loc_lat=body['entry'][0]['messaging'][0]['message']['attachments'][0]['payload']['coordinates']['lat']
                loc_long=body['entry'][0]['messaging'][0]['message']['attachments'][0]['payload']['coordinates']['long']
        
                  
                
            elif loc_long and loc_lat:
                ctx={
                'recipient': {
                    'id': user_id,
                },
                'message': {
                    'text': 'Your location is: '+loc_lat+','+loc_long,
                    }
                }
                response=send_to_messenger(ctx)
                
            elif message_text=='2':
                ctx = {
                    'recipient': {
                        'id': user_id,
                    },
                    'message': {
                        'text': 'Please visit the website.',
                    }
                }
            elif message_text=='3':
                ctx = {
                    'recipient': {
                        'id': user_id,
                    },
                    'message': {
                        'text': 'Please check out the videos on the website.',
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
                        'text': 'Please find the info on our website.',
                    }
                }
            elif message_text=='6':
                ctx = {
                    'recipient': {
                        'id': user_id,
                    },
                    'message': {
                        'text': 'We are currently working on this feature.',
                    }
                }
            elif message_text=='7':
                ctx = {
                    'recipient': {
                        'id': user_id,
                    },
                    'message': {
                        'text': 'We are currently working on this feature.',
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