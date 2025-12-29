import pygame
import random
import json
import os
import platform

pygame.init()

GRID_WIDTH = 10
GRID_HEIGHT = 20
CELL_SIZE = 30
SCREEN_WIDTH = GRID_WIDTH * CELL_SIZE + 200
SCREEN_HEIGHT = GRID_HEIGHT * CELL_SIZE

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
ORANGE = (255, 165, 0)
GRAY = (128, 128, 128)
DARK_GRAY = (64, 64, 64)
LIGHT_GRAY = (192, 192, 192)

COLORS = [BLACK, RED, GREEN, BLUE, YELLOW, CYAN, MAGENTA, ORANGE]

SHAPES = [
    [[1, 1, 1, 1]],
    [[1, 1], [1, 1]],
    [[1, 1, 1], [0, 1, 0]],
    [[1, 1, 1], [1, 0, 0]],
    [[1, 1, 1], [0, 0, 1]],
    [[1, 1, 0], [0, 1, 1]],
    [[0, 1, 1], [1, 1, 0]]
]

DIFFICULTIES = {
    'easy': {'speed': 800, 'name': '简单'},
    'medium': {'speed': 500, 'name': '中等'},
    'hard': {'speed': 300, 'name': '困难'}
}

HIGH_SCORE_FILE = 'high_scores.json'

def get_chinese_font(size):
    system = platform.system()
    if system == 'Windows':
        font_names = ['microsoftyahei', 'simhei', 'simsun', 'msyh']
        for font_name in font_names:
            try:
                return pygame.font.SysFont(font_name, size)
            except:
                continue
    return pygame.font.Font(None, size)

class HighScoreManager:
    def __init__(self):
        self.scores = self.load_scores()
    
    def load_scores(self):
        if os.path.exists(HIGH_SCORE_FILE):
            try:
                with open(HIGH_SCORE_FILE, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return {'easy': 0, 'medium': 0, 'hard': 0}
        return {'easy': 0, 'medium': 0, 'hard': 0}
    
    def save_scores(self):
        with open(HIGH_SCORE_FILE, 'w', encoding='utf-8') as f:
            json.dump(self.scores, f, ensure_ascii=False, indent=2)
    
    def update_score(self, difficulty, score):
        if score > self.scores[difficulty]:
            self.scores[difficulty] = score
            self.save_scores()
            return True
        return False
    
    def get_high_score(self, difficulty):
        return self.scores[difficulty]

class Button:
    def __init__(self, x, y, width, height, text, color, hover_color, action):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.action = action
        self.hovered = False
    
    def draw(self, screen, font):
        color = self.hover_color if self.hovered else self.color
        pygame.draw.rect(screen, color, self.rect, border_radius=10)
        pygame.draw.rect(screen, WHITE, self.rect, 2, border_radius=10)
        
        text_surface = font.render(self.text, True, WHITE)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)
    
    def check_hover(self, mouse_pos):
        self.hovered = self.rect.collidepoint(mouse_pos)
    
    def check_click(self, mouse_pos):
        if self.rect.collidepoint(mouse_pos) and self.action:
            return self.action()
        return None

class Menu:
    def __init__(self, screen, high_score_manager):
        self.screen = screen
        self.high_score_manager = high_score_manager
        self.font = get_chinese_font(48)
        self.small_font = get_chinese_font(32)
        
        button_width = 200
        button_height = 50
        button_x = SCREEN_WIDTH // 2 - button_width // 2
        start_y = 200
        gap = 70
        
        self.buttons = [
            Button(button_x, start_y, button_width, button_height, '简单', GREEN, (0, 200, 0), lambda: 'easy'),
            Button(button_x, start_y + gap, button_width, button_height, '中等', YELLOW, (200, 200, 0), lambda: 'medium'),
            Button(button_x, start_y + gap * 2, button_width, button_height, '困难', RED, (200, 0, 0), lambda: 'hard'),
            Button(button_x, start_y + gap * 3, button_width, button_height, '退出', GRAY, LIGHT_GRAY, lambda: 'quit')
        ]
    
    def draw(self):
        self.screen.fill(BLACK)
        
        title = self.font.render('俄罗斯方块', True, CYAN)
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 100))
        self.screen.blit(title, title_rect)
        
        subtitle = self.small_font.render('选择难度', True, WHITE)
        subtitle_rect = subtitle.get_rect(center=(SCREEN_WIDTH // 2, 150))
        self.screen.blit(subtitle, subtitle_rect)
        
        for i, (diff, data) in enumerate(DIFFICULTIES.items()):
            high_score = self.high_score_manager.get_high_score(diff)
            score_text = self.small_font.render(f'{data["name"]}: {high_score}', True, WHITE)
            self.screen.blit(score_text, (20, 20 + i * 30))
        
        for button in self.buttons:
            button.draw(self.screen, self.small_font)
        
        pygame.display.flip()
    
    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return None
                
                if event.type == pygame.MOUSEMOTION:
                    for button in self.buttons:
                        button.check_hover(event.pos)
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        for button in self.buttons:
                            result = button.check_click(event.pos)
                            if result:
                                return result
            
            self.draw()
            self.clock = pygame.time.Clock()
            self.clock.tick(60)

class Tetris:
    def __init__(self, difficulty='medium', high_score_manager=None):
        self.difficulty = difficulty
        self.high_score_manager = high_score_manager
        self.grid = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
        self.current_piece = self.new_piece()
        self.next_piece = self.new_piece()
        self.score = 0
        self.game_over = False
        self.clock = pygame.time.Clock()
        self.fall_time = 0
        self.fall_speed = DIFFICULTIES[difficulty]['speed']
        self.new_high_score = False

    def new_piece(self):
        shape = random.choice(SHAPES)
        color = random.randint(1, 7)
        return {
            'shape': shape,
            'color': color,
            'x': GRID_WIDTH // 2 - len(shape[0]) // 2,
            'y': 0
        }

    def valid_move(self, piece, dx, dy, new_shape=None):
        if new_shape is None:
            new_shape = piece['shape']
        
        for y, row in enumerate(new_shape):
            for x, cell in enumerate(row):
                if cell:
                    new_x = piece['x'] + x + dx
                    new_y = piece['y'] + y + dy
                    
                    if new_x < 0 or new_x >= GRID_WIDTH or new_y >= GRID_HEIGHT:
                        return False
                    
                    if new_y >= 0 and self.grid[new_y][new_x]:
                        return False
        return True

    def rotate_piece(self, piece):
        shape = piece['shape']
        rows = len(shape)
        cols = len(shape[0])
        new_shape = [[shape[rows - 1 - j][i] for j in range(rows)] for i in range(cols)]
        return new_shape

    def lock_piece(self):
        for y, row in enumerate(self.current_piece['shape']):
            for x, cell in enumerate(row):
                if cell:
                    if self.current_piece['y'] + y < 0:
                        self.game_over = True
                        self.check_high_score()
                        return
                    self.grid[self.current_piece['y'] + y][self.current_piece['x'] + x] = self.current_piece['color']
        
        self.clear_lines()
        self.current_piece = self.next_piece
        self.next_piece = self.new_piece()
        
        if not self.valid_move(self.current_piece, 0, 0):
            self.game_over = True
            self.check_high_score()

    def clear_lines(self):
        lines_cleared = 0
        for y in range(GRID_HEIGHT - 1, -1, -1):
            if all(self.grid[y]):
                del self.grid[y]
                self.grid.insert(0, [0 for _ in range(GRID_WIDTH)])
                lines_cleared += 1
        
        self.score += lines_cleared * 100 * (lines_cleared + 1) // 2

    def check_high_score(self):
        if self.high_score_manager:
            self.new_high_score = self.high_score_manager.update_score(self.difficulty, self.score)

    def draw(self, screen):
        screen.fill(BLACK)
        
        for y in range(GRID_HEIGHT):
            for x in range(GRID_WIDTH):
                if self.grid[y][x]:
                    pygame.draw.rect(screen, COLORS[self.grid[y][x]],
                                   (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
                    pygame.draw.rect(screen, BLACK,
                                   (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE), 1)
        
        for y, row in enumerate(self.current_piece['shape']):
            for x, cell in enumerate(row):
                if cell:
                    pygame.draw.rect(screen, COLORS[self.current_piece['color']],
                                   ((self.current_piece['x'] + x) * CELL_SIZE,
                                    (self.current_piece['y'] + y) * CELL_SIZE,
                                    CELL_SIZE, CELL_SIZE))
                    pygame.draw.rect(screen, BLACK,
                                   ((self.current_piece['x'] + x) * CELL_SIZE,
                                    (self.current_piece['y'] + y) * CELL_SIZE,
                                    CELL_SIZE, CELL_SIZE), 1)
        
        pygame.draw.rect(screen, WHITE, (0, 0, GRID_WIDTH * CELL_SIZE, GRID_HEIGHT * CELL_SIZE), 2)
        
        font = get_chinese_font(36)
        small_font = get_chinese_font(28)
        
        score_text = font.render(f'得分: {self.score}', True, WHITE)
        screen.blit(score_text, (GRID_WIDTH * CELL_SIZE + 20, 20))
        
        high_score = self.high_score_manager.get_high_score(self.difficulty) if self.high_score_manager else 0
        high_score_text = small_font.render(f'最高: {high_score}', True, YELLOW)
        screen.blit(high_score_text, (GRID_WIDTH * CELL_SIZE + 20, 60))
        
        diff_name = DIFFICULTIES[self.difficulty]['name']
        diff_text = small_font.render(f'难度: {diff_name}', True, CYAN)
        screen.blit(diff_text, (GRID_WIDTH * CELL_SIZE + 20, 90))
        
        next_text = font.render('下一个:', True, WHITE)
        screen.blit(next_text, (GRID_WIDTH * CELL_SIZE + 20, 130))
        
        for y, row in enumerate(self.next_piece['shape']):
            for x, cell in enumerate(row):
                if cell:
                    pygame.draw.rect(screen, COLORS[self.next_piece['color']],
                                   (GRID_WIDTH * CELL_SIZE + 20 + x * CELL_SIZE,
                                    170 + y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
                    pygame.draw.rect(screen, BLACK,
                                   (GRID_WIDTH * CELL_SIZE + 20 + x * CELL_SIZE,
                                    170 + y * CELL_SIZE, CELL_SIZE, CELL_SIZE), 1)
        
        if self.game_over:
            game_over_text = font.render('游戏结束!', True, RED)
            screen.blit(game_over_text, (GRID_WIDTH * CELL_SIZE // 2 - 80, GRID_HEIGHT * CELL_SIZE // 2 - 40))
            
            if self.new_high_score:
                new_record_text = font.render('新纪录!', True, YELLOW)
                screen.blit(new_record_text, (GRID_WIDTH * CELL_SIZE // 2 - 60, GRID_HEIGHT * CELL_SIZE // 2))
            
            restart_text = small_font.render('按 R 重新开始', True, WHITE)
            screen.blit(restart_text, (GRID_WIDTH * CELL_SIZE // 2 - 80, GRID_HEIGHT * CELL_SIZE // 2 + 40))
            
            menu_text = small_font.render('按 M 返回菜单', True, WHITE)
            screen.blit(menu_text, (GRID_WIDTH * CELL_SIZE // 2 - 80, GRID_HEIGHT * CELL_SIZE // 2 + 70))

    def run(self, screen):
        while True:
            dt = self.clock.tick(60)
            self.fall_time += dt
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return 'quit'
                
                if event.type == pygame.KEYDOWN:
                    if self.game_over:
                        if event.key == pygame.K_r:
                            self.__init__(self.difficulty, self.high_score_manager)
                        elif event.key == pygame.K_m:
                            return 'menu'
                    else:
                        if event.key == pygame.K_LEFT:
                            if self.valid_move(self.current_piece, -1, 0):
                                self.current_piece['x'] -= 1
                        elif event.key == pygame.K_RIGHT:
                            if self.valid_move(self.current_piece, 1, 0):
                                self.current_piece['x'] += 1
                        elif event.key == pygame.K_DOWN:
                            if self.valid_move(self.current_piece, 0, 1):
                                self.current_piece['y'] += 1
                        elif event.key == pygame.K_UP:
                            new_shape = self.rotate_piece(self.current_piece)
                            if self.valid_move(self.current_piece, 0, 0, new_shape):
                                self.current_piece['shape'] = new_shape
                        elif event.key == pygame.K_SPACE:
                            while self.valid_move(self.current_piece, 0, 1):
                                self.current_piece['y'] += 1
                            self.lock_piece()
                        elif event.key == pygame.K_ESCAPE:
                            return 'menu'
            
            if not self.game_over:
                if self.fall_time >= self.fall_speed:
                    if self.valid_move(self.current_piece, 0, 1):
                        self.current_piece['y'] += 1
                    else:
                        self.lock_piece()
                    self.fall_time = 0
            
            self.draw(screen)
            pygame.display.flip()

def main():
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('俄罗斯方块')
    
    high_score_manager = HighScoreManager()
    
    while True:
        menu = Menu(screen, high_score_manager)
        difficulty = menu.run()
        
        if difficulty == 'quit' or difficulty is None:
            pygame.quit()
            break
        
        game = Tetris(difficulty, high_score_manager)
        result = game.run(screen)
        
        if result == 'quit':
            pygame.quit()
            break

if __name__ == '__main__':
    main()
