import json
import requests

from bottle import debug, request, route, run

GRAPH_URL = "https://graph.facebook.com/v2.6"
VERIFY_TOKEN = 'YOUR_VERIFY_TOKEN'
PAGE_TOKEN='EAAGDZANjZA9KIBADJZCAc34b64brGgA4vOxjRqqUZAADsRSvVUMWM3jPLvFufVuoZAU4H68uKYNNZAjwhdNHp6NngeBmNvQfQZBeBznvHUHRplDTSzOYc7YmgFsLiZBbOn9URtgkmdprCFzR4d4o0Ce7Hl1pR2RZCFUZAtOZAA2fiSEhQZDZD'
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
            ctx = {
                'recipient': {
                    'id': user_id,
                },
                'message': {
                    'text': message_text,
                }
            }
            response = send_to_messenger(ctx)
        return ''


debug(True)
run(reloader=True, port=8080)
