import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)




def getDistance():
    TRIG = 20
    GPIO.setup(TRIG,GPIO.OUT)
    ECHO = 21
    GPIO.setup(ECHO,GPIO.IN)
    i = 0
    verification = False
    avgDistance = 0
   
    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)
    while GPIO.input(ECHO)==0:
        pulse_start = time.time()

    while GPIO.input(ECHO)==1:
        pulse_end = time.time()
        pulse_duration = pulse_end - pulse_start
        distance = pulse_duration * 17150
        distance = round(distance,2)
        

    return distance





import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

#verification = False


#def test():
    #print("test")

def Distance():
    #print("dis")
    TRIG = 20
    GPIO.setup(TRIG,GPIO.OUT)
    ECHO = 21
    GPIO.setup(ECHO,GPIO.IN)
    i = 0
    verification = False
    avgDistance = 0
    
    avgDistance=0

    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)
    while GPIO.input(ECHO)==0:
        pulse_start = time.time()

    while GPIO.input(ECHO)==1:
        pulse_end = time.time()

    pulse_duration = pulse_end - pulse_start

    distance = pulse_duration * 17150
    distance = round(distance,2)
    avgDistance=avgDistance+distance
    
    return avgDistance

def calcDistance():
    
    a =0
    TRIG = 20
    GPIO.setup(TRIG,GPIO.OUT)
    ECHO = 21
    GPIO.setup(ECHO,GPIO.IN)
    PWM = 18
    GPIO.setup(PWM,GPIO.OUT)
    p=GPIO.PWM(PWM,1000)
    p.start(0)
    GPIO.setup(ECHO,GPIO.IN)
    i = 0
    distance=getDistance()
    
    if distance > 150:
        distance = 150
    else:
        distance = distance
    
    percentage=(distance/150)*100
    DutyCycle=percentage/1.35
    #print(DutyCycle)
    
    print("Distance:"+str(distance)+"cm, DutyCycle:"+str(DutyCycle))
    p.ChangeDutyCycle(DutyCycle)
    
    return distance
    #time.sleep(0.5)
