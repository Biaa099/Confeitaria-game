from browser import document, timer, window, html
import math
import random

# --- Constants ---
GRAVITY = 0.8
JUMP_FORCE = -15
GROUND_Y = 350
PLAYER_X = 100
PLAYER_WIDTH = 40
OBSTACLE_SPEED = 6
MIN_SPAWN_INTERVAL = 60 # frames

class GourmetDash:
    def __init__(self, canvas_id):
        self.canvas = document[canvas_id]
        self.ctx = self.canvas.getContext('2d')
        self.w = self.canvas.width
        self.h = self.canvas.height
        
        self.state = "MENU"
        self.score = 0
        self.frame_count = 0
        
        # Player properties
        self.player_y = GROUND_Y - PLAYER_WIDTH
        self.player_vel_y = 0
        self.is_jumping = False
        
        self.obstacles = []
        self.last_spawn = 0
        
        # Bind events
        document["btn-start"].bind("click", self.start_game)
        document["btn-restart"].bind("click", self.start_game)
        window.bind("keydown", self.handle_keydown)
        
        # Start the loop
        self.update()

    def start_game(self, ev=None):
        # Force state to PLAYING and clear UI
        self.state = "PLAYING"
        self.score = 0
        self.player_y = GROUND_Y - PLAYER_WIDTH
        self.player_vel_y = 0
        self.obstacles = []
        self.frame_count = 0
        self.last_spawn = 0
        self.is_jumping = False
        
        # Hide all menus
        document["menu-screen"].classList.add("hidden")
        document["gameover-screen"].classList.add("hidden")
        document["instructions"].text = "ESPAÇO para pular!"
        document["score-display"].text = "PONTOS: 0"

    def handle_keydown(self, ev):
        # Spacebar (Code "Space" or KeyCode 32)
        if ev.keyCode == 32 or ev.code == "Space":
            ev.preventDefault() # Avoid jumping scroll
            
            if self.state == "PLAYING" and not self.is_jumping:
                self.player_vel_y = JUMP_FORCE
                self.is_jumping = True
            elif self.state == "MENU" or self.state == "GAMEOVER":
                self.start_game()

    def spawn_obstacle(self):
        # Balanced obstacle spawning
        if self.frame_count - self.last_spawn > random.randint(MIN_SPAWN_INTERVAL, 120):
            height = random.randint(40, 70)
            self.obstacles.append({
                "x": self.w,
                "y": GROUND_Y - height,
                "w": 30,
                "h": height,
                "passed": False
            })
            self.last_spawn = self.frame_count

    def check_collision(self, obs):
        # AABB Collision box (slightly smaller for fairness)
        p_hitbox = 4
        return (PLAYER_X + p_hitbox < obs["x"] + obs["w"] and
                PLAYER_X + PLAYER_WIDTH - p_hitbox > obs["x"] and
                self.player_y + p_hitbox < obs["y"] + obs["h"] and
                self.player_y + PLAYER_WIDTH - p_hitbox > obs["y"])

    def game_over(self):
        self.state = "GAMEOVER"
        document["final-score"].text = f"Pontuação: {self.score}"
        document["gameover-screen"].classList.remove("hidden")
        document["instructions"].text = "Pressione ESPAÇO para reiniciar"

    def draw_player(self):
        ctx = self.ctx
        x, y = PLAYER_X, self.player_y
        
        # Body Gradient
        grad = ctx.createLinearGradient(x, y, x + PLAYER_WIDTH, y + PLAYER_WIDTH)
        grad.addColorStop(0, "#ad1457")
        grad.addColorStop(1, "#f06292")
        
        ctx.fillStyle = grad
        # Rounded Cube
        r = 8
        ctx.beginPath()
        ctx.moveTo(x + r, y)
        ctx.lineTo(x + PLAYER_WIDTH - r, y)
        ctx.quadraticCurveTo(x + PLAYER_WIDTH, y, x + PLAYER_WIDTH, y + r)
        ctx.lineTo(x + PLAYER_WIDTH, y + PLAYER_WIDTH - r)
        ctx.quadraticCurveTo(x + PLAYER_WIDTH, y + PLAYER_WIDTH, x + PLAYER_WIDTH - r, y + PLAYER_WIDTH)
        ctx.lineTo(x + r, y + PLAYER_WIDTH)
        ctx.quadraticCurveTo(x, y + PLAYER_WIDTH, x, y + PLAYER_WIDTH - r)
        ctx.lineTo(x, y + r)
        ctx.quadraticCurveTo(x, y, x + r, y)
        ctx.fill()
        
        # Eyes
        ctx.fillStyle = "white"
        ctx.beginPath(); ctx.arc(x + 28, y + 15, 4, 0, math.pi*2); ctx.fill()

    def draw_obstacle(self, obs):
        ctx = self.ctx
        ctx.fillStyle = "#2c3e50"
        ctx.beginPath()
        ctx.moveTo(obs["x"], GROUND_Y)
        ctx.lineTo(obs["x"] + obs["w"]/2, obs["y"])
        ctx.lineTo(obs["x"] + obs["w"], GROUND_Y)
        ctx.fill()

    def update(self, _=0):
        ctx = self.ctx
        
        # Clear Canvas with BG Color
        ctx.fillStyle = "#fff5f8"
        ctx.fillRect(0, 0, self.w, self.h)
        
        # Draw Ground Line
        ctx.strokeStyle = "#ad1457"
        ctx.lineWidth = 4
        ctx.beginPath()
        ctx.moveTo(0, GROUND_Y)
        ctx.lineTo(self.w, GROUND_Y)
        ctx.stroke()
        
        if self.state == "PLAYING":
            self.frame_count += 1
            
            # Physics Y
            self.player_vel_y += GRAVITY
            self.player_y += self.player_vel_y
            
            # Ground Collision
            if self.player_y >= GROUND_Y - PLAYER_WIDTH:
                self.player_y = GROUND_Y - PLAYER_WIDTH
                self.player_vel_y = 0
                self.is_jumping = False
            
            self.spawn_obstacle()
            
            for obs in self.obstacles[:]:
                obs["x"] -= OBSTACLE_SPEED
                
                if self.check_collision(obs):
                    self.game_over()
                    break
                
                if obs["x"] + obs["w"] < 0:
                    self.obstacles.remove(obs)
                
                if not obs["passed"] and obs["x"] < PLAYER_X:
                    self.score += 1
                    obs["passed"] = True
                    document["score-display"].text = f"PONTOS: {self.score}"
            
            for obs in self.obstacles:
                self.draw_obstacle(obs)
        
        # Always draw player
        self.draw_player()

        # Keep the loop running
        timer.request_animation_frame(self.update)

# Initialize only when DOM is fully ready
if hasattr(document, 'readyState') and document.readyState == 'complete':
    GourmetDash("gameCanvas")
else:
    # Use timer to wait a bit for Brython to settle
    timer.set_timeout(lambda: GourmetDash("gameCanvas"), 100)
