import pygame.camera


class Camera(object):
    def __init__(self, camera_index=0, **argd):
        self.__dict__.update(**argd)
        super(Camera, self).__init__(**argd)
        pygame.camera.init(None)

        self.init_cams(camera_index)
        self.main_surface = pygame.surface.Surface((640, 360), 0)
        self.main_surface.fill((15, 15, 15))

    def init_cams(self, which_cam_idx):
        self.clist = pygame.camera.list_cameras()

        try:
            cam_id = self.clist[which_cam_idx]
        except IndexError:
            cam_id = self.clist[0]

        try:
            self.camera = pygame.camera.Camera(cam_id, (640, 360), "RGB")
        except ValueError:
            self.camera = pygame.camera.Camera(cam_id, (640, 480), "RGB")

        self.camera.set_controls(bool(1))  # flip camera horisontal

        self.camera.start()

    def start(self):
        try:
            self.snapshot = self.camera.get_image()

            self.main_surface.blit(self.snapshot, (0, 0))

            if self.camera.get_size() == (640, 360):
                self.main_surface_resize = pygame.transform.scale(self.main_surface,
                                                                  (self.main_surface.get_width() // 1.4,
                                                                   self.main_surface.get_height() // 1.4))
                pygame.draw.rect(self.main_surface_resize,
                                 (15, 15, 15),
                                 (-6, -6,
                                  self.main_surface_resize.get_size()[0] + 12, self.main_surface_resize.get_size()[1] + 12),
                                 width=5, border_radius=20)
            else:
                self.main_surface_resize = pygame.transform.scale(self.main_surface,
                                                                  (self.main_surface.get_width() // 1.4,
                                                                   self.main_surface.get_height() // 1.4))
                pygame.draw.rect(self.main_surface_resize,
                                 (15, 15, 15),
                                 (-6, -6,
                                  self.main_surface_resize.get_size()[0] + 12, self.main_surface_resize.get_size()[1] + 12),
                                 width=5, border_radius=20)
            return self.main_surface_resize
        except SystemError:
            print("Camera already in use")

    def restart(self):
        self.camera.stop()
        #pygame.camera.Camera.stop(self.camera)
