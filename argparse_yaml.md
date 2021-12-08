# argparse使用总结

首先argparse一般写在

```
if __name__ == '__main__':
```

之后，在下方写需要使用的参数；

格式如下：

```python
parse = argparse.ArgumentParser()
parse.add_argument('--num_batches', type=int, default=50, help='the num of batch')
parse.add_argument('--num_window', type=int, default=5, help='the num of window')
parse.add_argument('--weight', type=str, default= '../pretrain.pth', help='the path of pretrained model')
opt = parse.parse_args()
```

parse = argparse.ArgumentParser() 首先创建一个对象，然后用 parse.add_argument方法添加需要的参数值，添加完后用 opt = parse.parse_args()将所有的参数封装在opt内，之后用例如opt.weight就可以调用。



在主函数传入opt参数，即可调用命令行传入的参数值，整个例子如下：

```python
import argparse

def main(opt):
    print(opt.num_batches)

if __name__ == '__main__':

    parse = argparse.ArgumentParser()
    parse.add_argument('--num_batches', type=int, default=50, help='the num of batch')
    parse.add_argument('--num_window', type=int, default=5, help='the num of window')
    parse.add_argument('--weight', type=str, default= '../pretrain.pth', help='the path of pretrained model')
    
    opt = parse.parse_args()
    main(opt)
```
****
# Yaml使用总结
yaml文件通常也是用于保存参数，在主函数中用来调用，yaml文件是一个层级结构，以字典形式调用
yaml文件结构如下：
```
device: 'cpu'

data:
    train_path: 'data/train'
    test_path: 'test/train'
    num: 1000
```
特别需要注意缩进使用空格而不是tab，并且层级之间一定要对齐。

## 读取yaml文件
在读取yaml文件时，先将yaml文件里面的内容全部用系统函数读入，然后用yaml.safe_load进行加载，转换成一个字典，返回字典供后续使用。读取代码如下：
```python
def read_yaml(path):
    file = open(path, 'r', encoding='utf-8')
    string = file.read()
    dict = yaml.safe_load(string)

    return dict
```

调用的时候就根据yaml文件里面的结构层次按键值对进行调用：

```python
path = 'config.yaml'
Dict = read_yaml(path)
device = Dict['device']
print(device)

train_path = Dict['data']['train_path']
print(train_path)
```

完整测试代码如下：
```python
import yaml

def read_yaml(path):
    file = open(path, 'r', encoding='utf-8')
    string = file.read()
    dict = yaml.safe_load(string)

    return dict
path = 'config.yaml'
Dict = read_yaml(path)
device = Dict['device']
print(device)

train_path = Dict['data']['train_path']
print(train_path)
```



# yaml与argparse混合使用

看过很多paper的代码，两者基本都是混合使用的，yaml首先可以将全部参数都设置一个默认值，比如网络的层数，激活函数用哪个等等，大多是模型内相关的参数以及train和test使用的数据的地址。

argparse通常设置几个train和test时经常更改的参数，比如训练的epoch，batch_size，learning_rate...

argparse接收的是命令行的输入，所以优先级应该是会高一些；假如argparse和yaml文件中都有相同的参数，如果命令行指定了参数，那么代码运行时使用的参数是命令行输入的参数。