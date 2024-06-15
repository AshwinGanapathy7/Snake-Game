import pygame
from pygame.math import Vector2
import random
import sys

class SNAKE:
	def __init__(self):
		self.body = [Vector2(5, 10), Vector2(4,10), Vector2(3,10)]
		self.dir = Vector2(1, 0)
		self.color = (0, 255, 0)
		self.face_color = (0, 180, 0)
		self.add_block = False

	def draw_snake(self):
		for i, block in enumerate(self.body):

			body_rect = pygame.Rect(int(block.x * CELL_SIZE), int(block.y * CELL_SIZE), CELL_SIZE, CELL_SIZE)
			if(i != 0):
				pygame.draw.rect(screen, self.color, body_rect)
			elif(i == 0):
				pygame.draw.rect(screen, self.face_color, body_rect)
	def move_snake(self):
		if(self.add_block):
			body_copy = self.body[:]
			body_copy.insert(0, self.body[0] + self.dir)
			self.body = body_copy
			self.add_block = False
		else:
			body_copy = self.body[:-1]
			body_copy.insert(0, self.body[0] + self.dir)
			self.body = body_copy

	def show_score(self):
		self.score = str(len(self.body) - 3)
		self.score_text = font.render(self.score, True, (255, 255, 255))
		score_x = int(CELL_SIZE * NUMBER_OF_CELLS - 10)
		score_y = int(CELL_SIZE * NUMBER_OF_CELLS - 10)
		score_rect = self.score_text.get_rect(center = (score_x - 30, score_y - 30))
		screen.blit(self.score_text, score_rect)



class FRUIT:
	def __init__(self):
		self.x = random.randint(0, NUMBER_OF_CELLS - 1)
		self.y = random.randint(0, NUMBER_OF_CELLS - 1)
		self.color = (255, 0, 0)
		self.pos = Vector2(self.x, self.y)

	def draw_fruit(self):		
		fruit_rect = pygame.Rect(int(self.pos.x * CELL_SIZE), int(self.pos.y * CELL_SIZE), CELL_SIZE, CELL_SIZE)
		pygame.draw.rect(screen, self.color, fruit_rect)

	def randomize(self):
		self.x = random.randint(0, NUMBER_OF_CELLS - 1)
		self.y = random.randint(0, NUMBER_OF_CELLS - 1)
		self.pos = Vector2(self.x, self.y)

class MAIN:
	def __init__(self):
		self.fruit = FRUIT()
		self.snake = SNAKE()

	def draw(self):
		self.fruit.draw_fruit()
		self.snake.draw_snake()

	def grow(self):
		if(self.snake.body[0] == self.fruit.pos):
			self.snake.add_block = True
			self.fruit.randomize()

CELL_SIZE = 25
NUMBER_OF_CELLS = 25



def setup():
	global font, game_over_font, screen, clock, running, main
	pygame.init()

	font = pygame.font.Font('/System/Library/Fonts/Supplemental/Verdana Bold.ttf', 20)
	game_over_font = pygame.font.Font('/System/Library/Fonts/Supplemental/Verdana Bold.ttf', 40)
	screen = pygame.display.set_mode((CELL_SIZE * NUMBER_OF_CELLS, CELL_SIZE * NUMBER_OF_CELLS))
	pygame.display.set_caption("Snake Game")
	clock = pygame.time.Clock()

	running = True
	main = MAIN()

	SCREEN_UPDATE = pygame.USEREVENT
	pygame.time.set_timer(SCREEN_UPDATE, 100)

def game():


	pygame.init()

	font = pygame.font.Font('/System/Library/Fonts/Supplemental/Verdana Bold.ttf', 20)
	game_over_font = pygame.font.Font('/System/Library/Fonts/Supplemental/Verdana Bold.ttf', 40)
	screen = pygame.display.set_mode((CELL_SIZE * NUMBER_OF_CELLS, CELL_SIZE * NUMBER_OF_CELLS))
	pygame.display.set_caption("Snake Game")
	clock = pygame.time.Clock()

	running = True
	main = MAIN()

	SCREEN_UPDATE = pygame.USEREVENT
	pygame.time.set_timer(SCREEN_UPDATE, 100)

	#game loop
	while running:
		screen.fill((0,0,0))
		for event in pygame.event.get():
			if(event.type == pygame.QUIT):
				running = False
				pygame.quit()
				sys.exit()
			if(event.type == SCREEN_UPDATE):
				main.snake.move_snake()
			if(event.type == pygame.KEYDOWN):
				if(event.key == pygame.K_UP and main.snake.dir != Vector2(0, 1)):
					main.snake.dir = Vector2(0, -1)
				if(event.key == pygame.K_DOWN and main.snake.dir != Vector2(0, -1)):
					main.snake.dir = Vector2(0, 1)
				if(event.key == pygame.K_LEFT and main.snake.dir != Vector2(1, 0)):
					main.snake.dir = Vector2(-1, 0)
				if(event.key == pygame.K_RIGHT and main.snake.dir != Vector2(-1, 0)):
					main.snake.dir = Vector2(1, 0)
		main.draw()
		main.grow()
		main.snake.show_score()
		if(main.snake.body[0].x < 0 or main.snake.body[0].x > NUMBER_OF_CELLS - 1 or main.snake.body[0].y < 0 or main.snake.body[0].y > NUMBER_OF_CELLS - 1):
			running = False
		for block in main.snake.body[1:]:
			if(main.snake.body[0] == block):
				running = False
		clock.tick(120)
		pygame.display.update()


	#high score and current score calculating logic
	score = main.snake.score
	with open('high_score.txt', 'r') as f:
		high_score = f.read()
	if(score > high_score):
		with open('high_score.txt', 'w') as f:
			f.write(score)
			high_score = score

	#button colors for end screen
	restart_btn_color = (0, 150, 50)
	exit_btn_color = (0, 100, 100)
    
	#variable used for button press on end screen
	clicked = False
	#whole loop for end screen
	end_run = True
	while end_run:
		#length and width for both buttons
		length = 120
		width = 40
		
		#restart button information
		restart_rect_x = (NUMBER_OF_CELLS*CELL_SIZE) / 2
		restart_rect_y = 300
		x_min_restart = restart_rect_x - length / 2
		x_max_restart = restart_rect_x + length / 2
		y_min_restart = restart_rect_y - width / 2
		y_max_restart = restart_rect_y + width / 2
		

		#exit button information
		exit_rect_x = (NUMBER_OF_CELLS*CELL_SIZE) / 2
		exit_rect_y = 350
		x_min_exit = exit_rect_x - length / 2
		x_max_exit = exit_rect_x + length / 2
		y_min_exit = exit_rect_y - width / 2
		y_max_exit = exit_rect_y + width / 2

		mouse = pygame.mouse.get_pos() 
		for event in pygame.event.get():
			if(event.type == pygame.QUIT):
				end_run = False
				pygame.quit()
				sys.exit()
			if(event.type == pygame.MOUSEBUTTONDOWN):
				clicked = True
				if(x_min_restart <= mouse[0] <=  x_max_restart and y_min_restart <= mouse[1] <= y_max_restart):
					restart_btn_color = (0, 120, 20)
				if(x_min_exit <= mouse[0] <=  x_max_exit and y_min_exit <= mouse[1] <= y_max_exit):
					exit_btn_color = (0, 70, 70)
			if(event.type == pygame.MOUSEBUTTONUP and clicked == True):
				clicked = False
				if(x_min_restart <= mouse[0] <=  x_max_restart and y_min_restart <= mouse[1] <= y_max_restart):
					restart_btn_color = (0, 150, 50)
					setup()
					game()
				if(x_min_exit <= mouse[0] <=  x_max_exit and y_min_exit <= mouse[1] <= y_max_exit):
					exit_btn_color = (0, 100, 100)
					pygame.quit()
					sys.exit()


		if(x_min_restart <= mouse[0] <=  x_max_restart and y_min_restart <= mouse[1] <= y_max_restart):
			restart_btn_color = (0, 135, 35)
		elif(x_min_exit <= mouse[0] <=  x_max_exit and y_min_exit <= mouse[1] <= y_max_exit):
			exit_btn_color = (0, 85, 85)
		else:
			restart_btn_color = (0, 150, 50)
			exit_btn_color = (0, 70, 70)
			
		screen.fill((0,0,0))
		#Show Game Over Text
		game_over_text = game_over_font.render("Game Over", True, (255, 255, 255))
		game_over_rect = game_over_text.get_rect(center = ((NUMBER_OF_CELLS * CELL_SIZE) / 2, 20))
		screen.blit(game_over_text, game_over_rect)

		#Show the high score
		high_score_text = "High Score: " + high_score
		game_over_high_score_text = font.render(high_score_text, True, (255, 255, 255))
		game_over_high_score_rect = game_over_high_score_text.get_rect(center = ((NUMBER_OF_CELLS * CELL_SIZE) / 2 , 100))
		screen.blit(game_over_high_score_text, game_over_high_score_rect)

		#Show the user's score
		score_text = "Your score: " + score
		game_over_score_text = font.render(score_text, True, (255,255,255))
		game_over_score_rect = game_over_score_text.get_rect(center = ((NUMBER_OF_CELLS * CELL_SIZE) / 2, 150))
		screen.blit(game_over_score_text ,game_over_score_rect)

		#Restart button
		restart = "RESTART"
		restart_text = font.render(restart, True, (255, 255, 255))
		
		restart_rect = restart_text.get_rect(center = (restart_rect_x, restart_rect_y))
		
		restart_rect_rectangle = pygame.Rect(restart_rect_x - length / 2, restart_rect_y - width / 2, length, width)
		pygame.draw.rect(screen, restart_btn_color, restart_rect_rectangle)
		screen.blit(restart_text, restart_rect)

		#Exit button
		exit = "EXIT"
		exit_text = font.render(exit, True, (255, 255, 255))
		
		exit_rect = exit_text.get_rect(center = (exit_rect_x, exit_rect_y))
		exit_rect_rectangle = pygame.Rect(exit_rect_x - length / 2, exit_rect_y - width / 2, length, width)
		pygame.draw.rect(screen, exit_btn_color, exit_rect_rectangle)
		screen.blit(exit_text, exit_rect)
		


		pygame.display.update()

	pygame.quit()

setup()
game()