from browser import document, timer, alert, window
import math
import random

# --- Core Engine ---
class AntigravityEngine:
    def __init__(self, canvas_id):
        self.canvas = document[canvas_id]
        self.ctx = self.canvas.getContext('2d')
        self.w = self.canvas.width
        self.h = self.canvas.height

    def clear(self):
        # Background tray
        grad = self.ctx.createLinearGradient(0, 0, 0, self.h)
        grad.addColorStop(0, "#fff5f8")
        grad.addColorStop(1, "#fce4ec")
        self.ctx.fillStyle = grad
        self.ctx.fillRect(0, 0, self.w, self.h)

    def round_rect(self, x, y, w, h, r):
        # Compatibility helper for roundRect
        if hasattr(self.ctx, "roundRect"):
            self.ctx.beginPath()
            self.ctx.roundRect(x, y, w, h, r)
        else:
            self.ctx.beginPath()
            self.ctx.moveTo(x + r, y)
            self.ctx.lineTo(x + w - r, y)
            self.ctx.quadraticCurveTo(x + w, y, x + w, y + r)
            self.ctx.lineTo(x + w, y + h - r)
            self.ctx.quadraticCurveTo(x + w, y + h, x + w - r, y + h)
            self.ctx.lineTo(x + r, y + h)
            self.ctx.quadraticCurveTo(x, y + h, x, y + h - r)
            self.ctx.lineTo(x, y + r)
            self.ctx.quadraticCurveTo(x, y, x + r, y)
            self.ctx.closePath()

    def draw_egg(self, x, y):
        # Shadow
        self.ctx.beginPath()
        self.ctx.ellipse(x+3, y+5, 24, 30, 0.2, 0, math.pi*2)
        self.ctx.fillStyle = "rgba(0,0,0,0.1)"
        self.ctx.fill()
        # Shell
        grad = self.ctx.createRadialGradient(x-8, y-10, 5, x, y, 35)
        grad.addColorStop(0, "#ffffff")
        grad.addColorStop(1, "#f5f5f5")
        self.ctx.beginPath()
        self.ctx.ellipse(x, y, 25, 32, 0.1, 0, math.pi*2)
        self.ctx.fillStyle = grad
        self.ctx.fill()
        self.ctx.strokeStyle = "#e0e0e0"
        self.ctx.lineWidth = 1
        self.ctx.stroke()

    def draw_flour(self, x, y):
        # Shadow
        self.ctx.fillStyle = "rgba(0,0,0,0.1)"
        self.ctx.fillRect(x-35, y+35, 70, 10)
        # Paper Bag
        grad = self.ctx.createLinearGradient(x-30, y-40, x+30, y+40)
        grad.addColorStop(0, "#d7ccc8")
        grad.addColorStop(1, "#a1887f")
        self.ctx.beginPath()
        self.ctx.moveTo(x-30, y+40); self.ctx.lineTo(x+30, y+40)
        self.ctx.lineTo(x+35, y-10); self.ctx.lineTo(x-35, y-10)
        self.ctx.closePath()
        self.ctx.fillStyle = grad; self.ctx.fill()
        self.ctx.strokeStyle = "#8d6e63"; self.ctx.lineWidth = 2; self.ctx.stroke()
        # Labels
        self.ctx.fillStyle = "#ffffff"
        self.ctx.fillRect(x-20, y, 40, 20)
        self.ctx.fillStyle = "#5d4037"
        self.ctx.font = "bold 10px Arial"
        self.ctx.textAlign = "center"
        self.ctx.fillText("FARINHA", x, y+14)

    def draw_sugar(self, x, y):
        # Glass Jar Effect
        grad = self.ctx.createLinearGradient(x-30, y, x+30, y)
        grad.addColorStop(0, "rgba(255,255,255,0.8)")
        grad.addColorStop(0.5, "rgba(224,247,250,0.4)")
        grad.addColorStop(1, "rgba(255,255,255,0.8)")
        self.round_rect(x-30, y-40, 60, 80, 12)
        self.ctx.fillStyle = grad; self.ctx.fill()
        self.ctx.strokeStyle = "rgba(255,255,255,0.5)"; self.ctx.lineWidth = 2; self.ctx.stroke()
        
        # Crystals
        self.ctx.fillStyle = "rgba(255,255,255,0.9)"
        for i in range(12):
             self.ctx.fillRect(x-18 + (i%4)*10, y + (i//4)*12, 4, 4)
        
        # Lid
        self.ctx.fillStyle = "#ec407a"
        self.ctx.fillRect(x-32, y-45, 64, 15)

    def draw_cake(self, x, y, size, flavor_color, frosting_type=None):
        # Shadows
        self.ctx.fillStyle = "rgba(0,0,0,0.1)"
        self.ctx.beginPath(); self.ctx.ellipse(x, y+40*size, 130*size, 20*size, 0, 0, 7); self.ctx.fill()

        # Base layer
        self.round_rect(x - 120*size, y - 50*size, 240*size, 100*size, 20*size)
        self.ctx.fillStyle = flavor_color; self.ctx.fill()
        self.ctx.strokeStyle = "#3e2723"; self.ctx.lineWidth = 2; self.ctx.stroke()
        
        # Top layer
        self.round_rect(x - 90*size, y - 110*size, 180*size, 80*size, 15*size)
        self.ctx.fillStyle = flavor_color; self.ctx.fill()
        self.ctx.stroke()

        # Frosting
        if frosting_type == "ganache":
            self.draw_frosting(x, y, size, "#3e2723", True)
        elif frosting_type == "icing":
            self.draw_frosting(x, y, size, "#f48fb1", False)

    def draw_frosting(self, x, y, size, color, shiny):
        self.ctx.fillStyle = color
        # Top frosting
        self.round_rect(x - 95*size, y - 115*size, 190*size, 35*size, 12*size)
        self.ctx.fill()
        
        if shiny:
            self.ctx.globalAlpha = 0.4
            self.ctx.fillStyle = "white"
            self.ctx.beginPath()
            self.ctx.ellipse(x - 30*size, y - 105*size, 45*size, 6*size, 0, 0, math.pi*2)
            self.ctx.fill()
            self.ctx.globalAlpha = 1.0

# --- Game Class ---
class Game:
    def __init__(self):
        self.engine = AntigravityEngine("gameCanvas")
        self.state = "MENU"
        self.score = 0
        self.baking_progress = 0.0
        self.baking_speed = 0.28
        self.cake_flavor = "#FFF9C4"
        self.frosting = None
        self.sprinkles = []
        
        self.ingredients = [
            {"name": "Ovo", "x": 200.0, "y": 150.0, "type": "egg", "in": False, "drag": False},
            {"name": "Farinha", "x": 400.0, "y": 150.0, "type": "flour", "in": False, "drag": False},
            {"name": "Açúcar", "x": 600.0, "y": 150.0, "type": "sugar", "in": False, "drag": False}
        ]
        
        # Bind Elements
        document["btn-start"].bind("click", self.start_game)
        document["btn-oven"].bind("click", self.check_oven)
        document["btn-restart"].bind("click", self.reset_game)
        document["btn-finish"].bind("click", self.finish_game)
        
        for b in document.select(".btn-flavor"): 
            b.bind("click", self.set_flavor)
        for b in document.select(".btn-frost"): 
            b.bind("click", self.set_frosting)

        document["gameCanvas"].bind("mousedown", self.handle_down)
        document["gameCanvas"].bind("mousemove", self.handle_move)
        document["gameCanvas"].bind("mouseup", self.handle_up)

        self.loop()

    def start_game(self, ev):
        self.state = "PREPARO"
        document["btn-start"].classList.add("hidden")
        document["instructions"].text = "Arraste os ingredientes para a tigela!"

    def set_flavor(self, ev):
        self.cake_flavor = ev.target.getAttribute("data-color")
        self.score += 50
        document["flavor-menu"].classList.add("hidden")
        document["frosting-menu"].classList.remove("hidden")

    def set_frosting(self, ev):
        self.frosting = ev.target.getAttribute("data-type")
        self.score += 50
        document["frosting-menu"].classList.add("hidden")
        self.state = "DECORACAO"
        document["btn-finish"].classList.remove("hidden")
        document["instructions"].text = "Toques Finais! Adicione granulados clicando no bolo."

    def check_oven(self, ev):
        if self.state != "FORNO":
            return
            
        if 80 <= self.baking_progress <= 90:
            self.score += 500
            self.state = "CUSTOMIZACAO"
            document["btn-oven"].classList.add("hidden")
            document["flavor-menu"].classList.remove("hidden")
            document["instructions"].text = "Excelente! Escolha o sabor do seu bolo!"
        else:
            # Instead of a blocking alert, we'll reset state or show a fail message
            self.state = "FAIL"
            document["btn-oven"].classList.add("hidden")
            document["instructions"].text = "Oops! Passou do ponto. Clique para recomeçar."
            document["btn-restart"].classList.remove("hidden")

    def handle_down(self, ev):
        mx, my = self.get_pos(ev)
        if self.state == "PREPARO":
            for ing in self.ingredients:
                if not ing["in"] and math.sqrt((mx-ing["x"])**2 + (my-ing["y"])**2) < 50:
                    ing["drag"] = True
                    break
        elif self.state == "DECORACAO":
            color = random.choice(["#FF4081", "#FFD700", "#00E5FF", "#76FF03", "#D500F9"])
            self.sprinkles.append({"x": mx, "y": my, "color": color})
            self.score += 10
        elif self.state == "FAIL":
            self.reset_game(None)

    def handle_move(self, ev):
        if self.state == "PREPARO":
            mx, my = self.get_pos(ev)
            for ing in self.ingredients:
                if ing["drag"]: 
                    ing["x"], ing["y"] = mx, my

    def handle_up(self, ev):
        if self.state == "PREPARO":
            ingredient_dropped = False
            for ing in self.ingredients:
                if ing["drag"]:
                    ing["drag"] = False
                    ingredient_dropped = True
                    # Bowl centered at (400, 480)
                    if math.sqrt((float(ing["x"])-400)**2 + (float(ing["y"])-480)**2) < 120:
                        ing["in"] = True
                        self.score += 100
                    else:
                        orig = {"Ovo": 200, "Farinha": 400, "Açúcar": 600}[str(ing["name"])]
                        ing["x"], ing["y"] = orig, 150
            
            if ingredient_dropped and all(i["in"] for i in self.ingredients):
                timer.set_timeout(self.start_oven, 800)

    def start_oven(self):
        if self.state == "PREPARO":
            self.state = "FORNO"
            self.baking_progress = 0
            document["btn-oven"].classList.remove("hidden")
            document["instructions"].text = "Fique atento ao ponto perfeito (80-90%)!"

    def finish_game(self, ev):
        self.state = "FIM"
        document["btn-finish"].classList.add("hidden")
        document["btn-restart"].classList.remove("hidden")
        document["instructions"].text = f"Bolo concluído! Score Final: {self.score}"

    def reset_game(self, ev):
        window.location.reload()

    def get_pos(self, ev):
        rect = self.engine.canvas.getBoundingClientRect()
        return ev.clientX - rect.left, ev.clientY - rect.top

    def loop(self, _=0):
        self.engine.clear()
        
        ctx = self.engine.ctx
        if self.state == "MENU":
            ctx.fillStyle = "#880E4F"
            ctx.font = "bold 52px Arial"
            ctx.textAlign = "center"
            ctx.fillText("Confeitaria Mágica", 400, 280)
            ctx.font = "20px Arial"
            ctx.fillText("Experiência Gourmet de Sobremesas", 400, 320)
            
        elif self.state == "PREPARO":
            # Drawing the Bowl
            ctx.fillStyle = "#cfd8dc"
            ctx.beginPath(); ctx.arc(400, 480, 110, 0, math.pi); ctx.fill()
            ctx.beginPath(); ctx.ellipse(400, 480, 110, 25, 0, 0, math.pi*2); ctx.fillStyle = "#eceff1"; ctx.fill()
            
            for ing in self.ingredients:
                if not ing["in"]:
                    if ing["type"] == "egg": self.engine.draw_egg(ing["x"], ing["y"])
                    elif ing["type"] == "flour": self.engine.draw_flour(ing["x"], ing["y"])
                    elif ing["type"] == "sugar": self.engine.draw_sugar(ing["x"], ing["y"])

        elif self.state == "FORNO":
            self.baking_progress += self.baking_speed
            if self.baking_progress > 100:
                self.baking_progress = 100
                self.state = "FAIL"
                document["btn-oven"].classList.add("hidden")
                document["instructions"].text = "Queimou! O bolo passou do tempo. Clique para recomeçar."
                document["btn-restart"].classList.remove("hidden")
                return

            # UI Oven Drawing
            ctx.fillStyle = "#37474f"; ctx.fillRect(150, 200, 500, 300)
            ctx.fillStyle = "#263238"; ctx.fillRect(180, 230, 440, 200)
            # Progress Bar UI
            ctx.fillStyle = "#455a64"; ctx.fillRect(200, 440, 400, 30)
            # Green Zone
            ctx.fillStyle = "#66bb6a"; ctx.fillRect(200 + 400*0.8, 440, 400*0.1, 30)
            # Active Progress
            ctx.fillStyle = "#ffca28"; ctx.fillRect(200, 440, 400*(self.baking_progress/100), 30)

        elif self.state in ["CUSTOMIZACAO", "DECORACAO", "FIM"]:
            self.engine.draw_cake(400, 400, 1.4, self.cake_flavor, self.frosting)
            for s in self.sprinkles:
                ctx.fillStyle = s["color"]
                ctx.beginPath(); ctx.arc(s["x"], s["y"], 5, 0, math.pi*2); ctx.fill()

        elif self.state == "FAIL":
             ctx.fillStyle = "#d32f2f"
             ctx.font = "bold 40px Arial"
             ctx.textAlign = "center"
             ctx.fillText("BOLO PERDIDO", 400, 300)

        # Update Score only if it changed (optimization)
        if document["score-display"].text != f"Score: {self.score}":
            document["score-display"].text = f"Score: {self.score}"
            
        timer.request_animation_frame(self.loop)

Game()
