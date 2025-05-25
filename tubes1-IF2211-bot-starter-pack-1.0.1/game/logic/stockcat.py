import math
from typing import Optional
from game.logic.base import BaseLogic
from game.models import GameObject, Board, Position
from ..util import get_direction


class StockCat(BaseLogic):
    def __init__(self):
        self.goal_position: Optional[Position] = None

    def distance(self, a: Position, b: Position) -> int:
        return abs(a.x - b.x) + abs(a.y - b.y)  # Manhattan distance

    def next_move(self, board_bot: GameObject, board: Board):
        bot_props = board_bot.properties
        bot_pos = board_bot.position

        # Inventory penuh? Kembali ke base
        if bot_props.diamonds >= bot_props.inventory_capacity:
            self.goal_position = bot_props.base
        else:
            best_score = -1
            best_pos = None

            for obj in board.game_objects:
                if obj.type == "DiamondGameObject":
                    # Nilai diamond: 2 (red), 1 (blue)
                    value = 2 if obj.properties.get("score") == 2 else 1
                    dist = self.distance(bot_pos, obj.position)
                    if dist == 0:
                        continue  # Sudah di posisi ini
                    score_ratio = value / dist
                    if score_ratio > best_score:
                        best_score = score_ratio
                        best_pos = obj.position

            if best_pos:
                self.goal_position = best_pos
            else:
                # Jika tidak ada diamond, kembali ke base
                self.goal_position = bot_props.base

        # Hitung arah ke goal
        delta_x, delta_y = get_direction(
            bot_pos.x,
            bot_pos.y,
            self.goal_position.x,
            self.goal_position.y
        )

        return delta_x, delta_y
