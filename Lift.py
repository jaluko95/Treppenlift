try:
	import RPi.GPIO as GPIO
	import time 
	#import threading
	#import multiprocessing
	
	GPIO.setmode(GPIO.BCM)
	
	
	motor1_richtung = 22 #low/high = hoch/runter
	motor1_v = 27 # 80/100
	motor1_standby = 10 #high = standby
	GPIO.setup(motor1_richtung, GPIO.OUT)
	GPIO.setup(motor1_v, GPIO.OUT)
	GPIO.setup(motor1_standby, GPIO.OUT)
	GPIO.output(motor1_standby, GPIO.HIGH)# default standby
	motor1_pwm = GPIO.PWM(motor1_v, 80)

	motor2_richtung = 20
	motor2_v = 16
	motor2_standby = 12
	GPIO.setup(motor2_richtung, GPIO.OUT)
	GPIO.setup(motor2_v, GPIO.OUT)
	GPIO.setup(motor2_standby, GPIO.OUT)
	GPIO.output(motor2_standby, GPIO.HIGH)#default standby
	
	grenze_fahrtweg = 13 #NC
	positionsgeber_unten = 5
	positionsgeber_oben = 6 
	GPIO.setup(grenze_fahrtweg, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
	GPIO.setup(positionsgeber_unten, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
	GPIO.setup(positionsgeber_oben, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)

	drehanschlag_links = 23 #NC
	drehanschlag_rechts = 8
	GPIO.setup(drehanschlag_links, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
	GPIO.setup(drehanschlag_rechts, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
		
	sensoren = 25# 3,3V wenn weg frei. 0V wenn Taster betaetigt
	GPIO.setup(sensoren, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
	
	sound = 17 #High = standby
	GPIO.setup(sound, GPIO.OUT)
	GPIO.output(sound, GPIO.HIGH)# default standby

	bremse = 4 #High/Gnd= bremse aktiv/ low= bremse offen
	GPIO.setup(bremse, GPIO.OUT)
	GPIO.output(bremse, GPIO.HIGH)#default aktiv

	buzzer = 14
	GPIO.setup(buzzer, GPIO.OUT)

	schloss = 15# 3,3V = an
	GPIO.setup(schloss, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)

	schalter_hoch = 24 #NO
	schalter_runter = 9
	GPIO.setup(schalter_hoch, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
	GPIO.setup(schalter_runter, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
	
	def beep():
		GPIO.output(buzzer, GPIO.HIGH)
		time.sleep(0.15)
		GPIO.output(buzzer, GPIO.LOW)
	
	def start():
		beep()

		#H-Brücke "wecken"
		GPIO.output(motor1_standby, GPIO.LOW)
		GPIO.output(bremse, GPIO.LOW) #Bremse lösen
		time.sleep(0.5)
		
		#langsam anfahren
		motor1_pwm.start(20)
		for dc in range(21, 100):
			motor1_pwm.ChangeDutyCycle(dc)
			time.sleep(0.002)

	def stop(): #langsam anhalten
		for dc in range(100, 20, -1):
			motor1_pwm.ChangeDutyCycle(dc)
			time.sleep(0.002)
		motor1_pwm.stop()
		
		GPIO.output(motor1_standby, GPIO.HIGH) #H-Brücke in Standby versetzen
		GPIO.output(bremse, GPIO.HIGH) #bremse festsetzen
		
	def notstop():
		motor1_pwm.stop()
		GPIO.output(bremse, GPIO.HIGH)
		GPIO.output(motor1_standby, GPIO.HIGH)

	def lift(schalter, richtung):
		
		#fahrtichtung festlegen
		positionsgeber = "null"
		if richtung == GPIO.HIGH: #nach unten fahren
			positionsgeber = positionsgeber_oben
		elif richtung == GPIO.LOW: #nach oben fahren
			positionsgeber = positionsgeber_unten
		
		GPIO.output(motor1_richtung, richtung) #Fahrtrichtung einstellen
		start() #losfahren
		
		#solange "Fahren-Taste" gedrückt wird und alle Sensoren "weg ist frei" sagen und der Lift noch nicht am Ziel angekommen ist:
		while GPIO.input(schalter) == 1 and GPIO.input(sensoren) == 1 and GPIO.input(positionsgeber) == 1:
			time.sleep(0.05) #Auf 20 Abfragen pro Sekunde reduzieren
		
		if GPIO.input(schalter) == 0: #wenn "Fahren-Taste" nicht mehr gedrückt wird
			stop()
		elif GPIO.input(positionsgeber_unten) == 0 or GPIO.input(positionsgeber_oben) == 0: #wenn der Lift oben oder unten angekommen ist
			stop()
		elif GPIO.input(sensoren) == 0: #Wenn einer der Sensoren ein Hindernis feststellt:
			notstop()

	while True: #Prüfe ob die "Fahren-Taste" gedrückt wird 
		if GPIO.input(schalter_hoch) == 1 or GPIO.input(schalter_runter) == 1:
			time.sleep(0.75) #"Fahren-Taste" muss mindestens 3/4s gedrückt werden
			if GPIO.input(schalter_hoch) == 1 and GPIO.input(sensoren) == 1: #prüfe vor Fahrtbeginn ob alle Sensoren "Der Weg ist frei" sagen
				if GPIO.input(positionsgeber_unten) == 0: #Wenn 0, dann Stromkreis offen - Taster gedrückt = Lift steht unten
					#hochfahren
					lift(schalter_hoch, GPIO.HIGH)
						
				elif GPIO.input(positionsgeber_oben) == 0: #Wenn 0, dann Stromkreis offen - Taster gedrückt = Lift steht oben
					#nichts, lift ist bereits oben
				
				elif GPIO.input(positionsgeber_unten) == 1 and GPIO.input(positionsgeber_oben) == 1: #weder oben noch unten
					#hochfahren
					lift(schalter_hoch, GPIO.HIGH)
			
				
			elif GPIO.input(schalter_runter) == 1 and GPIO.input(sensoren) == 1:
				if GPIO.input(positionsgeber_oben) == 0:
					#nach links drehen
					lift(schalter_runter, GPIO.LOW)
				elif GPIO.input(positionsgeber_unten) == 0:
					#nichts, lift ist bereits unten
					
				elif GPIO.input(positionsgeber_unten) == 1 and GPIO.input(positionsgeber_oben) == 1: #weder oben noch unten
					#runterfahren
					lift(schalter_runter, GPIO.LOW)
		time.sleep(0.1) #MC entlasten

except Exception as e:
	print(e)

finally:
	GPIO.cleanup()
