import twitter
import urlparse
import oauth2 as oauth
import unicodedata
import re
import random
import sys

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
with open("twts.txt", "r+") as file:
    for line in file:
        linelist.append(line.replace("\n",""))

friends = api.GetFriends()
actualizar = raw_input('Desea actualizar los logs de tweets? (S/N)')
if actualizar == 's':
    print "Actualizando log de tweets.",
    for friend in friends:
        tweets = api.GetUserTimeline(id=friend.id,count=100)
        sys.stdout.write(".")
        sys.stdout.flush()
        f = open('twts.txt','a')
        for tweet in tweets:
            ## como hay tweets que tienen simbolos no ascii que no se puede imprimir por pantalla, esta funcion de unicode le quita esos simbolos raros.
            tweet.text=unicodedata.normalize('NFKD', tweet.text).encode('ascii','ignore')
            tweet.user=unicodedata.normalize('NFKD', tweet.user.name).encode('ascii','ignore')
            rxp = "http.*"
			## REGEXP PARA ELIMINAR https!
            tweet.text = re.sub(rxp,"",tweet.text)
            if tweet.text not in linelist:
                f.write(tweet.text)
                f.write('\n')

    print "Listo!"
separador = "\n" #Nunca aparecera en una palabra, asi que sera el registro vacio.
finoracion = (".", "!", "?", "\n") #Nueva finoracion si se encuentra al final de un string. 
seplinea  = "\n" #String used to seperate sentences

# TABLA:
w1 = separador
w2 = separador
table = {}

#Archivo con logs:
with open("twts.txt") as file:
    for line in file:
        for word in line.split():
            if word[-1] in finoracion:
                table.setdefault( (w1, w2), [] ).append(word[0:-1])
                w1, w2 = w2, word[0:-1]
                word = word[-1]
            table.setdefault( (w1, w2), [] ).append(word)
            w1, w2 = w2, word
# Marca el final del archivo 
table.setdefault( (w1, w2), [] ).append(separador)

# GENERA SECUENCIA DE OUTPUT
maxfinoraciones  = 9

w1 = separador
w2 = separador
sentencecount = 0
sentence = []
words = 0
log = []

## ALGORITMO:
## CADENAS DE MARKOV
## Sistema matematico que se transforma de un estado al otro,
## con la propiedad de que el estado siguiente depende solo
## de el estado actual, y no de los estados pasados.
##
## Estados: palabras
## Estado actual: Ultimas dos palabras
##
## Se almacenan en una tabla valores [(p1, p2), px, py, pz...]
## donde (p1, p2) son un par de palabras, y px, py, y pz son
## posibles continuaciones leidas en algun tweet.
## Los estados siguientes solo dependen de las dos ultimas
## palabras, lo que puede llevar a resultados interesantes.

print "%d. " % (sentencecount+1),
while sentencecount < maxfinoraciones:
    if(words < 24):
        newword = random.choice(table[(w1, w2)])
        if newword == separador: sys.exit()
        if newword in finoracion:
            print "%s%s%s" % (" ".join(sentence), newword, seplinea)
            log.append(" ".join(sentence))
            sentence = []
            sentencecount += 1
            print "%d." % (sentencecount+1),
        else:
            sentence.append(newword)
        w1, w2 = w2, newword
        words += 1
    else:
        words = 0
        print "%s%s%s" % (" ".join(sentence), newword, seplinea)
        log.append(" ".join(sentence))
        sentence = []
        sentencecount += 1
        print "%d." % (sentencecount+1),
postear = raw_input('Desea postear un mensaje? (1-9/0 para salir)')
if postear != '0':
    api.PostUpdate(status=log[int(postear)-1])
