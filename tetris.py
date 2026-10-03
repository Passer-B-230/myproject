import random
import tkinter as tk


class TetrisGame:
    def __init__(self, root):
        self.root = root
        self.root.title("俄罗斯方块")
        self.root.configure(bg="#0f172a")
        self.root.resizable(False, False)

        self.cols = 10
        self.rows = 20
        self.cell_size = 28
        self.width = self.cols * self.cell_size
        self.height = self.rows * self.cell_size

        self.board = [[0] * self.cols for _ in range(self.rows)]
        self.current_piece = None
        self.next_piece = None
        self.score = 0
        self.level = 1
        self.game_over = False
        self.drop_speed = 500
        self.last_drop = 0

        self.frame = tk.Frame(root, bg="#0f172a", padx=16, pady=16)
        self.frame.pack()

        self.side_panel = tk.Frame(self.frame, bg="#0f172a")
        self.side_panel.pack(side="right", padx=(20, 0))

        self.score_label = tk.Label(
            self.side_panel,
            text="分数：0",
            font=("Microsoft YaHei", 16, "bold"),
            fg="#f8fafc",
            bg="#0f172a",
        )
        self.score_label.pack(anchor="w", pady=(0, 10))

        self.level_label = tk.Label(
            self.side_panel,
            text="等级：1",
            font=("Microsoft YaHei", 14),
            fg="#f8fafc",
            bg="#0f172a",
        )
        self.level_label.pack(anchor="w", pady=(0, 20))

        self.next_label = tk.Label(
            self.side_panel,
            text="下一个：",
            font=("Microsoft YaHei", 12, "bold"),
            fg="#f8fafc",
            bg="#0f172a",
        )
        self.next_label.pack(anchor="w", pady=(0, 8))

        self.next_canvas = tk.Canvas(
            self.side_panel,
            width=120,
            height=120,
            bg="#111827",
            highlightthickness=0,
        )
        self.next_canvas.pack()

        self.canvas = tk.Canvas(
            self.frame,
            width=self.width,
            height=self.height,
            bg="#111827",
            highlightthickness=0,
        )
        self.canvas.pack(side="left")

        self.pieces = {
            "I": [
                [(0, 0), (1, 0), (2, 0), (3, 0)],
                [(0, 0), (0, 1), (0, 2), (0, 3)],
            ],
            "O": [[(0, 0), (1, 0), (0, 1), (1, 1)]],
            "T": [
                [(1, 0), (0, 1), (1, 1), (2, 1)],
                [(1, 0), (1, 1), (2, 1), (1, 2)],
                [(0, 1), (1, 1), (2, 1), (1, 2)],
                [(1, 0), (0, 1), (1, 1), (1, 2)],
            ],
            "S": [
                [(1, 0), (2, 0), (0, 1), (1, 1)],
                [(1, 0), (1, 1), (2, 1), (2, 2)],
            ],
            "Z": [
                [(0, 0), (1, 0), (1, 1), (2, 1)],
                [(2, 0), (1, 1), (2, 1), (1, 2)],
            ],
            "J": [
                [(0, 0), (0, 1), (1, 1), (2, 1)],
                [(1, 0), (1, 1), (1, 2), (0, 2)],
                [(0, 1), (1, 1), (2, 1), (2, 2)],
                [(1, 0), (1, 1), (1, 2), (2, 0)],
            ],
            "L": [
                [(2, 0), (0, 1), (1, 1), (2, 1)],
                [(1, 0), (1, 1), (1, 2), (2, 2)],
                [(0, 1), (1, 1), (2, 1), (0, 2)],
                [(1, 0), (1, 1), (1, 2), (0, 0)],
            ],
        }

        self.colors = {
            "I": "#38bdf8",
            "O": "#facc15",
            "T": "#c084fc",
            "S": "#4ade80",
            "Z": "#f87171",
            "J": "#60a5fa",
            "L": "#fb923c",
        }

        self.root.bind("<KeyPress>", self.on_key_press)
        self.reset_game()

    def reset_game(self):
        self.board = [[0] * self.cols for _ in range(self.rows)]
        self.score = 0
        self.level = 1
        self.drop_speed = 500
        self.game_over = False
        self.update_labels()
        self.current_piece = self.create_piece()
        self.next_piece = self.create_piece()
        self.draw_next_piece()
        self.draw()
        self.root.after(self.drop_speed, self.tick)

    def create_piece(self):
        shape_name = random.choice(list(self.pieces.keys()))
        orientations = self.pieces[shape_name]
        rotation = random.randint(0, len(orientations) - 1)
        return {
            "type": shape_name,
            "cells": orientations[rotation],
            "x": self.cols // 2 - 2,
            "y": -1,
            "rotation": rotation,
        }

    def update_labels(self):
        self.score_label.config(text=f"分数：{self.score}")
        self.level_label.config(text=f"等级：{self.level}")

    def spawn_next_piece(self):
        self.current_piece = self.next_piece
        self.current_piece["x"] = self.cols // 2 - 2
        self.current_piece["y"] = -1
        self.next_piece = self.create_piece()
        self.draw_next_piece()

    def draw_next_piece(self):
        self.next_canvas.delete("all")
        piece = self.next_piece["cells"]
        min_x = min(x for x, _ in piece)
        max_x = max(x for x, _ in piece)
        min_y = min(y for _, y in piece)
        max_y = max(y for _, y in piece)

        width = max_x - min_x + 1
        height = max_y - min_y + 1
        cell = 20
        offset_x = (120 - width * cell) // 2
        offset_y = (120 - height * cell) // 2

        for x, y in piece:
            px = offset_x + (x - min_x) * cell
            py = offset_y + (y - min_y) * cell
            self.next_canvas.create_rectangle(
                px, py, px + cell, py + cell,
                fill=self.colors[self.next_piece["type"]],
                outline="#1f2937",
                width=2,
            )

    def on_key_press(self, event):
        if self.game_over:
            if event.keysym == "r":
                self.reset_game()
            return

        if event.keysym in {"Left", "a", "A"}:
            self.move_piece(-1, 0)
        elif event.keysym in {"Right", "d", "D"}:
            self.move_piece(1, 0)
        elif event.keysym in {"Down", "s", "S"}:
            self.soft_drop()
        elif event.keysym in {"Up", "w", "W"}:
            self.rotate_piece()
        elif event.keysym == "space":
            self.drop_to_bottom()

    def move_piece(self, dx, dy):
        if self.game_over:
            return False
        piece = self.current_piece
        if self.can_move(piece["x"] + dx, piece["y"] + dy, piece["cells"]):
            piece["x"] += dx
            piece["y"] += dy
            self.draw()
            return True
        return False

    def soft_drop(self):
        if self.move_piece(0, 1):
            self.score += 1
            self.update_labels()

    def rotate_piece(self):
        if self.game_over:
            return
        piece = self.current_piece
        shape = self.pieces[piece["type"]]
        next_rotation = (piece["rotation"] + 1) % len(shape)
        rotated = shape[next_rotation]

        offset = 0
        for test in range(-1, 2):
            if self.can_move(piece["x"] + test, piece["y"], rotated):
                offset = test
                break

        if self.can_move(piece["x"] + offset, piece["y"], rotated):
            piece["x"] += offset
            piece["rotation"] = next_rotation
            piece["cells"] = rotated
            self.draw()

    def can_move(self, x, y, cells):
        for cx, cy in cells:
            board_x = x + cx
            board_y = y + cy
            if board_x < 0 or board_x >= self.cols or board_y >= self.rows:
                return False
            if board_y >= 0 and self.board[board_y][board_x] != 0:
                return False
        return True

    def merge_piece(self):
        for cx, cy in self.current_piece["cells"]:
            x = self.current_piece["x"] + cx
            y = self.current_piece["y"] + cy
            if y >= 0:
                self.board[y][x] = self.current_piece["type"]

    def clear_lines(self):
        full_rows = [i for i, row in enumerate(self.board) if all(cell != 0 for cell in row)]
        for row_index in full_rows:
            del self.board[row_index]
            self.board.insert(0, [0] * self.cols)

        if full_rows:
            self.score += len(full_rows) * 10
            self.level = 1 + self.score // 100
            self.drop_speed = max(80, 500 - (self.level - 1) * 40)
            self.update_labels()

    def tick(self):
        if self.game_over:
            return

        if self.can_move(self.current_piece["x"], self.current_piece["y"] + 1, self.current_piece["cells"]):
            self.current_piece["y"] += 1
        else:
            self.merge_piece()
            self.clear_lines()
            self.spawn_next_piece()
            if not self.can_move(self.current_piece["x"], self.current_piece["y"], self.current_piece["cells"]):
                self.game_over = True
                self.draw_game_over()
                return

        self.draw()
        self.root.after(self.drop_speed, self.tick)

    def drop_to_bottom(self):
        while self.can_move(self.current_piece["x"], self.current_piece["y"] + 1, self.current_piece["cells"]):
            self.current_piece["y"] += 1
        self.merge_piece()
        self.clear_lines()
        self.spawn_next_piece()
        if not self.can_move(self.current_piece["x"], self.current_piece["y"], self.current_piece["cells"]):
            self.game_over = True
            self.draw_game_over()
            return
        self.draw()

    def draw_game_over(self):
        self.canvas.create_rectangle(
            20,
            self.height // 2 - 30,
            self.width - 20,
            self.height // 2 + 30,
            fill="#0b1120",
            outline="#94a3b8",
            width=2,
        )
        self.canvas.create_text(
            self.width // 2,
            self.height // 2,
            text="游戏结束",
            font=("Microsoft YaHei", 22, "bold"),
            fill="#f8fafc",
        )
        self.canvas.create_text(
            self.width // 2,
            self.height // 2 + 28,
            text="按 R 重新开始",
            font=("Microsoft YaHei", 10),
            fill="#cbd5e1",
        )

    def draw(self):
        self.canvas.delete("all")

        for x in range(self.cols + 1):
            self.canvas.create_line(x * self.cell_size, 0, x * self.cell_size, self.height, fill="#1f2937")
        for y in range(self.rows + 1):
            self.canvas.create_line(0, y * self.cell_size, self.width, y * self.cell_size, fill="#1f2937")

        for y, row in enumerate(self.board):
            for x, cell in enumerate(row):
                if cell:
                    self.canvas.create_rectangle(
                        x * self.cell_size + 1,
                        y * self.cell_size + 1,
                        (x + 1) * self.cell_size - 1,
                        (y + 1) * self.cell_size - 1,
                        fill=self.colors[cell],
                        outline="#1f2937",
                        width=2,
                    )

        if self.current_piece:
            for cx, cy in self.current_piece["cells"]:
                x = self.current_piece["x"] + cx
                y = self.current_piece["y"] + cy
                if y >= 0:
                    self.canvas.create_rectangle(
                        x * self.cell_size + 1,
                        y * self.cell_size + 1,
                        (x + 1) * self.cell_size - 1,
                        (y + 1) * self.cell_size - 1,
                        fill=self.colors[self.current_piece["type"]],
                        outline="#1f2937",
                        width=2,
                    )


if __name__ == "__main__":
    root = tk.Tk()
    game = TetrisGame(root)
    root.mainloop()
