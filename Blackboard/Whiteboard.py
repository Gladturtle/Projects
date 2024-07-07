import pygame
red_button = pygame.Rect(10,10,20,20)
blue_button = pygame.Rect(40,10,20,20)
green_button = pygame.Rect(70,10,20,20)
yellow_button = pygame.Rect(100,10,20,20)
eraser = pygame.Rect(130,10,30,30)
screen = pygame.display.set_mode((1280, 770))
colour_menu = pygame.Rect(0,0,1280,50)
run = True
x = 0
y = 0
cursor_colour = (255,255,255)
while run:
    colour_select = pygame.draw.rect(screen,(255,255,255),colour_menu)
    x = pygame.mouse.get_pos()[0]
    y = pygame.mouse.get_pos()[1]
    if 10<x<30 and 10<y<30 and events.type == pygame.MOUSEBUTTONDOWN :
         cursor_colour = (255,0,0)
    else:
         red_outline = pygame.draw.rect(screen,(0,0,0),(8,8,24,24),0)
    red = pygame.draw.rect(screen,(255,0,0),red_button)
    if 40<x<60 and 10<y<30 and events.type == pygame.MOUSEBUTTONDOWN :
         cursor_colour = (0,0,255)
    else:
         blue_outline = pygame.draw.rect(screen,(0,0,0),(38,8,24,24),0)
    blue = pygame.draw.rect(screen,(0,0,255),blue_button)
    if 70<x<90 and 10<y<30 and events.type == pygame.MOUSEBUTTONDOWN :
         cursor_colour = (0,255,0)
    else:
         green_outline = pygame.draw.rect(screen,(0,0,0),(68,8,24,24),0)
    green = pygame.draw.rect(screen,(0,255,0),green_button)
    if 100<x<120 and 10<y<30 and events.type == pygame.MOUSEBUTTONDOWN :
         cursor_colour = (255,255,0)
    else:
         yellow_outline = pygame.draw.rect(screen,(0,0,0),(98,8,24,24),0)
    yellow = pygame.draw.rect(screen,(255,255,0),yellow_button) 
    if pygame.mouse.get_pressed()[0]:
            if events.type == pygame.MOUSEMOTION :
                (x,y) = pygame.mouse.get_pos()
                if (abs(past_x-x)>10 or abs(past_y-y)>10 ):
                    fill_sq = int(abs(past_x-x)+abs(past_y-y))
                    indent_x =  0.5*(x-past_x)/(fill_sq+1)
                    indent_y = 0.5*(y-past_y)/(fill_sq+1)
                    print(indent_y,y,past_y,fill_sq)
                    for num in range(1,2*fill_sq):
                        
                        player = pygame.Rect(past_x+indent_x,past_y+indent_y,20,20)
                        past_x = past_x+indent_x
                        past_y = past_y +indent_y
                        pygame.draw.rect(screen,cursor_colour,player)
                player = pygame.Rect(x,y,20,20)
                pygame.draw.rect(screen,cursor_colour,player)
    past_x = x
    past_y = y
    
    for events in pygame.event.get():
        if events.type == pygame.QUIT:
            run = False
    screen.blit(screen,(0,0))   
    pygame.display.flip()