import torch
import numpy as np

def IOU(box,other_boxes):
    #box: [x1,y1,x2,y2] 分别表示方框的左上角的点和右下角的点
    #other_boxs: N个box，多了一个维度(代表box的数量)

    box_area = (box[2]-box[0])*(box[3]-box[1])
    other_boxes_area = (other_boxes[:,2]-other_boxes[:,0]) * (other_boxes[:,3]-other_boxes[:,1])

    #交集
    x1 = torch.max(box[0],other_boxes[:,0])
    y1 = torch.max(box[1],other_boxes[:,1])
    x2 = torch.min(box[2],other_boxes[:,2])
    y2 = torch.min(box[3],other_boxes[:,3])
    Min = torch.tensor([0])
    w,h = torch.max(Min,x2-x1),torch.max(Min,y2-y1) #考虑有没相交的框

    #交集面积
    overlap_area = w*h

    iou = overlap_area / (box_area+other_boxes_area-overlap_area)

    return iou

# box = torch.tensor([1,1,10,10])
# boxes = torch.tensor([
#     [1,1,11,11],
#     [4,4,6,6]
# ])

# iou = IOU(box,boxes)
# print(iou)

def NMS(boxes, C = 0.5):
    #boxes：包含了每一类的置信度，这里以一个类作为示例，每个boxes的数据 [单个类别置信度, x1, y1, x2, y2]

    #首先对输入的boxes按照类别置信度排序筛选出置信度最高的box作为参考
    sort_boxes = boxes[boxes[:,0].argsort(descending=True)]
    keep = []

    while len(sort_boxes)>0:
        ref_box = sort_boxes[0]
        keep.append(ref_box)
        if len(sort_boxes) > 1:
            other_boxes = sort_boxes[1:] #去除掉参考的那个box
            #注意这里的box和上面的IOU函数里面的box相比多了一个置信度，所以要取[1:]
            sort_boxes = other_boxes[torch.where(IOU(ref_box[1:], other_boxes[:,1:])<C)] 
        else:
            break
    return torch.stack(keep)

boxes = torch.tensor([
    [0.8, 1, 1, 10, 10],
    [0.2, 1, 1, 11, 11],
    [0.3, 4, 4, 6, 6]
])

NMS_boxes = NMS(boxes,C = 0.5)
print(NMS_boxes)