from django.shortcuts import render
from django.http import HttpResponse
from django.views import generic
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import json
import re
import random
import requests


# Create your views here.
VERIFY_TOKEN="27thSeptember2016"

PAGE_ACCESS_TOKEN="EAAPmlEHMYHgBAFRvX0h5a6Pcw0ZBRWYUkKTNQGUFnjf5vMvaskRue5ZAzAOZBob8R5e07FB723ZBaPsFgaERCE3x1qOY5sZB78lB7zlaLOFB19mTyFNUJJu4eg4HSXXyTLEpubYS64I3kkg5Eua7P7MAAELZCRn6v48Y3Yt5TePQZDZD"

def index(request):
	output_text=find()
	return HttpResponse(output_text,content_type='application/json')

def post_facebook_message(fbid,message_text):
	post_message_url = 'https://graph.facebook.com/v2.6/me/messages?access_token=%s'%PAGE_ACCESS_TOKEN
	text,image_url,url_info=find(message_text)

	try:
		if len(text) > 315:
			text = text[:315] + ' ...'
	except KeyError:
		text = ''

	response_msg_generic={
	    "recipient":{
	        "id":fbid 
	      },
	      "message":{
	        "attachment":{
	          "type":"template",
	          "payload":{
	            "template_type":"generic",
	            "elements":[
	              {
	                "title":"ok",
	                "item_url":"whateever",
	                "image_url":image_url,
	                "subtitle":"Nostalgia",
	                "buttons":[
	                  {
	                    "type":"web_url",
	                    "url":url_info,
	                    "title":"View Website"
	                  },
	                  {
	                    "type":"postback",
	                    "title":"Start Chatting",
	                    "payload":"DEVELOPER_DEFINED_PAYLOAD"
	                  }              
	                ]
	              }
	            ]
	          }
	        }
	      }
	

	}
	response_msg_generic=json.dumps(response_msg_generic)

	#response_msg = json.dumps({"recipient":{"id":fbid}, "message":{"text":text}})
	status=requests.post(post_message_url, headers={"Content-Type": "application/json"},data=response_msg_generic)
	print status.json()
	



def find(title="girls"):
	url="http://api.tvmaze.com/singlesearch/shows?q=%s"%(title)
	resp = requests.get(url=url).text
	data = json.loads(resp)
	scoped_data=data["summary"]
	image_url=data["image"]["medium"]
	url_info=data['url']
	
	return scoped_data,image_url,url_info

class MyChatBotView(generic.View):
    def get(self,request,*args,**kwargs):
        if self.request.GET['hub.verify_token']==VERIFY_TOKEN:
            return HttpResponse(self.request.GET['hub.challenge'])
        else:
            return HttpResponse('oops invalid token')

    @method_decorator(csrf_exempt)
    def dispatch(self,request,*args,**kwargs):
        return generic.View.dispatch(self,request,*args,**kwargs)

    def post(self,request,*args,**kwargs):
		incoming_message=json.loads(self.request.body.decode('utf-8'))
		print incoming_message

		for entry in incoming_message['entry']:
			for message in entry['messaging']:
				print message
				try:
					sender_id = message['sender']['id']
					message_text = message['message']['text']
					post_facebook_message(sender_id,message_text) 
				except Exception as e:
					print e
					pass

		return HttpResponse() 




