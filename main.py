import sys

import pygame as pg
from OpenGL.GL import *

from constants import DEFAULT_WINDOW_SIZE, FPS_LIMIT, WINDOW_TITLE
from core.context import Context


def load_assets(context: Context):
    """Loads the dorm model, textures and shaders."""
    context.load_texture('grid', 'assets/grid.png')
    context.load_texture('chair_one_tex', 'assets/CHAIR_ONE_TEX.png')
    context.load_texture('chair_2_tex', 'assets/CHAIR_2_TEX.png')
    context.load_texture('wall_tex', 'assets/WALL_TEX.png')
    context.load_texture('celling_tex', 'assets/CELLING_TEX.png')
    context.load_texture('floor_tex', 'assets/FLOOR_TEX.png')
    context.load_texture('table_tex', 'assets/TABLE_TEX.png')
    context.load_texture('papers_1_tex', 'assets/PAPERS_1_TEX.png')

    default_shader = context.load_shader(
        'default_shader', 'assets/vertex_shader.vert', 'assets/fragment_shader.frag')

    context.create_material("default_material", "default_shader", {
        'texture': ("texture", 'grid', 0)
    })

    context.create_material("chair_one", "default_shader", {
        'texture': ("texture", 'chair_one_tex', 0)
    })

    context.create_material("chair_two", "default_shader", {
        'texture': ("texture", 'chair_2_tex', 0)
    })

    context.create_material("wall", "default_shader", {
        'texture': ("texture", 'wall_tex', 0)
    })

    context.create_material("celling", "default_shader", {
        'texture': ("texture", 'celling_tex', 0)
    })

    context.create_material("floor", "default_shader", {
        'texture': ("texture", 'floor_tex', 0)
    })

    context.create_material("table", "default_shader", {
        'texture': ("texture", 'table_tex', 0)
    })

    context.create_material("papers_1", "default_shader", {
        'texture': ("texture", 'papers_1_tex', 0)
    })

    chair_one = context.scene.load_mesh('assets/CHAIR_ONE.obj')
    chair_one.material_name = 'chair_one'

    chair_two = context.scene.load_mesh('assets/CHAIR_2.obj')
    chair_two.material_name = 'chair_two'

    wall = context.scene.load_mesh('assets/WALL.obj')
    wall.material_name = 'wall'

    ceiling = context.scene.load_mesh('assets/CELLING.obj')
    ceiling.material_name = 'celling'

    floor = context.scene.load_mesh('assets/FLOOR.obj')
    floor.material_name = 'floor'

    table = context.scene.load_mesh('assets/TABLE.obj')
    table.material_name = 'table'

    papers_1 = context.scene.load_mesh('assets/PAPERS_1.obj')
    papers_1.material_name = 'papers_1'

    # Compile Shaders
    default_shader.compile()


def main():
    """Main function."""
    context = Context()

    # Window creation and OpenGL context creation
    init_pygame()

    glEnable(GL_DEPTH_TEST)
    glDepthFunc(GL_LESS)

    # Loads the dorm model, textures and shaders
    load_assets(context)

    glClearColor(0., 0., 0., 1)
    glEnable(GL_MULTISAMPLE)

    dt = 0
    clock = pg.time.Clock()
    clock.tick(FPS_LIMIT)

    # Main event loop
    forward_motion = 0.0
    right_motion = 0.0
    up_motion = 0.0

    while True:
        # Input processing

        for event in pg.event.get():
            if event.type == pg.QUIT:
                sys.exit()
            elif event.type == pg.VIDEORESIZE:
                context.camera.aspect_ratio = event.w / event.h
                context.camera.window_size = event.w, event.h
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_w:
                    forward_motion = 1.0
                elif event.key == pg.K_s:
                    forward_motion = -1.0
                elif event.key == pg.K_a:
                    right_motion = -1.0
                elif event.key == pg.K_d:
                    right_motion = 1.0
                elif event.key == pg.K_e:
                    up_motion = 1.0
                elif event.key == pg.K_q:
                    up_motion = -1.0

            elif event.type == pg.KEYUP:
                if event.key == pg.K_w or event.key == pg.K_s:
                    forward_motion = 0.0
                if event.key == pg.K_a or event.key == pg.K_d:
                    right_motion = 0.0
                if event.key == pg.K_e or event.key == pg.K_q:
                    up_motion = 0.0

        if pg.mouse.get_pressed()[0]:
            delta_mouse = pg.mouse.get_rel()
            context.camera.update(
                delta_mouse, forward_motion, right_motion, up_motion, dt)
        else:
            pg.mouse.get_rel()
            context.camera.update((0, 0), forward_motion,
                                  right_motion, up_motion, dt)

        # Clear the screen
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        context.scene.draw(context)

        # Swap front and back buffers
        pg.display.flip()

        dt = clock.tick(FPS_LIMIT) / 1000.0


def init_pygame():
    pg.init()

    pg.display.gl_set_attribute(pg.GL_CONTEXT_MAJOR_VERSION, 4)
    pg.display.gl_set_attribute(pg.GL_CONTEXT_MINOR_VERSION, 1)
    pg.display.gl_set_attribute(
        pg.GL_CONTEXT_PROFILE_MASK, pg.GL_CONTEXT_PROFILE_CORE)

    pg.display.set_mode(DEFAULT_WINDOW_SIZE,
                        pg.DOUBLEBUF | pg.OPENGL | pg.RESIZABLE)
    pg.display.gl_set_attribute(pg.GL_MULTISAMPLEBUFFERS, 1)
    pg.display.set_caption(WINDOW_TITLE)


if __name__ == "__main__":
    main()
