import requests
import urllib3
import facebook
import json

app_id = '533916530673968'
app_secret = 'fc03d0f96f30c5a851b1a9ee644c622f'

token = 'EAAHlmCEmiTABAF7UZA31ZAP5pDI0F2nIVfyZCqqFgZAeg1yCCgEYwX9qdPZCl4jwAbCdaPPgQkQoiB46mavsNuvcqhdSnL3jvfRA8xZBmv86OoND1uzTFC7p5eBrL3OwdqEfenx8A5TWXUEz6GgrbKpzKICAwHZCAwMn1s4iksvZCAZDZD'

def sonet(token):

	graph = facebook.GraphAPI(access_token=token)
	# print dir(graph)


	# profile = graph.get_object('me')
	# page_name = raw_input("Enter a page name: ")
	# fields = ['id','name','about','likes','link','band_members']
	# fields = ','.join(fields)
	page = graph.get_object("/me")

	# q = graph.get_connections(id='me', connection_name='friends')
	# graph.put_object(parent_object='me', connection_name='feed', message='Hello, world')
	# print q
	# graph.put_object("me", "feed", message="Posting on my wall1!")
	# net = graph.get_connections('me', 'posts', fields='message, link, created_time')
	# print json.dumps(page, indent=4)
	# print net
	print page

sonet(token)



