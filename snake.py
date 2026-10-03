import random
import tkinter as tk


class SnakeGame:
    def __init__(self, root):
        self.root = root
        self.root.title("贪吃蛇")
        self.root.configure(bg="#0f172a")
        self.root.resizable(False, False)

        self.cols = 20
        self.rows = 20
        self.cell_size = 24
        self.width = self.cols * self.cell_size
        self.height = self.rows * self.cell_size

        self.score = 0
        self.speed = 140
        self.running = True
        self.direction = "Right"
        self.next_direction = "Right"

        self.frame = tk.Frame(root, bg="#0f172a", padx=12, pady=12)
        self.frame.pack()

        self.score_label = tk.Label(
            self.frame,
            text="分数：0",
            font=("Microsoft YaHei", 16, "bold"),
            fg="#f8fafc",
            bg="#0f172a",
        )
        self.score_label.pack(anchor="w", pady=(0, 10))

        self.canvas = tk.Canvas(
            self.frame,
            width=self.width,
            height=self.height,
            bg="#111827",
            highlightthickness=0,
        )
        self.canvas.pack()

        self.snake = [(4, 2), (3, 2), (2, 2)]
        self.food = self.spawn_food()

        self.root.bind("<KeyPress>", self.on_key_press)
        self.root.bind("<space>", self.toggle_pause)

        self.draw()
        self.root.after(self.speed, self.step)

    def spawn_food(self):
        available = [
            (x, y)
            for x in range(self.cols)
            for y in range(self.rows)
            if (x, y) not in self.snake
        ]
        if not available:
            self.running = False
            self.draw_game_over("你赢了！")
            return (0, 0)
        return random.choice(available)

    def draw_game_over(self, msg):
        self.canvas.create_rectangle(
            40,
            self.height // 2 - 40,
            self.width - 40,
            self.height // 2 + 40,
            fill="#0b1120",
            outline="#94a3b8",
            width=2,
        )
        self.canvas.create_text(
            self.width // 2,
            self.height // 2,
            text=msg,
            font=("Microsoft YaHei", 22, "bold"),
            fill="#f8fafc",
        )
        self.canvas.create_text(
            self.width // 2,
            self.height // 2 + 30,
            text="按 R 重新开始，或按 Space 暂停/继续",
            font=("Microsoft YaHei", 10),
            fill="#cbd5e1",
        )

    def reset_game(self):
        self.score = 0
        self.speed = 140
        self.running = True
        self.direction = "Right"
        self.next_direction = "Right"
        self.snake = [(4, 2), (3, 2), (2, 2)]
        self.food = self.spawn_food()
        self.score_label.config(text="分数：0")
        self.canvas.delete("all")
        self.draw()
        self.root.after(self.speed, self.step)

    def toggle_pause(self, event=None):
        if not self.running:
            return
        self.running = not self.running
        if self.running:
            self.root.after(self.speed, self.step)
        else:
            self.canvas.create_rectangle(
                self.width // 2 - 80,
                self.height // 2 - 30,
                self.width // 2 + 80,
                self.height // 2 + 30,
                fill="#0b1120",
                outline="#94a3b8",
                width=2,
            )
            self.canvas.create_text(
                self.width // 2,
                self.height // 2,
                text="暂停",
                font=("Microsoft YaHei", 22, "bold"),
                fill="#f8fafc",
            )

    def on_key_press(self, event):
        if event.keysym in {"Up", "w", "W"}:
            if self.direction != "Down":
                self.next_direction = "Up"
        elif event.keysym in {"Down", "s", "S"}:
            if self.direction != "Up":
                self.next_direction = "Down"
        elif event.keysym in {"Left", "a", "A"}:
            if self.direction != "Right":
                self.next_direction = "Left"
        elif event.keysym in {"Right", "d", "D"}:
            if self.direction != "Left":
                self.next_direction = "Right"
        elif event.keysym == "r":
            self.reset_game()

    def step(self):
        if not self.running:
            return

        self.direction = self.next_direction
        dx, dy = {
            "Up": (0, -1),
            "Down": (0, 1),
            "Left": (-1, 0),
            "Right": (1, 0),
        }[self.direction]

        head_x, head_y = self.snake[0]
        new_head = (head_x + dx, head_y + dy)

        if (
            new_head[0] < 0
            or new_head[1] < 0
            or new_head[0] >= self.cols
            or new_head[1] >= self.rows
        ):
            self.running = False
            self.draw_game_over("游戏结束")
            return

        self.snake.insert(0, new_head)
        ate_food = new_head == self.food

        if not ate_food:
            self.snake.pop()

        if new_head in self.snake[1:]:
            self.running = False
            self.draw_game_over("游戏结束")
            return

        if ate_food:
            self.score += 1
            self.score_label.config(text=f"分数：{self.score}")
            self.food = self.spawn_food()
            self.speed = max(60, self.speed - 4)

        self.draw()
        self.root.after(self.speed, self.step)

    def draw(self):
        self.canvas.delete("all")

        for x in range(self.cols + 1):
            self.canvas.create_line(x * self.cell_size, 0, x * self.cell_size, self.height, fill="#1f2937")
        for y in range(self.rows + 1):
            self.canvas.create_line(0, y * self.cell_size, self.width, y * self.cell_size, fill="#1f2937")

        for x, y in self.snake:
            px = x * self.cell_size
            py = y * self.cell_size
            fill = "#22c55e" if (x, y) == self.snake[0] else "#4ade80"
            outline = "#166534"
            self.canvas.create_rectangle(
                px + 1,
                py + 1,
                px + self.cell_size - 1,
                py + self.cell_size - 1,
                fill=fill,
                outline=outline,
                width=2,
            )

        fx = self.food[0] * self.cell_size + self.cell_size // 2
        fy = self.food[1] * self.cell_size + self.cell_size // 2
        self.canvas.create_oval(
            fx - 7,
            fy - 7,
            fx + 7,
            fy + 7,
            fill="#ef4444",
            outline="#b91c1c",
            width=2,
        )


if __name__ == "__main__":
    root = tk.Tk()
    game = SnakeGame(root)
    root.mainloop()
