# Typeactor object 1

# The object for the first request is just a simple result
# The object for the second request is another simple result 
# The object for the third request is an audio file 
import json

class typeactor(object):
	def __init__(self, speak_urls: str, result: str): 	
		self.speak_urls = speak_urls
		self.result = result

def main():
	print('testing')
	user = typeactor(speak_urls="https://typecast.ai/api/speak/6234eac7b2559539e98a4012", result="$oid")
	json_data = json.dumps(user.__dict__)
	print(json_data)
