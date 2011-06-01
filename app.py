import twitter
import urlparse
import oauth2 as oauth
import unicodedata
## obtiene los consumer tokens desde el archivo consumer.txt.
consumer=open("consumer.txt","r")
consumer_key=consumer.readline()
consumer_secret=consumer.readline()
consumer.close()

## eliminamos los saltos de linea leidos del archivo, para tener los tokens limpios
consumer_key=consumer_key.replace("\n","")
consumer_secret=consumer_secret.replace("\n","")

## obtiene los access token desde el archivo consumer.txt.
tokens=open("tokens.txt","r")
access_token=tokens.readline()
access_secret=tokens.readline()
tokens.close()

## eliminamos los saltos de linea leidos del archivo, para tener los tokens limpios
access_token=access_token.replace("\n","")
access_secret=access_secret.replace("\n","")

print access_token;

## conecta el programa con la cuenta de twitter linkeada mediante los consumer y access tokens.
api = twitter.Api(consumer_key=consumer_key, consumer_secret=consumer_secret, access_token_key=access_token, access_token_secret=access_secret)

## via stdin postea un tweet a la cuenta linkeada.
tweet=raw_input("q estas pensando?\n")
api.PostUpdate(tweet)

i=1
users = api.GetFriends() ##obtiene los amigos de la cuenta linkeada.
for u in users:
	## como hay usuarios que tienen un candado y/o un signo de verificacion que no se pueden imprimir por pantalla, esta funcion de unicode le quita esos simbolos raros.
	u.name=unicodedata.normalize('NFKD', u.name).encode('ascii','ignore')
	print str(i)+"\t"+u.name
	i=i+1

i=1	
timeline = api.GetUserTimeline() ## obtiene el timeline de la cuenta linkeada.
for tweet in timeline:
	## como hay tweets que tienen simbolos no ascii que no se puede imprimir por pantalla, esta funcion de unicode le quita esos simbolos raros.
	tweet.text=unicodedata.normalize('NFKD', tweet.text).encode('ascii','ignore')
	print "tweet numero: "+str(i)+"\n\t"+tweet.text
	i=i+1
	
