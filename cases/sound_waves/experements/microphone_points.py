import numpy as np

class Microphone:
    def __init__(self,matrix = np.random.rand(120,120)):
        self.matrix = matrix
    def array(self):
        arrs =[
            [[self.matrix[0, -1], self.matrix[120 // 2, -1], self.matrix[-1, -1]]],
            [[self.matrix[0, 120 // 2], self.matrix[0, 3 * 120 // 4], self.matrix[0, -1], self.matrix[3 * 120 // 4, -1], self.matrix[120 // 2, -1], self.matrix[120 // 4, -1], self.matrix[-1, -1],
             self.matrix[-1, 3 * 120 // 4], self.matrix[-1, 120 // 2]]],
            [self.matrix[0, 60:-1],self.matrix[:,-1],self.matrix[-1,(120 // 2):-1]],
            [self.matrix[0, 60:-1],self.matrix[:,-1],self.matrix[-1,(120 // 2):-1],self.matrix[11:109,55],self.matrix[109,55:109],self.matrix[11:109,109],self.matrix[10,55:109]]
            ]
        return arrs
    coords = {'points': [
        #[[120, 120 // 2]],
        [[120, 120], [120, 120 // 2], [120, 0]],
       # [[120 // 2, 120], [120, 120], [120, 120 // 2], [120, 0], [120 // 2, 0]],
       # [[120 // 2, 120], [120, 120], [120, 3 * 120 // 4], [120, 120 // 2], [120, 120 // 4], [120, 0], [120 // 2, 0]],
        [[120 // 2, 120], [3 * 120 // 4, 120], [120, 120], [120, 3 * 120 // 4], [120, 120 // 2], [120, 120 // 4],
         [120, 0], [3 * 120 // 4, 0], [120 // 2, 0]],
        [[60, 119], [119, 119],[119,1],[60,1]],
        [[110, 110],[110 ,10],[55,10],[55, 110], [110, 110]],
    ]
    }

# m = Microphone(matrix = np.random.rand(120,120))
# a =m.array()
# lenght = sum([len(i) for i in a[1]])
# cnte = np.concatenate(a[3])
# #ss = [np.concatenate(a[3]) for i in a[3]]
# print(sum([sum(i) for i in a[3]]))
# # print()