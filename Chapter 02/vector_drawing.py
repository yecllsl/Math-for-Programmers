from math import sqrt, pi, ceil, floor
import matplotlib
import matplotlib.patches
from matplotlib.collections import PatchCollection


import numpy as np
import matplotlib.pyplot as plt
from matplotlib.pyplot import xlim, ylim

blue = 'C0'
black = 'k'
red = 'C3'
green = 'C2'
purple = 'C4'
orange = 'C2'
gray = 'gray'

class Polygon():
    def __init__(self, *vertices, color=blue, fill=None, alpha=0.4):
        self.vertices = vertices
        self.color = color
        self.fill = fill
        self.alpha = alpha

class Points():
    def __init__(self, *vectors, color=black):
        self.vectors = list(vectors)
        self.color = color

class Arrow():
    def __init__(self, tip, tail=(0,0), color=red):
        self.tip = tip
        self.tail = tail
        self.color = color

class Segment():
    def __init__(self, start_point, end_point, color=blue):
        self.start_point = start_point
        self.end_point = end_point
        self.color = color

# helper function to extract all the vectors from a list of objects
def extract_vectors(objects):
    for object in objects:
        if type(object) == Polygon:
            for v in object.vertices:
                yield v
        elif type(object) == Points:
            for v in object.vectors:
                yield v
        elif type(object) == Arrow:
            yield object.tip
            yield object.tail
        elif type(object) == Segment:
            yield object.start_point
            yield object.end_point
        else:
            raise TypeError("Unrecognized object: {}".format(object))
'''
 这段代码定义了一个名为`draw`的函数，用于在Matplotlib库中绘制图形。它接受任意数量的参数，这些参数可以是对象、选项和参数。下面是`draw`函数的参数说明：

1. `*objects`：这是函数接受的所有参数的列表。这些参数可以是任意类型的对象，例如Polygon、Points、Arrow或Segment。
2. `origin=True`：这个选项表示是否在坐标系中显示原点。默认情况下，它是可见的。
3. `axes=True`：这个选项表示是否在坐标系中显示坐标轴。默认情况下，它是可见的。
4. `grid=(1,1)`：这个选项表示坐标轴的刻度。它是一个元组，表示x轴和y轴的刻度。默认情况下，它们都是1。
5. `nice_aspect_ratio=True`：这个选项表示是否使用一个漂亮的纵横比来调整图像大小。默认情况下，它是可见的。
6. `width=6`：这个选项表示图像的宽度。默认情况下，它是6英寸。
7. `save_as=None`：这个选项表示是否将图像保存到文件。如果设置了`save_as`参数，函数将在绘制图形后保存图像。默认情况下，它是不可见的。

函数的主要逻辑如下：

1. 首先，它从参数列表中提取所有可能的向量对象。
2. 然后，它计算所有向量的x和y坐标的最小和最大值，以便稍后设置坐标轴的范围。
3. 如果设置了`grid`选项，它计算x轴和y轴的刻度值，并将它们添加到坐标轴的范围中。
4. 如果设置了`origin`选项，它会在坐标轴中绘制原点。
5. 如果设置了`axes`选项，它会在坐标轴中绘制坐标轴。
6. 它遍历参数列表中的所有对象，并根据它们的类型进行不同的绘制。对于Polygon对象，它会绘制一个多边形。对于Points对象，它会绘制一组点。对于Arrow对象，它会绘制一个箭头。对于Segment对象，它会绘制一个线段。
7. 如果设置了`nice_aspect_ratio`选项，它会根据坐标轴的范围调整图像的大小，使其具有漂亮的纵横比。
8. 如果设置了`save_as`参数，它会将图像保存到指定的文件中。
9. 最后，它显示绘制好的图形。

总之，这段代码定义了一个函数，用于在Matplotlib库中绘制图形，支持各种类型的对象，如多边形、点、箭头和线段。它可以调整坐标轴的范围、大小和显示，以便使图形更加美观。
'''
def draw(*objects, origin=True, axes=True, grid=(1,1), nice_aspect_ratio=True,
            width=6, save_as=None):

    all_vectors = list(extract_vectors(objects))
    xs, ys = zip(*all_vectors)

    max_x, max_y, min_x, min_y = max(0,*xs), max(0,*ys), min(0,*xs), min(0,*ys)

    #sizing
    if grid:
        x_padding = max(ceil(0.05*(max_x-min_x)), grid[0])
        y_padding = max(ceil(0.05*(max_y-min_y)), grid[1])

        def round_up_to_multiple(val,size):
            return floor((val + size) / size) * size

        def round_down_to_multiple(val,size):
            return -floor((-val - size) / size) * size

        plt.xlim(floor((min_x - x_padding) / grid[0]) * grid[0],
                ceil((max_x + x_padding) / grid[0]) * grid[0])
        plt.ylim(floor((min_y - y_padding) / grid[1]) * grid[1],
                ceil((max_y + y_padding) / grid[1]) * grid[1])

    if origin:
        plt.scatter([0],[0], color='k', marker='x')

    if grid:
        plt.gca().set_xticks(np.arange(plt.xlim()[0],plt.xlim()[1],grid[0]))
        plt.gca().set_yticks(np.arange(plt.ylim()[0],plt.ylim()[1],grid[1]))
        plt.grid(True)
        plt.gca().set_axisbelow(True)

    if axes:
        plt.gca().axhline(linewidth=2, color='k')
        plt.gca().axvline(linewidth=2, color='k')

    for object in objects:
        if type(object) == Polygon:
            for i in range(0,len(object.vertices)):
                x1, y1 = object.vertices[i]
                x2, y2 = object.vertices[(i+1)%len(object.vertices)]
                plt.plot([x1,x2],[y1,y2], color=object.color)
            if object.fill:
                xs = [v[0] for v in object.vertices]
                ys = [v[1] for v in object.vertices]
                plt.gca().fill(xs,ys,object.fill,alpha=object.alpha)
        elif type(object) == Points:
            xs = [v[0] for v in object.vectors]
            ys = [v[1] for v in object.vectors]
            plt.scatter(xs,ys,color=object.color)
        elif type(object) == Arrow:
            tip, tail = object.tip, object.tail
            tip_length = (xlim()[1] - xlim()[0]) / 20.
            length = sqrt((tip[1]-tail[1])**2 + (tip[0]-tail[0])**2)
            new_length = length - tip_length
            new_y = (tip[1] - tail[1]) * (new_length / length)
            new_x = (tip[0] - tail[0]) * (new_length / length)
            plt.gca().arrow(tail[0], tail[1], new_x, new_y,
            head_width=tip_length/1.5, head_length=tip_length,
            fc=object.color, ec=object.color)
        elif type(object) == Segment:
            x1, y1 = object.start_point
            x2, y2 = object.end_point
            plt.plot([x1,x2],[y1,y2], color=object.color)
        else:
            raise TypeError("Unrecognized object: {}".format(object))

    fig = matplotlib.pyplot.gcf()

    if nice_aspect_ratio:
        coords_height = (ylim()[1] - ylim()[0])
        coords_width = (xlim()[1] - xlim()[0])
        fig.set_size_inches(width , width * coords_height / coords_width)

    if save_as:
        plt.savefig(save_as)

    plt.show()
