def transform(self, x, y):
        #return self.transform_perspective(x, y)
        return self.transform_2D(x, y)
    
def transform_2D(self, x, y):
        return int(x), int(y)

def transform_perspective(self, x, y):
        tr_y = y * self.perspective_point_y / self.height
        if tr_y > self.perspective_point_y:
            tr_y = self.perspective_point_y 