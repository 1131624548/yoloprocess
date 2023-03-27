import torch
#model = torch.hub.load('facebookresearch/detr:main', 'detr_resnet50', pretrained=True)
pretrained_weights  = torch.load(r'E:\workspace\detr\detr-main\detr-r50-e632da11.pth')

#2类
num_class = 3    #类别数+1，1为背景
pretrained_weights["model"]["class_embed.weight"].resize_(num_class+1, 256)
pretrained_weights["model"]["class_embed.bias"].resize_(num_class+1)
torch.save(pretrained_weights, "detr-r50_%d.pth"%num_class)
