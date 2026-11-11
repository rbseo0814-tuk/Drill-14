from pico2d import *
import game_world
import game_framework
from boy import Boy
from grass import Grass
from bird import Bird

boy = None


def handle_events():


    event_list = get_events()
    for event in event_list:
        if event.type == SDL_QUIT:
            game_framework.quit()
            return
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        else:
            boy.handle_event(event)


def init():
    global boy

    boy = Boy()
    game_world.add_oject(boy)

    grass = Grass()
    game_world.add_oject(grass, 0)

    game_world.add_oject(Bird())


def pause():
    boy.pause()


def resume():
    pass


def finish():
    global boy
    game_world.clear()
    boy = None


def update():
    game_world.update()
    # delay(0.1)  # p.25 실습: 강제적인 프레임 시간 증가 (테스트할 때 주석 해제)

def render():
    clear_canvas()
    game_world.render()
    update_canvas()









