import twitter
import urlparse
import oauth2 as oauth
import webbrowser
##############################################
## para que funcione, deben tener un 						##
## archivo de texto llamado "consumer.txt"			##
## donde la primera linea es el "consumer key"  	##
## y la segunda linea es el											##
## "consumer key secret" entregados por 				##
## twitter cuando se crea la aplicacion.					##
##############################################

## links entregados por twitter, son para todas las app igual.
request_token_url = 'https://api.twitter.com/oauth/request_token' 
access_token_url = 'https://api.twitter.com/oauth/access_token' 
authorize_url = 'https://api.twitter.com/oauth/authorize' 

## obtiene los consumer tokens desde el archivo consumer.txt.
consumer=open("consumer.txt","r")
consumer_key=consumer.readline()
consumer_key=consumer_key.replace("\n","")
consumer_secret=consumer.readline()
consumer_secret=consumer_secret.replace("\n","")
consumer.close()
consumer = oauth.Consumer(consumer_key, consumer_secret) 
client = oauth.Client(consumer)

## pide los valores de los tokens de solicitud.
resp, content = client.request(request_token_url, "GET") 
if resp['status'] != '200':
	raise Exception("Invalid response %s." % resp['status'])

## arma el token para la solicitud.
request_token = dict(urlparse.parse_qsl(content)) 

print "Request Token:"
print "    - oauth_token        = %s" % request_token['oauth_token']
print "    - oauth_token_secret = %s" % request_token['oauth_token_secret']
print 

## abre el WebBrowser pidiendo el codigo PIN de autorizacion.
webbrowser.open_new("%s?oauth_token=%s" % (authorize_url, request_token['oauth_token']))
print request_token['oauth_token']
accepted = 'n'
while accepted.lower() == 'n':
	accepted = raw_input('Me autorizaste? (s/n) ')
oauth_verifier = raw_input('Cual es el PIN? ')

token = oauth.Token(request_token['oauth_token'],request_token['oauth_token_secret'])
token.set_verifier(oauth_verifier) 
client = oauth.Client(consumer, token)

## pide los valores y arma el token de acceso.
resp, content = client.request(access_token_url, "POST") 
access_token = dict(urlparse.parse_qsl(content)) 

print "Access Token:"
print "    - oauth_token        = %s" % access_token['oauth_token']
print "    - oauth_token_secret = %s" % access_token['oauth_token_secret']
print
print "Ahora puedes acceder a la informacion privada con los tokens de arriba." 
print


## escribimos los valores de los tokens de autorizacion en el archivo tokens.txt
tokens=open("tokens.txt","w")
tokens.write(access_token['oauth_token'])
tokens.write("\n")
tokens.write(access_token['oauth_token_secret'])
tokens.write("\n")
tokens.close
