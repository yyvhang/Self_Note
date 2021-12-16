
import torch
import numpy as np
import torch.nn as nn

input = np.array([
    [1,2],
    [2,3],
    [3,4]
]).astype(np.float32)

torch_bn = nn.BatchNorm1d(2)
torch_data = torch.from_numpy(input)
torch_bn_out = torch_bn(torch_data)
print(torch_bn_out)

class My_bn:
    def __init__(self, monentum, eps, num_features):
        super().__init__()

        self.monentum = monentum
        self.eps = eps

        self.running_mean = 0
        self.running_var = 1
        self.gamma = np.ones(shape=(num_features, ))
        self.beta = np.zeros(shape=(num_features, ))

    def batch_norm(self, x):
        x_mean = x.mean(axis = 0)
        x_var = x.var(axis = 0)

        self.running_mean = self.monentum * self.running_mean + (1-self.monentum) * x_mean
        self.running_var = self.monentum * self.running_var + (1-self.monentum) * x_var

        y = (x - x_mean)/np.sqrt(x_var+self.eps)
        out = self.gamma*y + self.beta

        return out

model = My_bn(monentum=0.01, eps=0.0001, num_features=2)
My_bn._beta = torch_bn.bias.detach().numpy()
My_bn._gamma = torch_bn.weight.detach().numpy()
self_out = model.batch_norm(input)
print(self_out)