from object_3d import *
from camera import *
from projection import *
import pygame as pg
import square
from concurrent import futures
from control import Control

class SoftwareRender:
    def __init__(self) -> None:
        self.setting = {
            "clipping_mode": False,
            "show_coordinates": False,
            "show_basis_axis": True,
            "animation_duration": 10000,
        } 
        pool.submit(self.tkinit)
        pg.init()
        self.HEIGHT = 900
        self.WIDTH  = 1600
        self.RES = self.WIDTH, self.HEIGHT
        self.H_WIDTH, self.H_HEIGHT = self.WIDTH // 2, self.HEIGHT // 2
        self.FPS = 60
        self.screen = pg.display.set_mode(self.RES)
        self.clock = pg.time.Clock()
        self.create_objects()  
   
    def tkinit(self):
        try:
            Control("Control",self)
        except Exception as e:
            print(e)

    def create_objects(self):
        self.change_coordinate_matrix = np.array(
            [[1, 0, 0, 0], [0, 0, 1, 0], [0, 1, 0, 0], [0, 0, 0, 1]]
        )
        self.animation = np.array(
            [
                [1, 0, 0, 0],
                [0, 1, 0, 0],
                [0, 0, 1, 0],
                [0, 0, 0, 1],
            ]
        )
        self.camera = Camera(self, [3,1,-4])
        self.camera.camera_pitch(0.1)
        self.camera.camera_yaw(-math.pi/6)
        self.projection = Projection(self)

        self.object = Object3D(
            self,
            vertices=square.sqaure_vertices,
            faces=square.square_faces,
            animation=self.animation,
            transformation=self.change_coordinate_matrix,
        )
        # self.object.translate([5, 1, 2])
        # self.object.scale(0.08)
        # self.object.rotate_y(math.pi / 6)
        self.axis = Axis(self, transformation=self.change_coordinate_matrix, animation=self.animation)
        self.axis.translate([0.5, 0.5, 0.5])
        self.world_axis = Axis(self, transformation=self.change_coordinate_matrix)
        self.world_axis.movement_flag = False
        self.world_axis.scale(2)
        self.world_axis.translate([0.0001, 0.0001, 0.0001])

    def draw_3d_render_area(self):
        pg.draw.polygon(
            self.screen,
            pg.Color("white"),
            [[0, 0], [self.RES[0], 0], self.RES, [0, self.RES[1]]],
            3,
        )

    def draw(self):
        self.screen.fill(pg.Color("black"))
        self.camera.display_coord()
        if(self.setting["show_basis_axis"]):
            self.axis.draw()
        self.object.draw()
        self.world_axis.draw()
        # self.draw_3d_render_area()

    def run(self):
        while True:
            self.draw()
            self.camera.control()
            [exit() for i in pg.event.get() if i.type == pg.QUIT]
            pg.display.flip()
            self.clock.tick(self.FPS)


if __name__ == "__main__":
    pool = futures.ThreadPoolExecutor(max_workers=10)
    np.set_printoptions(suppress=True, formatter={"float": "{:0.02f}".format})
    app = SoftwareRender()
    app.run()
