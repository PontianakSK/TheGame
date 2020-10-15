import random
import itertools

class Terraformer:
    def __init__(self, density=50, length=10, width=10):
        self.coordinate = (0,0)
        self.density = density
        self.width = width
        self.length = length
        self.gradient_map = []
        self.map = []
        self.terrain_map = []
        self.check_map = []
        self.extremum_patterns = {
            'hill': {
                'border' : (-100,),
                #center width = 2:
                'center' : (100,1),
            },
        }
        self.pattern_setters = {
            'border' : self.border,
            'center' : self.center,
        }

        for i in range(0,length):
            row_ = []
            for j in range(0,width):
                row_.append(random.gauss(0,200))
            self.gradient_map.append(row_)
        
        for i in range(0,length):
            row_ = []
            for j in range(0,width):
                row_.append(0)
            self.map.append(row_)

        for i in range(0,length):
            row_ = []
            for j in range(0,width):
                row_.append(0)
            self.terrain_map.append(row_)

        for i in range(0,length):
            row_ = []
            for j in range(0,width):
                row_.append(0)
            self.check_map.append(row_)

    def __str__(self):
        list_map = []
        for row_ in self.map:
            list_row = []
            for cell_ in row_:
                list_row.append(str(cell_))
            list_map.append(','.join(list_row))
        return '\n'.join(list_map)

    def print_terrain(self):
        list_map = []
        for row_ in self.terrain_map:
            list_row = []
            for cell_ in row_:
                list_row.append(str(cell_))
            list_map.append(','.join(list_row))
        return '\n'.join(list_map)

    def get_random_areas(self, size_x, size_y, density, count):
        coordinates = []
        areas = []
        for i in range(count):
            center = self.get_random_point()
            coordinates.append((int(center[0]-size_x/2), int(center[1]-size_y/2)))

        for point in coordinates:
            area = Terraformer(density,size_x,size_y)
            area.coordinate = point
            areas.append(area)
        return areas

    def inside(self,x,y):
        if (0<= x < self.length) and (0<= y < self.width):
            return True
        else:
            return False
        
    def apply_map(self, terraformer, override=False):
        for i in range(terraformer.length):
            for j in range(terraformer.width):
                x = i+terraformer.coordinate[0]
                y = j+terraformer.coordinate[1]
                if self.inside(x,y):
                    if self.map[x][y] == 0 or override is True:
                        self.map[x][y] = terraformer.map[i][j]

    def apply_terrain_map(self, terraformer, override=False):
        for i in range(terraformer.length):
            for j in range(terraformer.width):
                x = i+terraformer.coordinate[0]
                y = j+terraformer.coordinate[1]
                if self.inside(x,y):
                    if self.terrain_map[x][y] == 0 or override is True:
                        self.terrain_map[x][y] = terraformer.terrain_map[i][j]
    
    def set_terrain(self, number):
        terrain_code = number
        for i in range(self.length):
            for j in range(self.width):
                if self.map[i][j] == 1:
                    self.terrain_map[i][j] = terrain_code

    def center(self,value,size=0):
        x_center = set()
        y_center = set()
        x_temp = set()
        y_temp = set()
        if self.length%2 == 0:
            x_center.add(self.length/2)
            x_center.add(self.length/2 - 1)
        elif self.length%2 == 1:
            x_center.add((self.length-1)/2)
        if self.width%2 == 0:
            y_center.add(self.width/2)
            y_center.add(self.width/2 - 1)
        elif self.width%2 == 1:
            y_center.add((self.width-1)/2)
        for i in range(size):
            for each in x_center:
                x_temp.add(each+i)
                x_temp.add(each-i)
            for each in y_center:
                y_temp.add(each+i)
                y_temp.add(each-i)
        x_center.update(x_temp)
        y_center.update(y_temp)
        for i in x_center:
            for j in y_center:
                self.map[int(i)][int(j)] = value
                self.check_map[int(i)][int(j)] = 1



    def border(self, value):
        for i in [0,-1]:
            for j in range(self.width):
                self.map[i][j] = value
                self.check_map[i][j] = 1
        for i in range(self.length):
            for j in [0,-1]:
                self.map[i][j] = value
                self.check_map[i][j] = 1

                

    def get_random_point(self,x_interval=None, y_interval=None):
        if x_interval is None:
            x_interval = (0,self.length)
        if y_interval is None:
            y_interval = (0,self.width)
        x_rand = int(random.random()*(x_interval[1]-x_interval[0])+x_interval[0])
        y_rand = int(random.random()*(y_interval[1]-y_interval[0])+y_interval[0])
        return (x_rand,y_rand)
    

    def create_extremums(self, pattern_name='hill'):
        pattern = self.extremum_patterns[pattern_name]
        for each in pattern.items():
            self.pattern_setters[each[0]](*each[1])

    def check(self):
        result = 0
        for each_row in self.check_map:
            for each_cell in each_row:
                result += each_cell
        return result == self.length*self.width

    def get_neighbours(self, x, y):
        result = []
        list_1 = [1,0,-1]
        closest = list(itertools.product(list_1,list_1))
        closest.remove((0,0))
        for each in closest:
            if (0 <= x+each[0] < self.length) and (0 <= y+each[1] < self.width):
                result.append((x+each[0],y+each[1]))
        return result


    def apply_gradients(self):
        while not self.check():
            for i in range(self.length):
                for j in range(self.width):
                    if self.check_map[i][j] !=1 :
                        neighbours = self.get_neighbours(i,j)
                        value = 0
                        for x,y in neighbours:
                            if self.check_map[x][y] == 1:
                                value += self.map[x][y]
                                value += self.gradient_map[x][y]
                        if bool(neighbours) and value != 0:
                            to_set = value/len(neighbours)
                            self.map[i][j] = int(min(abs(to_set),100)*to_set/abs(to_set))
            for i in range(self.length):
                for j in range(self.width):
                    if self.map[i][j] != 0:
                        self.check_map[i][j] = 1
    
    def normalize_map(self):
        for i in range(self.length):
                for j in range(self.width):
                    if self.map[i][j] < 50-self.density :
                        self.map[i][j] = 0
                    else:
                        self.map[i][j] = 1

    def create_object(self, pattern_name='hill'):
        self.create_extremums(pattern_name)
        self.apply_gradients()
        self.normalize_map()