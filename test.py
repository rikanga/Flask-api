import requests, json

url = "https://api.orange.com/oauth/v3/token"

headers = {
	"Authorization":"Basic U20yQ0luMmhzUUdBVjlIWU45cUVaVnlpa1JyczlkZnM6aGxDeWhMY0FKWkNFN0hIRg==",
	"Content-Type":"application/x-www-form-urlencoded",
	"Accept":"application/json"
}

data = {"grant_type":"client_credentials"}

req = requests.post(url, headers=headers, data=data)
print(req.json())

class SendSMS:
	def __init__(self, auth_token):
		self.url = 'https://api.orange.com/oauth/v3/token'
		self.auth_token = auth_token
	
	def login(self):
		headers = {
			'Authorization':self.auth_token,
			'Content-type':"application/x-www-form-urlencoded",
			"Accept":"application/json"
			}
			
		data = {"grant_type":'client_credentials'}
		response = requests.post(self.url, headers=headers, data=data)
		return response.json()

	def send(self, from_, to, message):
		#from_url = from_.split('+')[1]
		url = "https://api.orange.com/smsmessaging/v1/outbound/tel%3A%2B{}/requests".format(from_)
		login_data = self.login()
		
		headers = {
			'Authorization':"Bearer " + login_data['access_token'],
			'Content-Type':'application/json'}
		data = {
			'outboundSMSMessageRequest':{
				"address":"tel:+" + to,
				'senderAddress':"tel:+" + from_,
				'outboundSMSTextMessage':{'message':message}
				}
			}
		data = json.dumps(data)
		response = requests.post(url, headers=headers, data=data)
		return (response)
			
					
			
sms = SendSMS(auth_token="Basic RWhJd2dqajN3WTVGQ1I4aTEzMDFDSEdHdTgxWkZkZUc6Y1pyRHlwUkF3MUFGaGlmMg==")
print(sms.send(from_="243895371268", to="243815941630", message='Bonjour Ir Richard Kangamba'))
