import RPi.GPIO as GPIO
from time import sleep

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

class Motor():
	def __init__(self, EnaA, In1A, In2A, EnaB, In1B, In2B):
		self.EnaA = EnaA
		self.In1A = In1A
		self.In2A = In2A
		self.EnaB = EnaB
		self.In1B = In1B
		self.In2B = In2B
		GPIO.setup(self.EnaA, GPIO.OUT)
		GPIO.setup(self.In1A, GPIO.OUT)
		GPIO.setup(self.In2A, GPIO.OUT)
		GPIO.setup(self.EnaB, GPIO.OUT)
		GPIO.setup(self.In1B, GPIO.OUT)
		GPIO.setup(self.In2B, GPIO.OUT)
		self.pwmA = GPIO.PWM(self.EnaA, 100);
		self.pwmA.start(0)
		self.pwmB = GPIO.PWM(self.EnaB, 100);
		self.pwmB.start(0)
		print("init completed")
		
	def move(self, speed = 0.5, turn = 0, t = 0):
		speed *= 80
		turn *= 80
		leftSpeed = speed - turn
		rightSpeed = speed + turn
		if leftSpeed > 80: leftSpeed = 80
		elif leftSpeed < -80: leftSpeed = -80
		if rightSpeed > 80: rightSpeed = 80
		elif rightSpeed < -80: rightspeed = -80
		#print("left speed" + str(leftSpeed))
		#print("right speed" + str(rightSpeed))
		self.pwmA.ChangeDutyCycle(abs(leftSpeed))
		self.pwmB.ChangeDutyCycle(abs(rightSpeed))
		
		if leftSpeed > 0:
			GPIO.output(self.In1A, GPIO.HIGH)
			GPIO.output(self.In2A, GPIO.LOW)
		else:
			GPIO.output(self.In1A, GPIO.LOW)
			GPIO.output(self.In2A, GPIO.HIGH)
			
		if rightSpeed > 0:
			GPIO.output(self.In1B, GPIO.HIGH)
			GPIO.output(self.In2B, GPIO.LOW)
		else:
			GPIO.output(self.In1B, GPIO.LOW)
			GPIO.output(self.In2B, GPIO.HIGH)
			
		sleep(t)
		
	def stop(self, t = 0):
		self.pwmA.ChangeDutyCycle(0)
		self.pwmB.ChangeDutyCycle(0)
		sleep(t)
