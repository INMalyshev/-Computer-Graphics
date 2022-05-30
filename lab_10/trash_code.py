@staticmethod
def get_float(s):
    res = None

    try:
        res = float(s)
    except:
        showerror('Ошибка приведения', f'"{s}" не приводится к float.')

        return None

    return res


@staticmethod
def get_int(s):
    res = None

    try:
        res = int(s)
    except:
        showerror('Ошибка приведения', f'"{s}" не приводится к int.')

        return None

    return res


def get_meta(self):
    x0 = self.get_float(self.text_x0.get())
    xn = self.get_float(self.text_xn.get())
    dx = self.get_float(self.text_dx.get())

    z0 = self.get_float(self.text_z0.get())
    zn = self.get_float(self.text_zn.get())
    dz = self.get_float(self.text_dz.get())

    drx = self.get_int(self.text_drx.get())
    dry = self.get_int(self.text_dry.get())
    drz = self.get_int(self.text_drz.get())

    answer = {
        'x0': x0, 'xn': xn, 'dx': dx,
        'z0': z0, 'zn': zn, 'dz': dz,
        'drx': drx, 'dry': dry, 'drz': drz,
        'function': self.functions[self.function_number.get()],
    }

    if None in answer.values():
        self.set_default()

        return None

    if xn < x0 or dx < 0:
        showerror('Ошибка значений', 'Значения для оси X неудовлетворительны.')

        return None

    if zn < z0 or dz < 0:
        showerror('Ошибка значений', 'Значения для оси Z неудовлетворительны.')

        return None

    return answer


def process(self, meta=None):
    def rotate(x, y, z, drx, dry, drz):
        v = np.array([x, y, z, 1])
        X = np.array([[1, 0, 0, 0],
                      [0, cos(drx), -sin(drx), 0],
                      [0, sin(drx), cos(drx), 0],
                      [0, 0, 0, 1]])
        Y = np.array([[cos(dry), 0, sin(dry), 0],
                      [0, 1, 0, 0],
                      [-sin(dry), 0, cos(dry), 0],
                      [0, 0, 0, 1]])
        Z = np.array([[cos(drz), -sin(drz), 0, 0],
                      [sin(drz), cos(drz), 0, 0],
                      [0, 0, 1, 0],
                      [0, 0, 0, 1]])

        v = v.dot(X)
        v = v.dot(Y)
        v = v.dot(Z)

        return v[0], v[1], v[2]

    def is_visible(x, y, top, bottom):
        if y > top[x]:
            return 1
        elif y < bottom[x]:
            return -1
        else:
            return 0

    def update_top_bottom(x, y, top, bottom):
        top[x] = max(top[x], y)
        bottom[x] = min(bottom[x], y)

    def get_intersection(x1, y1, x2, y2, x3, y3, x4, y4):
        ua = ((x4 - x3) * (y1 - y3) - (y4 - y3) * (x1 - x3)) / ((y4 - y3) * (x2 - x1) - (x4 - x3) * (y2 - y1))
        ub = ((x2 - x1) * (y1 - y3) - (y2 - y1) * (x1 - x3)) / ((y4 - y3) * (x2 - x1) - (x4 - x3) * (y2 - y1))
        x = x1 + ua * (x2 - x1)
        y = y1 + ua * (y2 - y1)

        return x, y

    def inters(x_pr, y_pr, x, y, top, bottom):
        v1 = is_visible(x_pr, y_pr, top, bottom)
        v2 = is_visible(x, y, top, bottom)

        y1, y2 = None, None
        if v1 == 0:
            if v2 == 1:
                y1, y2 = top[x_pr], top[x]
            else:
                y1, y2 = bottom[x_pr], bottom[x]
        else:
            if v2 == 1:
                y1, y2 = top[x_pr], top[x]
            else:
                y1, y2 = bottom[x_pr], bottom[x]

        xi, yi = get_intersection(x_pr, y_pr, x, y, x_pr, y1, x, y2)

        return xi, yi

    if meta is None:
        return

    x_arr = np.arange(meta['x0'], meta['xn'] + meta['dx'], meta['dx'])
    z_arr = np.arange(meta['z0'], meta['zn'] + meta['dz'], meta['dz'])
    top = {x: self.canvas.field.start.y for x in x_arr}
    # top = np.ones(x_arr.shape) * self.canvas.field.start.y
    bottom = {x: self.canvas.field.finish.y for x in x_arr}
    # bottom = np.ones(x_arr.shape) * self.canvas.field.finish.y
    x_left, y_left, x_right, y_right = None, None, None, None
    function = meta['function']
    drx, dry, drz = radians(meta['drx']), radians(meta['dry']), radians(meta['drz'])

    for z_ind, z in enumerate(z_arr):
        x_pr = x_arr[0]
        y_pr = function(x_pr, z)
        vis_pr = is_visible(x_pr, y_pr, top, bottom)
        t, b = top.copy(), bottom.copy()

        if z_ind != 0:
            self.canvas.draw_line(Vector(x_left, y_left), Vector(x_arr[0], function(x_arr[0], z)))  # NB
        x_left = x_arr[0]
        y_left = function(x_arr[0], z)

        for x_ind, x in enumerate(x_arr):
            y = function(x_arr[0], z)

            x, y, z = rotate(x, y, z, drx, dry, drz)

            vis = is_visible(x, y, t, b)

            if vis * vis_pr == 1:
                self.canvas.draw_line(Vector(x_pr, y_pr), Vector(x, y))  # NB
                update_top_bottom(x, y, top, bottom)

            elif vis_pr + vis != 0:
                xi, yi = inters(x_pr, y_pr, x, y, t, b)
                if vis != 0:
                    self.canvas.draw_line(Vector(xi, yi), Vector(x, y))  # NB
                else:
                    self.canvas.draw_line(Vector(x_pr, y_pr), Vector(xi, yi))  # NB

            vis_pr = vis
            x_pr, y_pr = x, y

        if z_ind != 0:
            self.canvas.draw_line(Vector(x_right, y_right), Vector(x_arr[-1], function(x_arr[-1], z)))  # NB
        x_right = x_arr[-1]
        y_right = function(x_arr[-1], z)