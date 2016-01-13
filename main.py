import pygame
from time import sleep
pygame.init() #inizializzazione pygame

#inserimento font
font=pygame.font.Font('pixeldeb.ttf',40)
font_piccolo=pygame.font.Font('pixeldeb.ttf',18)

#caricamento musica
pygame.mixer.music.load('musica.ogg')
pygame.mixer.music.play(-1)

#gestione FPS
FPS=20
clock=pygame.time.Clock()

dim_schermo=[480,280]
#definizioni colori
BIANCO=(255,255,255)
NERO=(0,0,0)
VERDE=(0,255,0)
COBALTO=(61,89,171)
BLU=(0,0,255)
GIALLO=(255,255,0)
ARANCIONE=(255,128,0)
ROSSO=(238,44,44)
GRIGIO=(81,81,81)
		
schermataGioco=pygame.display.set_mode(dim_schermo,0,32)
pygame.display.set_caption('Frogger by pingumen96')

#inizializzazione dati P1
P1_x=200 #coordinata x P1
P1_y=240 #coordinata y P1
vite=3
punteggio=0

#pausa on/off
pausa=False

#classe del nemico, i parametri servono a piazzarlo nella schermata e stabilire la velocità di movimento (che sale finendo il livello)
class Nemico():
	def __init__(self, x,y,largh_nem,alt_nem,velocita,colore,senso):
		self.x=x
		self.y=y
		self.larghezza=largh_nem
		self.altezza=alt_nem
		self.velocita=velocita
		self.colore=colore
		self.senso=senso
		self.elemento=pygame.Rect(self.x,self.y,self.larghezza,self.altezza)

n_livello=0
lista_nemici=[]
def generazione_livello(livello):
	#creazione livello, da continuare
	lista_nemici[0:len(lista_nemici)]=[]
	lista_nemici.append(Nemico(0,200,70,40,1+livello,VERDE,'sinistra'))
	lista_nemici.append(Nemico(160,200,70,40,1+livello,VERDE,'sinistra'))
	lista_nemici.append(Nemico(320,200,70,40,1+livello,VERDE,'sinistra'))
	lista_nemici.append(Nemico(40,160,100,40,2+livello,BLU,'destra'))
	lista_nemici.append(Nemico(300,160,100,40,2+livello,BLU,'destra'))
	lista_nemici.append(Nemico(160,120,60,40,3+livello,GIALLO,'sinistra'))
	lista_nemici.append(Nemico(340,120,60,40,3+livello,GIALLO,'sinistra'))
	lista_nemici.append(Nemico(0,120,60,40,3+livello,GIALLO,'sinistra'))
	lista_nemici.append(Nemico(0,80,120,40,1+livello,ARANCIONE,'destra'))
	lista_nemici.append(Nemico(30,40,75,40,4+livello,ROSSO,'sinistra'))
	lista_nemici.append(Nemico(30,40,75,40,4+livello,ROSSO,'destra'))

generazione_livello(n_livello)

fine_gioco=False

def get_vite_testo():
	asterischi=''
	for i2 in range(0,vite):
		asterischi+='*'
	return asterischi

#gestione punteggio
y_temp=0

while not fine_gioco:
	#gestione FPS
	clock.tick(FPS)
	schermataGioco.fill(NERO)

	#controllo vite e punteggio
	if vite==0:
		hud_gioco_finito=font.render('GAME OVER',False,BIANCO)
		n_livello=0
		generazione_livello(n_livello)
		punteggio=0
		schermataGioco.blit(hud_gioco_finito,(100,120))
		hud_nuova_partita=font_piccolo.render('Premi N per riniziare',False,BIANCO)
		schermataGioco.blit(hud_nuova_partita,(10,240))
		#vite=3
	else:
		#gestione HUD
		hud_vite=font.render('VITE: '+get_vite_testo(),False,BIANCO)
		schermataGioco.blit(hud_vite,(0,5))
		hud_punteggio=font.render(str(punteggio),False,BIANCO)
		schermataGioco.blit(hud_punteggio,(400,5))

		if not pausa: #se c'è la pausa tutto deve stare fermo
			#inizializzazione oggetti
			P1=pygame.Rect(P1_x,P1_y,40,40)


			#controllo per aggiornare livello se necessario
			if P1.top<20:
				n_livello+=1
				generazione_livello(n_livello)
				P1_x=200; P1_y=240
				punteggio+=20
				sleep(1)
				pass
			#gestione nemici
			for i in range(0,len(lista_nemici)):
				if lista_nemici[i].elemento.colliderect(P1): #se si viene investiti si riparte da capo e si perde una vita
					P1_x=200; P1_y=240
					vite-=1
					sleep(0.5)
				if lista_nemici[i].senso=='destra':
					if lista_nemici[i].elemento.left>=480:
						lista_nemici[i].elemento.left=0
					else:
						lista_nemici[i].elemento.left+=lista_nemici[i].velocita
				elif lista_nemici[i].senso=='sinistra':
					if lista_nemici[i].elemento.right<=0:
						lista_nemici[i].elemento.right=480
					else:
						lista_nemici[i].elemento.right-=lista_nemici[i].velocita
				pygame.draw.rect(schermataGioco,lista_nemici[i].colore,lista_nemici[i].elemento)
			#gestione elementi su schermo
			pygame.draw.rect(schermataGioco,BIANCO,P1) #P1 viene disegnato su schermataGioco
		else:
			hud_pausa=font.render('PAUSA',False,BIANCO)
			schermataGioco.blit(hud_pausa,(150,120))
				


	
	#gestione eventi input
	for event in pygame.event.get():
		if event.type==pygame.QUIT:
			fine_gioco=True
		if event.type==pygame.KEYDOWN:
			if event.key==pygame.K_p and pausa==False:
				pausa=True
			elif event.key==pygame.K_p and pausa==True:
				pausa=False
			if event.key==pygame.K_UP and P1.top>0:
				P1_y-=40
			if event.key==pygame.K_DOWN and P1.bottom<dim_schermo[1]:
				P1_y+=40
			if event.key==pygame.K_LEFT and P1.left>0:
				P1_x-=40
			if event.key==pygame.K_RIGHT and P1.right<dim_schermo[0]:
				P1_x+=40
			if event.key==pygame.K_n and vite==0:
				vite=3

	pygame.display.update()
