# -*- coding: utf-8 -*-
"""
menu demo and moving surface (non-pygame-Sprite)
on the menu, only screen resolution change, quit and sound toggle
have visible effects
#url: http://thepythongamebook.com/en:part2:pygame:step003
author: horst.jens@spielend-programmieren.at
licence: gpl, see http://www.gnu.org/licenses/gpl.html

works with pyhton3.4 
"""

import pygame 
import random

class MenuDictError(Exception):
    pass

class Menu(object):
    """menu with dict:
       { menu_name : [ list of menu points] }
       Each menu level has an unique name. Top-level menu name must be 
       'root'. Menu name 'back' is not allowed."""
    def __init__(self, items={"root":["play","credits","quit"]}):
        if not "root" in items:
            raise MenuDictError("Menu dict is missing 'root' key")
        if "back" in items:
            raise MenuDictError("Menu dict has the forbidden key 'back'")
        if items == {}:
            raise MenuDictError("Menu dict is empty")
        self.dict = items 
        self.history = []
        self.name = "root"
        self.index = 0
        self.items = self.dict[self.name]
        self.loop = True # if True, it is possible to loop throug items. 
        
    def next_item(self):
        if self.index == len(self.items)-1:
            if self.loop:
                self.index = 0 
        else:
            self.index += 1
        
    def previous_item(self):
        if self.index == 0:
            if self.loop:
                 self.index = len(self.items)-1
        else:
            self.index -= 1
                    
    def action(self):
        """return selected menu item name.or None if another (sub) menu
           is selected."""
        text = self.items[self.index]
        if text != "back" and text not in self.dict:
            return text
        if text == "back":
            self.name = self.history.pop()
        else:
            self.history.append(self.name) # make history
            self.name = text
        self.items = self.dict[self.name]
        if self.name != "root":
            if self.items[-1] != "back":
               self.items.append("back")
        self.index = 0
        return None

class PygView(object):

    def __init__(self, width=640, height=400, fps=30):
        
        pygame.init()
        pygame.display.set_caption("Press ESC to quit. PgUP/PgDOWN "
                                   "to change speed of blue ball")
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((self.width, 
                                        self.height), pygame.DOUBLEBUF)
        self.background = pygame.Surface(
                                      self.screen.get_size()).convert()  
        self.background.fill((255,255,255)) # fill background white
        self.clock = pygame.time.Clock()
        self.fps = fps
        self.playtime = 0.0
        self.sprites=[]         # a simple sprite container
        self.paint_background() # this is called once
        self.create_sprites()
           # 
        self.allgroup = pygame.sprite.Group()   
        self.stuffgroup = pygame.sprite.Group()
        self.textgroup = pygame.sprite.Group()
        Fragment.groups = self.stuffgroup, self.allgroup
        Text.groups = self.textgroup, self.allgroup
    
    
           
    def explode(self, i = 0):
        for x in range(100):
            Fragment((120,i*30+10))
            print("Ich bin ein Fragment und der Silas nerft mich.")
            
    def randomcolor(self):
        """returns random color tuple"""
        return (random.randint(0,255), random.randint(0,255), 
                random.randint(0,255))
                
    def draw_text(self, text, x=50, y=150, centered=False, 
                 color=(0,0,0), fontsize=24):
        """blit text on apygame surface. X,Y is topleft or center pos"""
        self.font = pygame.font.SysFont('mono', fontsize, bold=True)
        fw, fh = self.font.size(text) # calculate size of rect
        surface = self.font.render(text, True, color)
        if centered:
            self.screen.blit(surface, (x - fw/2,y-fh/2))
        else:
            self.screen.blit(surface, (x,y)) # x,y is topleft corner

    def create_sprites(self): #   area    x   y    color    dx    dy 
        area1 = self.screen.get_rect()
        area2 = pygame.Rect(self.width/2,0,self.width/2,self.height)
        self.sprites.append(Ball(area1, 50,250, (0,0,255), 50, -8))
        self.sprites.append(Ball(area2, 100,100, (255,0,0),-50, 40))

    def paint_background(self):
        """painting on the surface"""
        y = self.height - 100
        #------- try out some pygame draw functions --------
        # pygame.draw.rect(Surface, color, Rect, width=0): return Rect
        # rect: (topleftX, topleftY, width, height)
        pygame.draw.rect(self.background, (0,255,0), (50,y,100,25)) 
        # pygame.draw.circle(Surface, color, pos, radius, width=0)
        pygame.draw.circle(self.background, (0,200,0), (200,y), 35)
        # pygame.draw.polygon(Surface, color, pointlist, width=0)
        pygame.draw.polygon(self.background, (0,180,0), ((250,y),
                            (300,y-50),(350,y+20)))
        # pygame.draw.arc(Surface, color, Rect, start_angle, stop_angle)
        pygame.draw.arc(self.background, (0,150,0),(400,y-20,150,100),
                                          0, 3.14) # radiant, not  grad
    
    def menu_blit(self, menu, x=50, top=50, h=25):
        """paint menu items of actual menu on the screen"""
        for i in menu.items:
            y = top+menu.items.index(i)*h # h=height of text
            if menu.items.index(i) == menu.index: # active item?
                self.draw_text("-->", x-50,y, color=self.randomcolor() )
                self.draw_text(i,x,y, color=self.randomcolor())
            else:
                self.draw_text(i, x, y) # paint text in black 
    
    def run(self):
        running = True
        while running: 
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False 
                elif event.type == pygame.KEYDOWN:
                    # key pressed (once) and released
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    if event.key == pygame.K_DOWN:
                        m.next_item()
                    if event.key == pygame.K_UP:
                        m.previous_item()
                    if event.key == pygame.K_RETURN:
                        actionstring = m.action()
                        if actionstring != None: # action handler
                            print(actionstring + " is selected")
                            if actionstring == "turn sound off":
                                m.dict["options"][2] = "turn sound on"
                                Text("Sound turned ON", 100,100)
                            elif actionstring == "turn sound on":
                                m.dict["options"][2] = "turn sound off"
                                Text("Sound turned OFF", 100,100)
                            elif actionstring == "quit":
                                running = False
                            elif m.name == "graphic":
                                x,y = actionstring.split("x")
                                x = int(x)
                                y = int(y)
                                self.__init__(x,y) # restart pygame
                                self.explode(3)
            
            # keys pressed (and not released)
            pressedkeys = pygame.key.get_pressed()
            if pressedkeys[pygame.K_PAGEUP]:
                self.sprites[0].dx *= 1.1
                self.sprites[0].dy *= 1.1
            if pressedkeys[pygame.K_PAGEDOWN]:
                self.sprites[0].dx *= 0.9
                self.sprites[0].dy *= 0.9 
            seconds = self.clock.tick(self.fps) / 1000.0 # milliseconds
            self.playtime += seconds
            self.screen.blit(self.background, (0, 0)) # clean all
            
            #update sprites (overwriting background)
            for sprite in self.sprites:
                sprite.update(seconds)
                sprite.blit(self.screen)
                
           # 
            self.allgroup.update(seconds)
            self.allgroup.draw(self.screen)
            #pygame.display.flip()
            #self.screen.blit(self.background, (0, 0))
            
            # update screen text (overwriting sprites)
            text = "fps: {:6.3} seconds since start: {:6.3}".format(
                self.clock.get_fps(),self.playtime)
            self.draw_text(text, self.width/2, self.height-30, True) 
            text ="speed of blue ball (dx/dy): {:6.3}/{:6.3}".format(
                self.sprites[0].dx, self.sprites[0].dy)
            self.draw_text(text, self.width/2, self.height-10, True)
            # paint menu (overwriting everything else)
            self.menu_blit(m)
            
            pygame.display.flip() 
        pygame.quit()

class Ball(object):
    """this is not a native pygame Sprite. It's a pygame surface"""
    def __init__(self, area, x=100, y=240, color=(0,0,255), dx=0,
        dy=0, radius = 10):
        """create a (black) surface and paint a blue ball on it"""
        self.radius = radius
        self.color = color
        self.area = area   # where the ball is allowed to move
        self.x = float(x)
        self.y = float(y)
        self.dx = float(dx)         # x movement in pixel per seconds
        self.dy = float(dy)         # y movement in pixel per seconds
        # create a rectangular surface for the ball 100 x 100
        self.surface = pygame.Surface((2*self.radius,2*self.radius))  
        self.rect = self.surface.get_rect()  
        # pygame.draw.circle(Surface, color, pos, radius, width=0)
        pygame.draw.circle(self.surface, color, (radius, radius),radius)
        self.surface = self.surface.convert() # for faster blitting. 
        self.surface.set_colorkey((0,0,0)) # make black transparent color
        self.surface = self.surface.convert_alpha() # faster blitting 
        
    def update(self, seconds):
        self.x += self.dx * seconds
        self.y += self.dy * seconds
        self.areacheck()
        
    def areacheck(self):
        if self.x < self.area.left:
            self.x = self.area.left
            self.dx *= -1 # bounce
        if self.x + self.rect.width > self.area.right:
            self.x = self.area.right - self.rect.width
            self.dx *= -1
        if self.y < self.area.top:
            self.y = self.area.top
            self.dy *= -1
        if self.y + self.rect.height > self.area.bottom:
            self.y = self.area.height - self.rect.bottom
            self.dy *= -1
        
    def blit(self, screen):
        """blit a pygame surface on another pygame surface"""
        screen.blit(self.surface,(round(self.x,0),round(self.y,0)))
        
class Text(pygame.sprite.Sprite):
    """Credits text"""
    def __init__(self, text, x, y, fontsize=20, color=(random.randint(0,255),random.randint(0,255),random.randint(0,255)), centered=True):
            #print("fragment")
            pygame.sprite.Sprite.__init__(self, self.groups)
            self.pos = [x,y]
            self.x = x
            self.y = y
            #self.image = pygame.Surface((10,10))
            #color=(0,0,0), (fontsize=24):
            """blit text on apygame surface. X,Y is topleft or center pos"""
            self.font = pygame.font.SysFont('mono', fontsize, bold=True)
            self.fw, self.fh = self.font.size(text) # calculate size of rect
            self.image= self.font.render(text, True, color)
            #if centered:
            #    self.screen.blit(surface, (x - fw/2,y-fh/2))
            #else:
            #    self.screen.blit(surface, (x,y)) # x,y is topleft corner


            self.image.set_colorkey((0,0,0)) # black transparent
            #pygame.draw.circle(self.image, (random.randint(20,230),random.randint(20,230),random.randint(20,230)), (5,5),
                                            #random.randint(3,10))
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
            #self.a -= 2
            #self.a = max(0, self.a)
            #self.image = self.get_alpha_surface(self.image0, self.a) 
            
            if self.time > self.lifetime:
                self.kill()
            self.x += self.dx * seconds
            self.y += self.dy * seconds
            #if Fragment.gravity:
            #    self.dy += 1 # gravity suck fragments down
            self.rect.centerx = round(self.x,0)
            self.rect.centery = round(self.y,0)
            #pygame.mouse.set_pos(random.randint(0,200),random.randint(0,200))


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
    m = Menu({"root":["play","options","credits","quit"],
              "options":["difficulty", "graphic", "turn sound off"],
              "graphic":["320x200","640x400","800x600","1024x768",
                         "1280x800","1280x1024","1366x768","1920x1080"],
              "difficulty":["beginner","normal","veteran","elite"]})
    PygView(800,600).run()
