# -*- coding: utf-8 -*-
"""
003_static_blit_pretty.py
static blitting and drawing (pretty version)
url: http://thepythongamebook.com/en:part2:pygame:step003
author: horst.jens@spielend-programmieren.at
licence: gpl, see http://www.gnu.org/licenses/gpl.html

works with pyhton 3.4 and python2.7

Blitting a surface on a static position
Drawing a filled circle into ballsurface.
Blitting this surface once.
introducing pygame draw methods
The ball's rectangular surface is black because the background
color of the ball's surface was never defined nor filled."""

import random
import pygame
import survivalrpgjoystick as game

class Menu(object):
    
    def __init__(self):
        self.items = ["start game", "options", "help", "quit"]
        self.items1= ["sound", "graphics", "load game"]
        
        self.items = self.items
        self.activenr = 0
        
    def getText(self):
        return self.items[self.activenr]
        
    def nextItem(self):
        if self.activenr == len(self.items)-1:
            self.activenr = 0
        else:
            self.activenr += 1
            
            
    def prevItem(self):
        if self.activenr == 0:
            self.activenr = len(self.items)-1
        else:
            self.activenr -=1
    def printItem(self):
        print(self.items[self.activenr])
        return self.activenr
       
class PygView(object):
    
  
    def __init__(self, width=640, height=400, fps=30):
        """Initialize pygame, window, background, font,...
           default arguments 
        """
        pygame.init()
        pygame.display.set_caption("Press ESC to quit")
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((self.width, self.height), pygame.DOUBLEBUF)
        self.background = pygame.Surface(self.screen.get_size()).convert()  
        self.background.fill((255,255,255)) # fill background white
        self.clock = pygame.time.Clock()
        self.fps = fps
        self.playtime = 0.0
        self.font = pygame.font.SysFont('mono', 24, bold=True)
        self.positionmin = 0
        self.positionmax = 20
        self.position = 0
        self.deltapos = 2
        self.getsmaller = False
        self.getbigger = False
        
        self.allgroup = pygame.sprite.Group()
        self.stuffgroup = pygame.sprite.Group()
        Fragment.groups = self.stuffgroup, self.allgroup

    def explode(self, i = 0):
        for x in range(1000):
            Fragment((120,i*30+10))
    def paint(self):
        """painting on the surface"""
       
        for i in m.items:
            if m.items.index(i)==m.activenr:
                self.draw_text(i, 60, m.items.index(i)*30+10, (random.randint(0,255),random.randint(0,255),random.randint(0,255)))
                self.draw_text("->", 20-self.position, m.items.index(i)*30+10,
                              (random.randint(0,255),random.randint(0,255),random.randint(0,255)))
                self.position += self.deltapos
                if self.position > self.positionmax:
                    self.deltapos = -2
                    self.position = self.positionmax
                if self.position < self.positionmin:
                    self.deltapos = 2
                    self.position = self.positionmin
               
            else:
                self.draw_text(i, 120,m.items.index(i)*30+10)
                
    def run(self):
        """The mainloop
        """
        running = True
        while running:
            self.paint()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False 
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    if event.key==pygame.K_DOWN:
                        m.nextItem()
                    if event.key==pygame.K_UP:
                        m.prevItem()
                    if event.key==pygame.K_RETURN:
                            action = m.printItem()
                            print(action)
                            self.explode(m.activenr)
                            if action==0:
                                game.Viewer().run()
                                #self.run()
                            if action==1:
                                print(action)
            milliseconds = self.clock.tick(self.fps)
            seconds = milliseconds / 1000
            self.playtime += seconds
            self.draw_text("FPS: {:6.3}".format(
                           self.clock.get_fps()))
             
            
            self.allgroup.update(seconds)
            self.allgroup.draw(self.screen)
            pygame.display.flip()
            self.screen.blit(self.background, (0, 0))

            
        pygame.quit()


    def draw_text(self, text, x=20, y = 150,color=(255,0,177)):
        """Center text in window
        """
        fw, fh = self.font.size(text)
        surface = self.font.render(text, True, color)
        self.screen.blit(surface, (x,y))

        
class Fragment(pygame.sprite.Sprite):
        """a fragment of an exploding Bird"""
        gravity = True # fragments fall down ?
        def __init__(self, pos):
            #print("fragment")
            pygame.sprite.Sprite.__init__(self, self.groups)
            self.pos = [0.0,0.0]
            self.pos[0] = pos[0]
            self.pos[1] = pos[1]
            self.image = pygame.Surface((10,10))
            self.image.set_colorkey((0,0,0)) # black transparent
            pygame.draw.circle(self.image, (random.randint(20,230),random.randint(20,230),random.randint(20,230)), (5,5),
                                            random.randint(3,10))
            self.a = 255
            self.image = self.image.convert_alpha()
            self.image0 = self.image.convert_alpha()
            self.rect = self.image.get_rect()
            self.rect.center = self.pos #if you forget this line the sprite sit in the topleft corner
            self.lifetime = 5 + random.random()*5 # max 6 seconds
            self.time = 0.0
            self.fragmentmaxspeed = 200  # try out other factors !
            self.dx = random.randint(-self.fragmentmaxspeed,self.fragmentmaxspeed)
            self.dy = random.randint(-self.fragmentmaxspeed,self.fragmentmaxspeed)
            
        def get_alpha_surface( self, surf, alpha=128, red=128, green=128, blue=128, mode=pygame.BLEND_RGBA_MULT):
         
            tmp = pygame.Surface( surf.get_size(), pygame.SRCALPHA, 32)
            tmp.fill( (red,green,blue,alpha) )
            tmp.blit(surf, (0,0), surf.get_rect(), mode)
            return tmp

        def update(self, seconds):
            
            self.time += seconds
            self.a -= 2
            self.a = max(0, self.a)
            self.image = self.get_alpha_surface(self.image0, self.a) 
            
            if self.time > self.lifetime:
                self.kill()
            self.pos[0] += self.dx * seconds
            self.pos[1] += self.dy * seconds
            if Fragment.gravity:
                self.dy += 1 # gravity suck fragments down
            self.rect.centerx = round(self.pos[0],0)
            self.rect.centery = round(self.pos[1],0)
            #pygame.mouse.set_pos(random.randint(0,200),random.randint(0,200))

if __name__ == '__main__':







    
    # call with width of window and fps
    m = Menu()
    p = PygView()
    PygView().run()
