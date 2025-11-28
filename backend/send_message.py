from twilio.rest import Client

account_sid = 'AC61bebf1f475ccc302eca0877a97e1c94'
auth_token = '79d73470d4a2ce158cd366c3252a7c3d'
client = Client(account_sid, auth_token)

message = client.messages.create(
  from_='whatsapp:+14155238886',
  content_sid='HXb5b62575e6e4ff6129ad7c8efe1f983e',
  content_variables='{"1":"10/1","2":"4pm"}',
  to='whatsapp:+919650379396'
)

print(message.sid)