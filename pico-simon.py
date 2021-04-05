# pico-simon
import utime, random
import picodisplay as display

# Set up and initialise Pico Display
buf = bytearray(display.get_width() * display.get_height() * 2)
display.init(buf)
display.set_backlight(0.8)

WHITE=display.create_pen(255, 255, 255)
BLACK=display.create_pen(0,0,0)
RED=display.create_pen(255,0,0)
GREEN=display.create_pen(0,255,0)
BLUE=display.create_pen(0,0,255)
YELLOW=display.create_pen(255,255,0)
rwidth=120
rheight=67
rect=[ {"x": 0, "y": 0}, {"x": 120, "y": 0}, {"x": 0, "y": 68}, {"x": 120, "y": 68} ]
rpen=[ RED, YELLOW, BLUE, GREEN ]
sleep=0.5
best=0
#
def clearDisplay():
    display.set_pen(BLACK)  
    display.clear()           
    display.update()
#
def menu():
    display.set_led(0,0,0)
    display.set_pen(BLACK)  
    display.clear()           
    display.set_pen(WHITE)  
    display.text("Press any button!", 10, 10, 240, (3,6)[best==0])  
    if best > 0:
        display.text("Hiscore: " + str(best), 10, 68, 240, 3)
    display.update()          # Update the display  
    while True:
        if display.is_pressed(display.BUTTON_A) or display.is_pressed(display.BUTTON_B) or display.is_pressed(display.BUTTON_X) or display.is_pressed(display.BUTTON_Y):
            return
        utime.sleep(0.5)
#
def play():
    count=0
    seq=[]
    while True:
        seq.append(random.randint(0,3))
        for i in seq: # display the sequence
            clearDisplay()
            utime.sleep(0.5)
            display.set_pen(rpen[i]) 
            display.rectangle(rect[i]["x"],rect[i]["y"],rwidth,rheight)  
            display.update()          
            utime.sleep(sleep)
        clearDisplay()
        for i in seq: # get buttons for the sequence
            b=getButton()
            display.set_pen(rpen[b]) 
            display.rectangle(rect[b]["x"],rect[b]["y"],rwidth,rheight)  
            display.update()          
            if b != i:
                display.set_led(255,0,0)
                utime.sleep(2)
                display.set_led(0,0,0)
                return len(seq)-1
            display.set_led(0,255,0)
            utime.sleep(1)
            display.set_led(0,0,0)
            clearDisplay()
def getButton():
    while True:
        if display.is_pressed(display.BUTTON_A):
            return 0
        if display.is_pressed(display.BUTTON_B):
            return 2
        if display.is_pressed(display.BUTTON_X):
            return 1
        if display.is_pressed(display.BUTTON_Y):
            return 3
        utime.sleep(0.1)
#
def failed():
    global best
    display.set_pen(RED)
    display.clear()        
    display.set_pen(YELLOW)
    display.text("Game Over!", 10, 10, 240, 6)  # Add some text
    display.update()          # Update the display
    utime.sleep(1)
    display.set_pen(RED)
    display.clear()
    display.set_pen(YELLOW)
    display.text("Score: " + str(score), 10, 10, 240, 3) 
    if score > best:
        display.text("New Hiscore!", 10, 68, 240, 3)
        best=score
    else:
        display.text("Hiscore: " + str(best), 10, 68, 240, 3)
    display.update()          # Update the display
    utime.sleep(3)
#
while True:
    menu()
    score=play()
    failed()
###fin