# ISP图像处理过程

# 0. ISP Pipline

ISP的处理过程主要为以下步骤，但是并不一定会包含所有的步骤，并且顺序也有所差别.

<img src="C:\Users\Yang_Yuhang\AppData\Roaming\Typora\typora-user-images\image-20211217093409408.png" alt="image-20211217093409408" style="zoom:67%;" />

<center style="color:#C0C0C0;text-decoration:underline">ISP pipline</center>

# 1. BLC(Black Level Correction)

**产生原因：**

暗电流，也称无照电流，指在没有光照射的状态下,在太阳电池、光敏二极管、光导电元件、光电管等的受光元件中流动的电流，一般由于载流子的扩散或者器件内部缺陷造成。目前常用的CMOS就是光电器件，所以也会有暗电流，导致光照为0的时候也有电压输出。

1. sensor到ISP会有一个AD转换的过程，而AD芯片都会有一个灵敏度，当电压低于这个阈值的时候无法进行AD转换，所以就人为添加一个常量使得原本低于阈值的这部分值也能被AD转换；

2. 因为人眼对暗部细节更加敏感，而对高亮区没那么敏感，所以就增加一个常量牺牲人眼不敏感的亮区来保留更大暗区细节。

   ![img](https://pic1.zhimg.com/80/v2-6ef7a2722e9568c50d94e7250aae827c_720w.jpg)

也就是经过AD之后，直线AB被移动到了A'B',BC高亮部分的信息丢失了。

**BL校正：**

一般分为sensor端和ISP端两个部分，目前大部分都在sensor端作了处理，在ISP端只用减去相应的值就行了，具体做法如下：

<img src="https://pic2.zhimg.com/80/v2-2b3b4c460f4dea4c569da0f3da7ad909_720w.jpg" alt="img" style="zoom:50%;" />

我们得到了一张RAW图(RGGB)格式，将RAW图按channel分开为Gr，Gb，R，B，将四个通道求平均值m，再对每个像素点减去m值；减去m值后会发现现在的最大像素值已经不是255了，所以需要一点处理，通道R和B会在白平衡阶段处理，而Gr和Gb通道会做一个归一化处理，假设减去m值之后的值为Gr和Gb通道的值为X，那么最终G的值为：
$$
G=X* \frac{255}{255-{\theta}}
$$
$\theta$就是AD过程中加的那个常量，目的是为了减去m后能让G通道的值在0-255之间，作为这些操作后再加分成的四个channel按位置拼接回原图，BLC就完成了。

**代码参考：**

```c++
data = readRaw(filePath, bits, row, col);

R = data(1:2:end, 1:2:end);
Gr = data(1:2:end, 2:2:end);
Gb = data(2:2:end, 1:2:end);
B = data(2:2:end, 2:2:end);

R_mean = round(mean(mean(R)));
Gr_mean = round(mean(mean(Gr)));
Gb_mean = round(mean(mean(Gb)));
B_mean = round(mean(mean(B)));

cR = R-R_mean;
cGr = Gr-Gr_mean;
cGb = Gb-Gb_mean;
cB = B-B_mean;

cData = zeros(size(data));
cData(1:2:end, 1:2:end) = cR(1:1:end, 1:1:end);
cData(1:2:end, 2:2:end) = cGr(1:1:end, 1:1:end);
cData(2:2:end, 1:2:end) = cGb(1:1:end, 1:1:end);
cData(2:2:end, 2:2:end) = cB(1:1:end, 1:1:end);
```

------

# 2. LSC(Lens Shading Correction)

**产生原因：**

Luma shading的主要原因是镜头中心到边缘的能量衰减导致的，如图所示，蓝色和绿色用相同的数量线条表示能量，中心位置的蓝色几乎所有能量都能达到最右侧的的成像单元，但是边缘的绿色由于有一定角度射入，经过镜头的折射，有一部分光（最上方的几条绿色线条）就没法达到成像单元，因此成像单元中心的能量就会比边缘的大，变现在亮度上就是亮度向边缘衰减变暗(导致Senor捕获的图像中间亮度高，周围边缘亮度低)。

![img](https://pic1.zhimg.com/80/v2-0fd37340e8b7d1a8d07bcc97b56a7ff4_720w.jpg)

**矫正方法：**

产生Luma shading的本质是能量的衰减，从而导致了像素值的变化，所以矫正就是对该像素点乘以一个gain值，使其恢复到衰减前的状态即可，LSC校正的本质就是找到合适的gain值.

**Mesh shading correct**:

对于一张图片，将其分成n×n的网格如下：

<img src="https://pic3.zhimg.com/80/v2-3c2a2ace32454574ef1707d31c6f95ce_720w.jpg" alt="img" style="zoom:50%;" />

然后针对网格顶点求出矫正的增益，然后把这些顶点的增益储存到内存中，在LSC时根据pixel的位置就能找到相应的增益gain值，然后用pixel的值与增益值相乘就可得到结果；但是，如果存储整张图像每个pixel的增益对内存消耗太大，所以通常只存储网格顶点的增益值，其余pixel的增益值就通过双线性插值来求出.

对于上图，分成网格后求出的亮度分布如下：

![image-20211216165222354](C:\Users\Yang_Yuhang\AppData\Roaming\Typora\typora-user-images\image-20211216165222354.png)

<center style="color:#C0C0C0;text-decoration:underline">亮度分布图</center>

针对网格亮度求出的增益就应该和亮度分布相反，如下图：

<img src="C:\Users\Yang_Yuhang\AppData\Roaming\Typora\typora-user-images\image-20211216165343266.png" alt="image-20211216165343266" style="zoom: 33%;" />

<center style="color:#C0C0C0;text-decoration:underline">亮度增益分布图</center>

# 3. DPC(Defective Pixel Correction)

**产生原因：**

图像传感器上光线采集点(像素点)所形成的阵列存在工艺上的缺陷，或光信号进行转化为电信号的过程中出现错误，从而会造成图像上像素信息错误，导致图像中的像素值不准确，这些有缺陷的像素即为图像坏点，sensor在长时间、高温环境下坏点也会越来越多，从而破坏了图像的清晰度和完整性.

**坏点分类：**

(1)静态坏点：

静态亮点：一般来说像素点的亮度值是正比于入射光的，而亮点的亮度值明显大于入射光乘以相应比例，并且随着曝光时间的增加，该点的亮度会显著增加；

静态暗点：无论在什么入射光下，该点的值接近于0;

(2)动态坏点：在一定像素范围内，该点表现正常，而超过这一范围，该点表现的比周围像素要亮，与sensor 温度、增益有关，sensor 温度升高或者gain 值增大时，动态坏点会变的更加明显；

**坏点对图像的影响：**

(1) 如果图像中存在坏点，后续进行插值和滤波处理的时候，会影响到周围的像素值;
(2) 会造成图像的边缘出现伪彩色的情况，不仅影响清晰度，还影响边缘的色彩;
(3) 会造成图像部分像素闪烁的现象;

**坏点矫正：**

坏点矫正又分为静态坏点消除和动态坏点消除，两种方法的流程如下图：

![image-20211217095711044](C:\Users\Yang_Yuhang\AppData\Roaming\Typora\typora-user-images\image-20211217095711044.png)

(1)静态坏点消除：生产厂商在sensor出厂时就标定好坏点的位置，并存在表里，后续根据表里的位置进行坏点矫正，但这种方法不太适用，一是内存问题，第二是sensor在使用时由于温度等环境因素的影响还会产生其他的坏点，这些坏点并没有在表里标注，也就无法矫正；

(2)动态坏点消除：分为坏点检测和坏点矫正两个步骤

![image-20211217100602310](C:\Users\Yang_Yuhang\AppData\Roaming\Typora\typora-user-images\image-20211217100602310.png)

坏点检测：

在raw图的格式下，每个通道的每个pixel与其相邻的8个pixel计算差值，判断这8个差值是正值还是负值，如果有的为正有的为负则为正常值；设置一个阈值，如果这8个差值都大于了该阈值，则为坏点；

坏点矫正：

检测到的坏点的pixel就用相邻的8个pixel的中值进行替代；

# 4. Denoise

**噪声的分类和产生原因**

(1) 固定模式噪声（FPN），由于图像传感器的空间不均匀性引起的，硅片本身的瑕疵，失效像素（坏点），像素参数的随机分布，均可构成固定模式噪声;

(2) 随机噪声，由于电子的随机热运动、光信号的统计涨落等多种原因引起的噪声，在芯片中普遍存在的1/f噪声也是一种随机噪声；

(3) 条带噪声（Banding），有水平条带和垂直条带两种表现形式，有固定模式和随机模式两种来源，其中固定模式来源包括传感器中各晶体管工作参数相对理论值的漂移；垂直条带往往是由于传感器中存在两个ADC器件，其参数不完全一致；随机模式往往由于电源纹波引起的；

![preview](https://pic4.zhimg.com/v2-7dfe883ad771c661f3fd93ca9960087f_r.jpg)

<center style="color:#C0C0C0;text-decoration:underline">三种不同噪声示意图</center>

**去噪算法**：

去噪的本质就是滤波，去噪的算法非常多，一般能用在RGB域下的方法都能用在Bayer域，只不过Bayer域需要把不同channel分开处理；

常见的去噪算法分类：

**空域算法**：均值滤波、中值滤波、高斯滤波、双边滤波、NLM；

**变换域算法：**

频域：低通滤波、高通滤波、带通滤波

Wavelet：基于小波系数阈值、基于系数相关性等

DCT(离散余弦)变换等

**时域算法：**常规算法结合多帧匹配，前景和背景判断、动静判决；

**结合算法：**类似BM3D去噪算，空域和Wavelet的结合

# 5. Demosaic

平时看到的图像大多是RGB的，但sensor端输出的其实是bayer格式，将raw图进行去马赛克之后才能得到RGB的图像：

<img src="https://pic4.zhimg.com/80/v2-e35e383b9118fb4fd7872443888a715b_720w.jpg" alt="img" style="zoom:67%;" />

去马赛克的过程就是将R、G、B三个通道先分别抽出，对每个pixel恢复出另外两个channel的值，然后拼接在一起成为RGB的图像；

demosaic的算法有很多，传统的方法是基于插值，有直接根据像素值来进行插值恢复pixel值的，也有根据色差原理来进行插值，通常是先恢复出G通道的R和B，然后根据色差原理进行插值恢复出R和B通道其他的channel值.

近几年也有基于Learning的方法做去马赛克的，参考如下：

[[1] End-to-End Learning for Joint Image Demosaicing, Denoising and Super-Resolution](https://openaccess.thecvf.com/content/CVPR2021/html/Xing_End-to-End_Learning_for_Joint_Image_Demosaicing_Denoising_and_Super-Resolution_CVPR_2021_paper.html)

[[2] Joint Demosaicing and Denoising with Self Guidance](https://openaccess.thecvf.com/content_CVPR_2020/html/Liu_Joint_Demosaicing_and_Denoising_With_Self_Guidance_CVPR_2020_paper.html)

[[3] Learning Deep Convolutional Networks for Demosaicing](https://arxiv.org/abs/1802.03769)

[[4] Deep Joint Demosaicking and Denoising](https://dl.acm.org/doi/abs/10.1145/2980179.2982399)

[[5] Replacing Mobile Camera ISP with a Single Deep Learning Model](https://openaccess.thecvf.com/content_CVPRW_2020/html/w31/Ignatov_Replacing_Mobile_Camera_ISP_With_a_Single_Deep_Learning_Model_CVPRW_2020_paper.html)

# 6. AWB(Auto White Balance)

**产生原因：**

人类视觉系统具有颜色恒常性特点，人类对物体观察不受光源影响。但是Sensor在不同光线下，物体呈现的颜色不同，在晴朗天空下会偏蓝，在烛光下会偏红。为了消除光源对于图像传感器成像的影响，模拟人类视觉系统的颜色恒常性，保证在任何场景下看到的白色是真正的白色。

白平衡处理的目的是通过改变图像的各个色彩通道的增益，对色温环境所造成的颜色偏差和拍摄一起本身所固有的色彩通道增益的偏差进行统一补偿，从而让获得的图像能正确反映物体的真实色彩。

![img](https://img2020.cnblogs.com/blog/1259754/202009/1259754-20200912105215256-1808208051.png)

<center style="color:#C0C0C0;text-decoration:underline">不同光源下sensor产生的图像</center>

**矫正算法：**

矫正算法的目的主要计算增益值gain，然后将原像素乘以gain值得到矫正后的值

(1) 灰度世界法

灰度世界假设：如果一张图片里面的颜色非常丰富，那么该图像中的每个channel的平均值应该是相等的，$R_{mean} = B_{mean} = G_{mean}$，所以矫正的时候就用R和B通道的pixel值乘上G通道的mean与该通道的mean(即gain值)，G通道不用作该操作而是被当作参考是因为G通道在BLC的时候就已经进行了归一化，gain值计算公式如下：
$$
R_{gain}=\frac{G_{mean}}{R_{mean}}, B_{gain}=\frac{G_{mean}}{B_{mean}}
$$
之后R通道和B通道的每个pixel直接乘以$R_{gain},B_{gain}$.

(2) 完全反射法(也叫最大亮点法)

完全反射也是基于一个假说：基于这样一种假设，一幅图像中最亮的像素相当于物体有光泽或镜面上的点，它传达了很多关于场景照明条件的信息。如果景物中有纯白的部分，那么就可以直接从这些像素中提取出光源信息。因为镜面或有光泽的平面本身不吸收光线，所以其反射的颜色即为光源的真实颜色，这是因为镜面或有光泽的平面的反射比函数在很长的一段波长范围内是保持不变的。完美反射法就是利用用这种特性来对图像进行调整。

进行矫正的时候先找出每个channel的pixel值最大的那个点记录为$R_{max},B_{max},G_{max}$,然后找出整张图中pixel最大的值，其实就是$I_{max} = max(R_{max},B_{max},G_{max})$，之后再分别计算每个channel的gain值，公式如下：
$$
R_{gain} = I_{max}/R_{max}
$$
其他连个通道方法类似.然后每个通道的pixel乘以对应的gain值，以R通道为例：
$$
R^，=\begin{cases}
R*R_{gain}, & \text{if} & R*R_{gain} < 255; \\
255, &\text{if} & R*R_{gain}>=255;

\end{cases}
$$
