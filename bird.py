from pico2d import *

import game_framework

# 월드 스케일: boy.py 와 동일하게 10 pixel = 30 cm
PIXEL_PER_METER = (10.0 / 0.3)

# 날갯짓 애니메이션: 시트의 14프레임이 날갯짓 1회(위 -> 아래 -> 위)
TIME_PER_ACTION = 0.4  # 날갯짓 1회에 걸리는 시간(초)
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION  # 초당 날갯짓 횟수
FRAMES_PER_ACTION = 14  # 날갯짓 1회의 애니메이션 프레임 수

# 크기: 시트 한 칸(가로 182px)이 실제 1.5m 가 되도록 축소해서 그림
CELL_W = 182
BIRD_SIZE_M = 1.5
DRAW_SCALE = BIRD_SIZE_M * PIXEL_PER_METER / CELL_W

# bird_animation.png(918 x 506) 분석 결과.
# 시트는 5열 x 3행(마지막 행 4개)이지만 행 간격이 균일하지 않아서
# 프레임마다 잘라낼 영역과 기준점(눈동자 중심)을 직접 측정해 둠.
# (left, bottom, width, height, eye_x, eye_y) - pico2d 좌표(원점 좌하단)
SHEET_FRAMES = [
    (0, 326, 182, 180, 123.2, 412.7),
    (182, 326, 182, 180, 305.2, 413.5),
    (364, 326, 182, 180, 487.6, 415.4),
    (546, 326, 182, 180, 669.6, 418.4),
    (728, 326, 182, 180, 851.6, 421.4),
    (0, 151, 182, 175, 123.2, 251.7),
    (182, 151, 182, 175, 305.6, 253.4),
    (364, 151, 182, 175, 487.2, 252.5),
    (546, 151, 182, 175, 669.6, 252.4),
    (728, 151, 182, 175, 851.6, 250.4),
    (0, 0, 182, 151, 123.6, 77.4),
    (182, 0, 182, 151, 305.2, 74.5),
    (364, 0, 182, 151, 487.2, 73.5),
    (546, 0, 182, 151, 669.2, 72.7),
]

# 각 프레임을 그릴 때 "눈동자 -> 잘라낸 영역의 중심" 까지의 오프셋을 미리 계산.
# 새의 위치(x, y)를 눈동자 위치로 보고, 그림 중심을 이 오프셋만큼 옮겨 그리면
# 프레임이 바뀌어도 몸통이 떨리지 않음.
FRAMES = []
for left, bottom, w, h, eye_x, eye_y in SHEET_FRAMES:
    offset_x = (left + w / 2) - eye_x
    offset_y = (bottom + h / 2) - eye_y
    FRAMES.append((left, bottom, w, h, offset_x, offset_y))


class Bird:
    image = None

    def __init__(self, x=800, y=450):
        if Bird.image is None:
            Bird.image = load_image('bird_animation.png')
        self.x, self.y = x, y
        self.frame = 0.0

    def update(self):
        # 초당 증가시킬 프레임 수 = 날갯짓 1회의 프레임 수 * 초당 날갯짓 횟수
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % FRAMES_PER_ACTION

    def draw(self):
        left, bottom, w, h, offset_x, offset_y = FRAMES[int(self.frame)]
        Bird.image.clip_draw(left, bottom, w, h,
                             self.x + offset_x * DRAW_SCALE, self.y + offset_y * DRAW_SCALE,
                             w * DRAW_SCALE, h * DRAW_SCALE)
