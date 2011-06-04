import twitter
import urlparse
import oauth2 as oauth
import unicodedata
import re
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

## conecta el programa con la cuenta de twitter linkeada mediante los consumer y access tokens.
api = twitter.Api(consumer_key=consumer_key, consumer_secret=consumer_secret, access_token_key=access_token, access_token_secret=access_secret)
timeline = api.GetFriendsTimeline(count=100) ## obtiene el timeline de la cuenta linkeada.
linelist = []
with open("twts.txt") as file:
	for line in file:
		linelist.append(line.replace("\n",""))

f = open('twts.txt','a')
for tweet in timeline:
	## como hay tweets que tienen simbolos no ascii que no se puede imprimir por pantalla, esta funcion de unicode le quita esos simbolos raros.
	tweet.text=unicodedata.normalize('NFKD', tweet.text).encode('ascii','ignore')
	tweet.user=unicodedata.normalize('NFKD', tweet.user.name).encode('ascii','ignore')
	rxp = "http.*"
	tweet.text = re.sub(rxp,"",tweet.text)
	print "Por: "+tweet.user+"\n\t"+tweet.text
	if tweet.text not in linelist:
		f.write(tweet.text)
		f.write('\n')
