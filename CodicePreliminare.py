#Batterie vanno rimosse dal robot quando non è in uso
#Batterie vanno tenute in carica fin tanto che siamo in classe
#PROTOCOLLO

#Richieste da client a server con risposta di conferma o eventuali anomalie
        #richieste  -->  (f"{command}|{value}")
        #risposte   -->  (f"{status}|{phrase}")

#Comandi:
'''     forward
        backward
        left
        right
'''
#Status:
'''     ok
        error
'''