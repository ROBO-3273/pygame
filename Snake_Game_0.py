import sys, time, random
import pygame as pg

pg.init()
#git hub
matrix = []
matrix_rows = 18
matrix_cols = 32

cell_size = 30
cell_margin = 1

snake_coor = [(2, 4), (2, 3), (2, 2)] #start point
snake_dir = 'right'

apple_point = None

color_bg = (50, 50, 50)
color_text = (255, 255, 0)
color_cell_empty = (50, 50, 255)
color_cell_snakeHead = (255, 0, 0)
color_cell_snakeBody = (0, 255, 0)
color_cell_apple = (255, 255, 255)
color_cell_edge = (0, 0, 0)

colors_cell = [color_cell_empty, color_cell_snakeHead, color_cell_snakeBody, color_cell_apple, color_cell_edge]

pg.display.set_caption('Snake Game')
fps = 60.0
gameSpeed = fps * 0.25
clock = pg.time.Clock()
screen_size = ((cell_size + cell_margin) * matrix_cols, (cell_size + cell_margin) * matrix_rows)
screen = pg.display.set_mode(screen_size)

MyDir = 'C:/ROBO/pygame/snake_game/' #set your directory

font_small = pg.font.Font(MyDir +  'consola.ttf', int(cell_size * 0.75)) 
font_big = pg.font.Font(MyDir + 'consolab.ttf', int(screen_size[0] / 8))


def create_matrix():
    global matrix
    matrix = []
    onerow = []
    for row in range(matrix_rows):
        for col in range(matrix_cols):
            if row == 0 or row == matrix_rows - 1 or col == 0 or col == matrix_cols - 1:
                onerow.append(4)
            else:
                onerow.append(0)

        matrix.append(onerow)
        onerow = []

def set_obj():
    global matrix
    #set snake
    row = 0
    col = 0
    for coor in snake_coor:
        if row == 0 and col == 0:
            row, col = coor
            matrix[row][col] = 1
        else:
            row, col = coor
            matrix[row][col] = 2
    #set apple
    row, col = apple_point
    matrix[row][col] = 3

def create_apple():
    global apple_point
    row = 0
    col = 0

    while True:
        row = random.randint(0, matrix_rows - 1)
        col = random.randint(0, matrix_cols - 1)
        if matrix[row][col] == 0:
            apple_point = (row, col)
            return


def draw_matrix():
    for row in range(matrix_rows):
        for col in range(matrix_cols):
            color = colors_cell[matrix[row][col]]
            pg.draw.rect(screen, color, ((cell_size + cell_margin) * col, (cell_size + cell_margin) * row, cell_size, cell_size))

def game_set():
    create_matrix()
    create_apple()
    set_obj()
    pressed = False
    textA, textA_rect = render_text('SNAKE GAME', font_big, color_text)
    textB, textB_rect = render_text('Press Any Key To Start', font_small, color_text)
    textA_rect.center = (screen_size[0] / 2, screen_size[1] / 2)
    textB_rect.center = (screen_size[0] / 2, screen_size[1] / 2 + textA_rect.height + textB_rect. height / 2 + 30)
    while not pressed:
        for event in pg.event.get():
            screen.blit(textA, textA_rect)
            screen.blit(textB, textB_rect)
            if event.type == pg.KEYDOWN:
                pressed = True
            pg.display.update()

        

def game_run():
    global snake_dir
    frame = 1
    score = 0
    life = 3

    while True:
        key = 0

        if not life:
            time.sleep(1)
            screen.fill([0, 0, 0])
            textA, textA_rect = render_text('GAME OVER', font_big, color_text)
            textB, textB_rect = render_text('Score: %s'% score, font_small, color_text)
            textA_rect.center = (screen_size[0] / 2, screen_size[1] / 2)
            textB_rect.center = (screen_size[0] / 2, screen_size[1] / 2 + textA_rect.height + textB_rect.height / 2 + 30)                
            screen.blit(textA, textA_rect)
            screen.blit(textB, textB_rect)
            pg.display.update()
            time.sleep(3)
            return
        
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return
            if event.type == pg.KEYDOWN:
                key = event.key
        
        if key == pg.K_ESCAPE:
            return
        elif key == pg.K_UP and snake_dir != 'down':
            snake_dir = 'up'
        elif key == pg.K_LEFT and snake_dir != 'right':
            snake_dir = 'left'
        elif key == pg.K_RIGHT and snake_dir != 'left':
            snake_dir = 'right'
        elif key == pg.K_DOWN and snake_dir != 'up':
            snake_dir = 'down'
        else:
            pass

        if frame % gameSpeed == 0:
   
            F_row = 0
            F_col = 0
            row, col = snake_coor[0]

            if snake_dir == 'up':
                F_row = -1
            elif snake_dir == 'down':
                F_row = 1
            elif snake_dir == 'left':
                F_col = -1
            elif snake_dir == 'right':
                F_col = 1

            forwardCell = checkForwardCell(row, col)

            if forwardCell == 0:
                snake_coor.insert(0, (row + F_row, col + F_col))
                snake_coor.pop()
            elif forwardCell == 3:
                snake_coor.insert(0, (row + F_row, col + F_col))
                create_apple()
            elif life:
                life -= 1
                score -= len(snake_coor) * 20
                snake_coor.pop()

            score += 4 + 2 * len(snake_coor)
            create_matrix()
            set_obj()

        title, title_rect = render_text('Snake Game', font_small, color_text)
        grade, grade_rect = render_text('Score: %s'% score, font_small, color_text)
        Life, Life_rect = render_text('Life: %s'% life, font_small, color_text)
        title_rect.center = (screen_size[0] / 2, cell_size / 1.5)
        grade_rect.center = ((cell_size + cell_margin) * 4, cell_size / 1.5)
        Life_rect.center = (screen_size[0] - (cell_size + cell_margin) * 4, cell_size / 1.5)

        screen.fill(color_bg)
        draw_matrix()
        screen.blit(grade, grade_rect)
        screen.blit(title, title_rect)
        screen.blit(Life, Life_rect)
        pg.display.update()
        frame += 1
        clock.tick(fps)

def render_text(text, font, color):
    Text = font.render(text, True, color)
    Text_rect = Text.get_rect()
    return Text, Text_rect
        
def checkForwardCell(row, col):
    if snake_dir == 'up':
        return matrix[row - 1][col]
    elif snake_dir == 'down':
        return matrix[row + 1][col]
    elif snake_dir == 'left':
        return matrix[row][col - 1]
    elif snake_dir == 'right':
        return matrix[row][col + 1]
    else:
        return None
    
    
        


def main():
    game_set()
    game_run()
    pg.quit()

if __name__ == "__main__":
    main()

