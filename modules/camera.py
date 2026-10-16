
class Camera:

  def __init__(self):
    self.cam_x = 0
    self.cam_y = 0

  def move(self, dx, dy):
    self.cam_x += dx
    self.cam_y += dy

  def get_position(self):
    return self.cam_x, self.cam_y


ma_camera = Camera()
