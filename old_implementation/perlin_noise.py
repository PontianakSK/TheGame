import random

class PerlinNoise:

    def __init__(self,frequency, seed=None):
        if seed != None:
            random.seed(seed)
        self.gradients = {}
        self.frequency = frequency
        self.set_gradients()

    def set_gradients(self):
        for y in range(self.frequency):
            for x in range(self.frequency):
                grad_x = round(random.random(),2)
                grad_y = round(random.random(),2)
                self.gradients[y,x] = [grad_y,grad_x]

    def dot_grid_gradient(self,iy,ix,y,x):
        dx = x-ix
        dy = y-iy
        grad = self.gradients[iy,ix]
        return (1-dy)*grad[0]+(1-dx)*grad[1]

    def lerp(self,a_0,a_1,w):
        return (1-w)*a_0+w*a_1

    def perlin(self,y_perc,x_perc):
        y = y_perc*(self.frequency-1)
        x = x_perc*(self.frequency-1)
        x_0 = int(x)
        x_1 = x_0 + 1
        y_0 = int(y)
        y_1 = y_0 + 1
        sx = x-x_0
        sy = y-y_0
        n_0 = self.dot_grid_gradient(y_0,x_0,y,x)
        n_1 = self.dot_grid_gradient(y_0,x_1,y,x)
        ix0 = self.lerp(n_0,n_1,sx)
        n_0 = self.dot_grid_gradient(y_1,x_0,y,x)
        n_1 = self.dot_grid_gradient(y_1,x_1,y,x)
        ix1 = self.lerp(n_0,n_1,sx)
        value = self.lerp(ix0,ix1,sy)
        return value

