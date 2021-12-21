# Deep Learning激活函数总结

## 1. Sigmoid函数

**函数图像：**

<img src="https://pic2.zhimg.com/v2-8d9c99a123ba8cb2629106660e8bf6d5_b.jpg" alt="img" style="zoom:67%;" />

**函数表达式：**
$$
f(x) = \frac{1}{1+e^{-x}}
$$
**Sigmoid函数的导数为：**
$$
f^‘(x) = f(x)*(1-f(x))
$$
**Sigmoid函数的适用场景：**

- Sigmoid 函数的输出范围是 0 到 1，由于输出值限定在 0 到 1，因此它对每个神经元的输出进行了归一化；
- 用于将预测概率作为输出的模型，由于概率的取值范围是 0 到 1，因此 Sigmoid 函数非常合适；
- 梯度平滑，避免跳跃的输出值；
- 分类问题，尤其是二分类问题，一般用于输出层，即最后一个全连接layer;

**Sigmoid函数的缺点：**

- 在函数值接近0和1的时候，会倾向于梯度消失；
- 函数输出不是以 0 为中心的，这会降低权重更新的效率；
- Sigmoid 函数执行指数运算，计算机运行得较慢；

## 2. Tanh函数

**函数图像：**

![img](https://pic1.zhimg.com/v2-3b8753a9956a673554d5e992c398f334_b.jpg)

**函数表达式：**
$$
Tanh(x) = \frac{2}{1-e^{-2x}}-1
$$
**Tanh函数与Sigmoid函数对比：**

Tanh和Sigmoid在函数图像上类似，但Tanh函数是以0为中心，而sigmoid是以0.5为中心，如下图所示：

![img](https://pic3.zhimg.com/v2-d04be8777f2eeba6321d90d9d3106d8e_b.jpg)

<center style="color:#C0C0C0;text-decoration:underline">Tanh和Sigmoid对比图</center>

Tanh存在着一个与Sigmoid相似的问题，在输入较大或者较小的时候，输出几乎是平滑的，梯度约等于0.不利于权重更新，但Tanh的输出间隔为1，比sigmoid大，负输入将被强映射为负，而零输入被映射为接近零，并且Tanh一般用于hidden layer(隐藏层)。

## 3. Relu函数

**函数图像：**

![img](https://pic1.zhimg.com/v2-30c8465016babfc2e6440c43aee81528_b.jpg)

**函数表达式：**
$$
Relu(x)=\begin{cases}
max(0,x), & \text{if} & x>=0; \\
0, &\text{if} & x<0;

\end{cases}
$$
Relu函数是非常常用的一种激活函数，它相对于Sigmoid和Tanh函数来说有以下优点：

- 不存在梯度消失的问题，Relu的梯度恒为一个常数，只要输入为正，在权重更新时都会有稳定的梯度；
- Relu里面只存在线性的计算，开销相比于sigmoid和tanh的指数要更小，计算速度更快；

但Relu函数也存在一些弊端：

- Dead ReLU 问题，当输入为负时，ReLU 完全失效，在正向传播过程中，这不是问题。有些区域很敏感，有些则不敏感。但是在反向传播过程中，如果输入负数，则梯度将完全为零，会丢失掉一部分信息，sigmoid 函数和 tanh 函数也具有相同的问题；
- ReLU 函数的输出为 0 或正数，这意味着 ReLU 函数不是以 0 为中心的函数。

## 4. Leaky Relu函数

为了解决Relu函数的Dead Relu问题，提出了Leaky Relu函数，是Relu函数的一种变体，两者的函数对比图如下：

![img](https://pic2.zhimg.com/v2-4d592b88fe164d0ca1fdd42a79f8b4a1_b.jpg)

<center style="color:#C0C0C0;text-decoration:underline">ReLU(左)，Leaky ReLU(右)</center>

**函数表达式：**
$$
LeakyRelu(x)=\begin{cases}
max(0,x), & \text{if} & x>=0; \\
\alpha x, &\text{if} & x<0;

\end{cases}
$$
$\alpha$通常为0.01，是一个很小的线性分量，来调整输入为负时的梯度为0的问题，从理论上来说Leaky ReLU函数具有ReLU的所有优点，并且能解决ReLU函数在输入为负时的零梯度问题，应该是比ReLU函数更好；但在实际实验中，使用Leaky ReLU的效果不一定比使用ReLU好，要根据实际实验结果选取.

## 5. ELU函数

**函数图像：**

<img src="https://pic4.zhimg.com/v2-061d9ad03c55dae92d564d452c2b22b3_b.jpg" alt="img" style="zoom:150%;" />

**函数表达式：**
$$
ELU(x)=\begin{cases}
max(0,x), & \text{if} & x>=0; \\
\alpha (e^x -1), &\text{if} & x<0;

\end{cases}
$$
ELU的思路和Leaky ReLU相似，都是为了解决ReLU函数的输入为负时梯度为0的问题，相对于前两者，ELU特性有一下几点：

- ELU 通过减少偏置偏移的影响，使正常梯度更接近于单位自然梯度，从而使均值向零加速学习；
- ELU 在较小的输入下会饱和至负值，从而减少前向传播的变异和信息；

## 6. Softmax函数

Softmax是用于多分类任务的激活函数，对于长度为 K 的任意实向量，Softmax 可以将其压缩为长度为 K，值在（0，1）范围内，并且向量中元素的总和为 1 的实向量，Softmax函数表达式如下：

![img](https://pic1.zhimg.com/v2-5179c5ba640ab588c917de55b7f704a8_b.jpg)

Softmax 函数的分母结合了原始输出值的所有因子，这意味着 Softmax 函数获得的各种概率彼此相关，并且根据函数表达式，softmax会使得Output值大的layer概率更大，值小的layer计算出的概率更小，但又不会直接丢弃，非常适合多分类任务，一般与交叉熵损失函数一起使用.

Softmax的缺点：

- 在零点不可微；
- 负输入的梯度为零，这意味着对于该区域的激活，权重不会在反向传播期间更新，因此会产生永不激活的死亡神经元；

## 7.GELU函数

GELU函数通常用于Transformer模型中，它其实就是高斯误差线性单元，它在激活中加入了随机正则的思想；可以理解为，对于输入的值，希望根据情况为它乘上1或者0，随着x的值越来越小，它被归为0的概率就越来越高，对于ReLU来说，就是当输入小于0时就将其乘0，而对与GELU，具体来说可以表示为$\Phi(x)*x+(1-\Phi(x))*0=x*\Phi(x)$,也就是说对于伯努利分布$\Phi(x)$的一部分，直接乘以输入x，而另一部分$1-\Phi(x)$则直接归0，于是GELU可以写为如下表达式：
$$
GELU(x)=xP(X\leq x) = x\Phi(x)
$$
$\Phi(x)$指的是x的高斯正态分布的累积分布，计算公式如下：
$$
xP(X\leq x)=x\int_{-\infty}^{x}\frac{e^{-\frac{(x-u)^2}{2\sigma^2}}}{\sqrt{2\pi}\sigma}dX
$$
最终计算的逼近结果为:
$$
GELU(x)=0.5x(1+tanh(\sqrt{2/\pi}(x+0.044715x^3)))
$$
**函数图像如下：**

<img src="https://pic4.zhimg.com/v2-149a8bc6ee90f65205a8d408f79a0017_b.jpg" alt="img" style="zoom:67%;" />

可以看出，当 x 大于 0 时，输出为 x；但 x=0 到 x=1 的区间除外，这时曲线更偏向于 y 轴.

GELU函数的导数图像：

![img](https://pic1.zhimg.com/v2-06d94b711445480094eca59b8ec51804_b.jpg)

<center style="color:#C0C0C0;text-decoration:underline">GELU导数图像</center>

该函数在Transformer中表现较好，并且能够避免梯度消失问题.