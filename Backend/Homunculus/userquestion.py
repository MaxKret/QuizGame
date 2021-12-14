import pygame as pg
import os.path

def user_check() -> str:
    userfilepath = os.path.join(os.path.abspath(os.path.dirname(__file__)), "user.txt")
    if(os.path.exists(userfilepath)):
        with open("user.txt", "r") as openfile:
            firstline = openfile.readline()
            return firstline
    else:
        useremail = ask()
        with open("user.txt", "w+") as openfile:
            openfile.write(useremail)
        return useremail


def ask() -> str:
    pg.init()
    screen = pg.display.set_mode((640, 480))
    font = pg.font.Font(None, 32)
    clock = pg.time.Clock()
    input_box = pg.Rect(100, 100, 140, 32)
    color_inactive = pg.Color('lightskyblue3')
    color_active = pg.Color('dodgerblue2')
    color = color_inactive
    active = False
    text = ''
    done = False

    useremail = ""

    while not done:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                done = True
            if event.type == pg.MOUSEBUTTONDOWN:
                # If the user clicked on the input_box rect.
                if input_box.collidepoint(event.pos):
                    # Toggle the active variable.
                    active = not active
                else:
                    active = False
                # Change the current color of the input box.
                color = color_active if active else color_inactive
            if event.type == pg.KEYDOWN:
                if active:
                    # return
                    if event.key == pg.K_RETURN:
                        useremail = text
                    #remove a char
                    elif event.key == pg.K_BACKSPACE:
                        text = text[:-1]
                    
                    else:
                        text += event.unicode

        screen.fill((30, 30, 30))
        # Render the current text.
        txt_surface = font.render(text, True, color)
        # Resize the box if the text is too long.
        width = max(200, txt_surface.get_width()+10)
        input_box.w = width
        # Blit the text.
        screen.blit(txt_surface, (input_box.x+5, input_box.y+5))
        # Blit the input_box rect.
        pg.draw.rect(screen, color, input_box, 2)

        # Render the current text.
        txt_surface = font.render(useremail, True, pg.Color(255,255,255))
        # Resize the box if the text is too long.
        width = max(200, txt_surface.get_width()+10)
        input_box.w = width
        # Blit the text.
        screen.blit(txt_surface, (input_box.x+5, input_box.y+35))
        # Blit the input_box rect.
        pg.draw.rect(screen, color, input_box, 2)

        

        pg.display.flip()
        clock.tick(30)
    pg.quit()
    return useremail

# if __name__ == '__main__':
#     ask()