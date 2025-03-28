import pyxel


class Game():
    def __init__(self):
        pyxel.init(80, 120, "meteor survival")
        pyxel.load("meteor.pyxres")

        self.index = 0  # 0はタイトル画面　1ゲーム中　2ゲームオーバー
        self.ship_x = 40 - 4
        self.ship_y = 100
        self.ship_speed = 1
        self.meteor_speed = 1
        self.score = 0
        self.meteors = []
        self.hit_range = 4
        self.is_hitting = False
        self.meteor_interval = 45  # 隕石生成間隔（初期値）

        pyxel.run(self.update, self.draw)


    def ship_update(self):
        # 自機移動
        if pyxel.btn(pyxel.KEY_RIGHT):
            self.ship_x += self.ship_speed
        if pyxel.btn(pyxel.KEY_LEFT):
            self.ship_x -= self.ship_speed

        # 壁判定
        if self.ship_x >= 80 - 4:
            self.ship_x = 80 - 4
        if self.ship_x <= - 4:
            self.ship_x =  - 4

    def ship_draw(self):
        pyxel.blt(self.ship_x, self.ship_y, 0, 0, 0, 8, 8, 0)

    def collision(self):
        for i in range(len(self.meteors)):
            mx = self.meteors[i][0]
            my = self.meteors[i][1]
            if (mx - self.ship_x)**2 + (my - self.ship_y)**2 < self.hit_range**2:
                self.index = 2 #game over
                self.is_hitting = True
                break

    def meteor_update(self):
        if pyxel.frame_count % self.meteor_interval == 0:
            x = pyxel.rndi(-4, 80 - 4)
            self.meteors.append((x, -8))  # ランダムに隕石を生成

        for i in range(len(self.meteors)):
            self.meteors[i] = (self.meteors[i][0], self.meteors[i][1] + self.meteor_speed)

        self.meteors = [meteor for meteor in self.meteors if meteor[1] <= 120]  

        #　隕石の出現頻度増加
        if pyxel.frame_count % 50 == 0:
            self.meteor_speed += 0.02
            self.meteor_interval -= 2
            if self.meteor_interval < 2:
                self.meteor_interval = 2
            
        

    def meteor_draw(self):
        for meteors in self.meteors:
            x, y = meteors            
            pyxel.blt(x, y, 0, 8, 0, 8, 8, 0)

    def reset(self):
        self.meteors = [] #隕石リスト初期化
        self.ship_x = 40 - 4 #自機初期位置
        self.ship_y = 100 #自機初期位置
        self.is_hitting = False #衝突フラグ初期化
        self.score = 0
        self.meteor_interval = 60  # 隕石生成間隔（初期値）
        self.meteor_speed = 1

    def update(self):
        if self.index == 0:
            if pyxel.btnp(pyxel.KEY_SPACE):
                self.reset()
                self.index = 1
        elif self.index == 1:
            self.ship_update()
            self.meteor_update()
            self.collision()
            if pyxel.frame_count % 20 == 0:
                self.score += 10
        elif self.index == 2:
            if pyxel.btnp(pyxel.KEY_SPACE):
                self.reset()
                self.index = 1
                


    def draw(self):
        if self.index == 0:
            pyxel.cls(0)
            pyxel.text(10, 40, "PRESS SPACE KEY", 7)
        elif self.index == 1:
            pyxel.cls(0)
            self.ship_draw()
            self.meteor_draw()
            pyxel.text(6, 6, f"SCORE:{self.score}", 0)
            pyxel.text(5, 5, f"SCORE:{self.score}", 7)
        elif self.index == 2:
            pyxel.text(21, 41, "GAME OVER", 0)
            pyxel.text(20, 40, "GAME OVER", pyxel.frame_count % 16)
            pyxel.text(30, 80, "RETRY", 7)
        
        

Game()