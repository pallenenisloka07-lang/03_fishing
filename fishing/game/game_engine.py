"""
GameEngine: owns the hook and the fish and runs the game logic.

Tasks completed:
Task 1 - Correct catch detection
Task 2 - Multiple fish types
Task 3 - Player-controlled casting
Task 4 - 30-second round timer
"""

import time

from game.hook import Hook, IDLE
from game.fish import Fish
from game.catch import check_catch
from game.renderer import WIDTH, HEIGHT, SURFACE_Y, MAX_DEPTH_Y


ROUND_DURATION = 30


class GameEngine:
    def __init__(self):
        self.hook = Hook(
            x=WIDTH / 2,
            surface_y=SURFACE_Y,
            max_depth_y=MAX_DEPTH_Y,
            speed=5
        )

        self.fish_list = [
            Fish(100, 180, 1.5, 36, 18, 10, (80, 180, 220)),
            Fish(400, 280, -4, 46, 22, 25, (240, 170, 60)),
            Fish(250, 380, 1.5, 36, 18, 10, (80, 180, 220)),
            Fish(550, 340, -4, 46, 22, 25, (240, 170, 60)),
        ]

        self.hooked_fish = None
        self.score = 0
        self.start_time = time.time()
        self.game_over = False

    def start_cast(self):
        if not self.game_over and self.hook.state == IDLE:
            self.hook.start_cast()

    def restart(self):
        self.__init__()

    def get_time_left(self):
        elapsed = time.time() - self.start_time
        return max(0, ROUND_DURATION - int(elapsed))

    def update(self):
        if self.game_over:
            return

        # Check timer
        if self.get_time_left() <= 0:
            self.game_over = True
            self.hook.state = IDLE
            self.hooked_fish = None
            return

        self.hook.update()

        for fish in self.fish_list:
            fish.update(WIDTH)

        if self.hooked_fish is not None:
            self.hooked_fish.x = self.hook.x
            self.hooked_fish.y = self.hook.y

            if self.hook.state == IDLE:
                self.score += self.hooked_fish.point_value
                self.hooked_fish = None

        else:
            caught = check_catch(self.hook, self.fish_list)

            if caught is not None:
                self.fish_list.remove(caught)
                self.hooked_fish = caught
                self.hooked_fish.x = self.hook.x
                self.hooked_fish.y = self.hook.y
                self.hook.catch_fish()

    def draw(self, surface, font):
        from game import renderer

        draw_list = list(self.fish_list)

        if self.hooked_fish is not None:
            draw_list.append(self.hooked_fish)

        renderer.draw_scene(
            surface,
            self.hook,
            draw_list
        )

        renderer.draw_text(
            surface,
            font,
            f"Score: {self.score}",
            (10, 10)
        )

        renderer.draw_text(
            surface,
            font,
            f"Time: {self.get_time_left()}",
            (10, 40)
        )

        if self.game_over:
            renderer.draw_text(
                surface,
                font,
                "TIME UP! Press R to restart",
                (WIDTH // 2 - 150, HEIGHT // 2)
            )