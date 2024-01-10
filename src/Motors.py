import RPi.GPIO as GPIO
import time

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

class Motor:
	def __init__(self, fr, rr, enb):
		self.fr = int(fr)
		self.rr = int(rr)
		self.enb = int(enb)
		
		GPIO.setup(self.fr, GPIO.OUT)
		GPIO.setup(self.rr, GPIO.OUT)
		GPIO.setup(self.enb, GPIO.OUT)
		
		self.enb_pwm = GPIO.PWM(self.enb, 100)
		self.pwm_val = 0
		print('Motor init successfully')
		
	def getPWM_Val(self):
		return self.pwm_val
		
	def setPWM_Val(self, val):
		self.pwm_val = val
		self.enb_pwm.ChangeDutyCycle(self.pwm_val)
		
	def moveFw(self):
		GPIO.output(self.fr, GPIO.HIGH)
		GPIO.output(self.rr, GPIO.LOW)
		
	def moveBw(self):
		GPIO.output(self.fr, GPIO.LOW)
		GPIO.output(self.rr, GPIO.HIGH)
		
	def pause(self):
		self.enb_pwm.ChangeDutyCycle(0)
		
	def speed_up(self):
		if self.pwm_val <= 90:
			val = self.pwm_val + 10
			self.setPWM_Val(val)
		
	def slow_down(self):
		if self.pwm_val >= 10:
			val = self.pwm_val - 10
			self.setPWM_Val(val)
		
	def start(self):
		self.enb_pwm.start(0)
		
	def stop(self):
		self.enb_pwm.stop()
		
