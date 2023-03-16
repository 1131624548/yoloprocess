
 # Descripttion:***
 # version: 1.0 
 # Author: xiaoxuesheng
 # Date: 2023-**-** **:**:**
# LastEditors:  *****
# LastEditTime: *****
# -*- coding: utf-8 -*-
import paddle
import paddle.nn as nn 

class ResNet(nn.layer):
    def __init__(self,in_dim=64,num_classes=10):
        super().__init__()
        # stem layer
        self.conv1= nn.Conv2D(in_channels=3,out_channels=in_dim,kernel_size=3,stride=1,padding=1,bias_attr=False)
        self.bn1=nn.BatchNorm2D(in_dim)
        self.relu=nn.ReLU()
        # block
        self.layer1 = self._make_layer(dim=64,n_blocks=2,stride=1)
        self.layer2 = self._make_layer(dim=64,n_blocks=2,stride=2)
        self.layer3 = self._make_layer(dim=64,n_blocks=2,stride=2)
        self.layer4 = self._make_layer(dim=64,n_blocks=2,stride=2)

        # head layer
        self.avgpool=nn.AdaptiveAvgPool2D(1)
        self.classifier = nn.Linear(512,num_classes)
    def forward(self,x):
        x =self.conv1(x)
        x =self.bn1(x)
        x =self.relu(x)
        x =self.layer1(x)
        x =self.layer2(x)
        x =self.layer3(x)
        x =self.layer4(x)
        x =self.avgpool(x)
        x = x.flatten(1)
        x =self.classifier(x)
        return x

def main():
    t=paddle.randn([4,3,32,32])
    model= ResNet
