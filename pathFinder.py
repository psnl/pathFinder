#!/usr/bin/env python
 
import pygame
from pygame import gfxdraw
import random
import math
 
# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

#MAX_SPEED = 60 #pixels/frame
#MIN_SPEED = 15 #pixels/frame
MAX_SPEED = 30 #pixels/frame
MIN_SPEED = 15 #pixels/frame

FIELD_WIDTH = 1200
FIELD_HEIGHT = 900
MIN_ANGLE = -60
MAX_ANGLE = 60
SEARCH_RADIUS = 30
CAPTURED_PATHS = 50000

# Class to generate trace 
class Trace:
    def __init__(self):
        self.points = []

    def Get(self):
        return self.points
	
    def Create(self):
        randomSpeed = random.randint(MIN_SPEED, MAX_SPEED)
        randomAngle = random.randint(MIN_ANGLE, MAX_ANGLE)

        point = Trace.StartPoint(randomSpeed)
        self.points.append(point)
        while True:
            point = Trace.GetNext(randomSpeed, randomAngle, point)
            if (point == None):
                break
            self.points.append(point)

    # Generate start point of trace
    @staticmethod
    def StartPoint(speed):
        randomX = random.randint(0, FIELD_WIDTH-1)
        randomY = random.randint(0, speed)
        point = [randomX, randomY]
        return point

    # Get next point of trace
    @staticmethod    
    def GetNext(speed, angle, point):
        xDist = int(round(math.sin(math.radians(angle))*speed))
        yDist = int(round(math.cos(math.radians(angle))*speed))
        pointXNext = point[0] + xDist
        pointYNext = point[1] + yDist
        if ((pointXNext > (FIELD_WIDTH-1)) or (pointXNext < 0)):
            return None
        if (pointYNext > (FIELD_HEIGHT-1)):
            return None
        return [pointXNext, pointYNext]


# Draw trace, use index as start point 
def DrawTrace(screen, trace, color, index=0):
    lastPoint = None
    for point in trace.Get()[index:]:
        if (lastPoint!=None):
            pygame.draw.line(screen, color, lastPoint, point, 1) 
        lastPoint = point 


# Find simular traces
def FindTrace(tracesHistory, pointCurrent, index):
    tracesFound = []
    #print(pointCurrent)
    for trace in tracesHistory:
         if (len(trace.Get()) > index):
             if PointInCircle(pointCurrent, SEARCH_RADIUS, trace.Get()[index]):
                 tracesFound.append(trace)
    #print(len(tracesFound), " I ", index)
    return tracesFound

# Determine if point is in a circle
def PointInCircle(pointCircle, radiusCircle, point):
    #print(point, ", ", pointCircle)
    if ( (math.sqrt(abs(point[0]-pointCircle[0])) + math.sqrt(abs(point[1]-pointCircle[1]))) <= math.sqrt(radiusCircle)):
        return True
    return False

# Main
def main():
    pygame.init()

     
    # Set the width and height of the screen [width, height]
    size = (FIELD_WIDTH, FIELD_HEIGHT)
    screen = pygame.display.set_mode(size)
     
    pygame.display.set_caption("Pinball")
     
    # Loop until the user clicks the close button.
    done = False
     
    # Used to manage how fast the screen updates
    clock = pygame.time.Clock()
    random.seed()

    screen.fill(BLACK)

    capturedTraces = []
    for i in range(CAPTURED_PATHS):
        trace = Trace()
        trace.Create()
        capturedTraces.append(trace)

    #for trace in capturedTraces:
    #    DrawTrace(trace, GREEN)

    liveData = Trace()
    liveData.Create()
    DrawTrace(screen, liveData, RED)

    livePoint = None

    # -------- Main Program Loop -----------
    while not done:
        # --- Main event loop
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if (event.key == pygame.K_ESCAPE) or (event.key == pygame.K_q):
                    done = True
                    break # break out of the for loop
            elif event.type == pygame.QUIT:
                done = True
                break # break out of the for loop
        if done:
            break # to break out of the while loop
     
        # --- Game logic should go here
        if (livePoint == None):
            liveSpeed = random.randint(MIN_SPEED, MAX_SPEED)
            liveAngle = random.randint(MIN_ANGLE, MAX_ANGLE)
            livePoint = Trace.StartPoint(liveSpeed)
            liveIndex = 0
            foundTraces = capturedTraces
            color = BLUE
        else:
            livePoint = Trace.GetNext(liveSpeed, liveAngle, livePoint)
            liveIndex=liveIndex+1

        if (livePoint!=None):
            foundTracesLatest = FindTrace(foundTraces, livePoint, liveIndex)
            if (len(foundTracesLatest)==0):
                color=RED
            else:
                foundTraces = foundTracesLatest
     
        # --- Screen-clearing code goes here
     
        # Here, we clear the screen to white. Don't put other drawing commands
        # above this, or they will be erased with this command.
     
        # If you want a background image, replace this clear with blit'ing the
        # background image.
        screen.fill(BLACK)
     
        #circle(Surface, color, pos, radius, width=0)
        for trace in foundTraces:
            DrawTrace(screen, trace, color, liveIndex)

        if (livePoint!=None):
            pygame.draw.circle(screen, WHITE, livePoint, 5) 

        # --- Drawing code should go here
        #pygame.gfxdraw.pixel(screen , randomX, randomY, RED)
        # --- Go ahead and update the screen with what we've drawn.
        pygame.display.flip()
     
        # --- Limit to 30 frames per second
        clock.tick(30)
     
    # Close the window and quit.
    pygame.quit()

if __name__ == "__main__":
    main()