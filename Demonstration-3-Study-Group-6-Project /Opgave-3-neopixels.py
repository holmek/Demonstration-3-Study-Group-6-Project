import umqtt_robust2 as mqtt
from neopixel import NeoPixel
from machine import Pin
from time import sleep
import time
from machine import PWM
import re

# Her kan i placere globale varibaler, og instanser af klasser
# HEX CONVERTER START --↓---↓---↓---↓---↓---↓---↓---↓---↓---↓---↓---↓---↓---↓---↓---↓
def valid_hex_color(color_code_str:str):
    # Regex til at tjekke valid HEX farvekoder.
    regex = "^#"+"[a-f0-9]"*6
    # Hvis streng er tom retuneres false.
    if(color_code_str == None):
        return False
    # Hvis strengen macher RegEx returneres værien.
    if(re.search(regex, color_code_str)):
        return True
    else:
        return False

# Test Case 1.
#str1 = "#ffffff"
#print(str1, ":", valid_hex_color(str1))

# Test Case 2.
#str2 = "#F00"
#print(str2, ":", valid_hex_color(str2))


# HEX CONVERTER END ↑---↑---↑---↑---↑---↑---↑---↑---↑---↑---↑---↑---↑---↑---↑---↑---↑

pb1 = Pin(4, Pin.IN)
pb2 = Pin(0, Pin.IN)

BUZZ_PIN = 26
buzzer_pin = Pin(BUZZ_PIN, Pin.OUT)
pwm_buzz = PWM(buzzer_pin)

def buzzer(buzzer_PWM_object, frequency, sound_duration, silence_duration):
    buzzer_PWM_object.duty(512)
    buzzer_PWM_object.freq(frequency)
    sleep(sound_duration)
    buzzer_PWM_object.duty(0)
    sleep(silence_duration)


n = 12
p = 26
np = NeoPixel(Pin(p, Pin.OUT), n)

# Øvelse 3.1 

#np[0] = (0, 10, 0)
#np[1] = (0, 10, 0)
#np[2] = (0, 10, 0)
#np[3] = (0, 0, 10) 
#np[4] = (0, 0, 10)
#np[5] = (0, 0, 10)
#np[6] = (10, 0, 0)
#np[7] = (10, 0, 0)
#np[8] = (10, 0, 0)
#np[9] = (10, 10, 0)
#np[10] = (10, 10, 0)
#np[11] = (10, 10, 0)
np.write()

def clear():
    for i in range(n):
        np[i] = (0, 0, 0)
    np.write()

def set_color(r, g, b):
    for i in range(n):
        np[i] = (r, g, b)
        np.write()
        
# Øvelse 3.2 -        
for i in range(3):
    set_color(10, 0, 0)  
    sleep(0.3)
    clear()  
    sleep(0.3)

# Øvelse 3.3
def fade_in_out(color, wait):
    for i in range(0, 4 * 256, 8):
        for j in range(n):
            if (i // 256) % 2 == 0:
                val = i & 0xff
            else:
                val = 255 - (i & 0xff)
                if color == 'red':
                  np[j] = (val, 0, 0)
                elif color == 'green':
                  np[j] = (0, val, 0)
                elif color == 'blue':
                  np[j] = (0, 0, val)
                elif color == 'purple':
                  np[j] = (val, 0, val)
                elif color == 'yellow':
                  np[j] = (val, val, 0)
                elif color == 'teal':
                  np[j] = (0, val, val)
                elif color == 'white':
                  np[j] = (val, val, val)
            np.write()
        time.sleep_ms(wait)
    
#fade_in_out('red', 0)
#fade_in_out('green', 10)
#fade_in_out('blue', 25)
#fade_in_out('purple', 10)
#fade_in_out('yellow', 10)
fade_in_out('teal', 10)
#fade_in_out('white', 10)
time.sleep(1)

# bounce
def bounce(r, g, b, wait):
  for i in range(4 * n):
      for j in range(n):
          np[j] = (r, g, b)
      if (i // n) % 2 == 0:
          np[i % n] = (0, 0, 0)
      else:
        np[n - 1 - (i % n) ] = (0, 0, 0)
      np.write()
      time.sleep_ms(wait)
      
#bounce(255, 0, 125, 50)
time.sleep(1)

# function to go through all colors
def wheel(pos):
    if pos < 0 or pos >255:
        return (0, 0, 0)
    if pos < 85:
        return (255 - pos * 3, pos * 3, 0)
    if pos < 170:
        pos -= 85
        return (0, 255 - pos * 3, pos * 3)
    pos -=170
    return (pos * 3, 0, 255 - pos * 3)

# rainbow
def rainbow_cycle(wait):
    for j in range(255):
        for i in range(n):
            rc_index = (i * 256 // n) + j
            np[i] = wheel(rc_index & 255)
        np.write()
        time.sleep_ms(wait)
        
#rainbow_cycle(2)
#rainbow_cycle(1)
time.sleep(1)

#turn off all pixels
def clear():
    for i in range(n):
        np[i] = (0, 0, 0)
        np.write()
        
clear()
    
# Øvelse 3.3 SLUT ------------------------------------------------------
    
    
while True:
    try:
                
        # Øvelse 3.4 start ----------------------------------------------
        
        if mqtt.besked == "a":
               print("Spiller tone a!")
               buzzer(pwm_buzz, 262, 0.2, 0.2)
               rainbow_cycle(5) # animationen rainbow
               
        if mqtt.besked == "b":
               print("Spiller tone b!")
               buzzer(pwm_buzz, 294, 0.4, 0.3)
               bounce(255, 0, 125, 50) # animationen "bounce"
               
        # Øvelse 3.4 Slut ----------------------------------------------

        # Øvelse 3.5 Start ----------------------------------------------
        
        if mqtt.besked == "start rainbow":
            print("Animation rainbown er startet")  
            rainbow_cycle(5) # animationen rainbow
        
        if mqtt.besked == "start bounce":
            print("Animation bounce er startet")
            bounce(255, 0, 125, 50) # animationen "bounce"
        
        # Øvelse 3.5 Slut ----------------------------------------------
        


        if len(mqtt.besked) != 0: # Her nulstilles indkommende beskeder
            mqtt.besked = ""
            clear()
            time.sleep
            
        mqtt.sync_with_adafruitIO() # igangsæt at sende og modtage data med Adafruit IO             
        #sleep(1) # Udkommentér denne og næste linje for at se visuelt output
        #print(".", end = '') # printer et punktum til shell, uden et enter        
    
    except KeyboardInterrupt: # Stopper programmet når der trykkes Ctrl + c
        print('Ctrl-C pressed...exiting')
        mqtt.c.disconnect()
        mqtt.sys.exit()