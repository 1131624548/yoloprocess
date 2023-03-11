import torch
from PIL import Image
from torchvision import transforms


class Recognition_Dataset(object):
    def __init__(self, segment, lbl2id_map, sequence_len, max_ratio, pad=0):
        self.data = segment
        self.lbl2id_map = lbl2id_map
        self.pad = pad  # padding标识符的id，默认0
        self.sequence_len = sequence_len  # 序列长度
        self.max_ratio = max_ratio * 3  # 将宽拉长3倍

        # 定义随机颜色变换
        self.color_trans = transforms.ColorJitter(0.1, 0.1, 0.1)
        # 定义 Normalize
        self.trans_Normalize = transforms.Compose([
            transforms.ToTensor(),
            transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225]),
        ])


    def __getitem__(self, index):
        """
        获取对应index的图像和ground truth label，并视情况进行数据增强
        """
        img_data = self.data[index]
        lbl_str = img_data.label.classification.category  # 图像标签

        # ----------------
        # 图片预处理
        # ----------------
        # load image
        with img_data.open() as fp:
            img = Image.open(fp).convert('RGB')

        # 对图片进行大致等比例的缩放
        # 将高缩放到32，宽大致等比例缩放，但要被32整除
        w, h = img.size
        ratio = round((w / h) * 3)  # 将宽拉长3倍，然后四舍五入
        if ratio == 0:
            ratio = 1
        if ratio > self.max_ratio:
            ratio = self.max_ratio
        h_new = 32
        w_new = h_new * ratio
        img_resize = img.resize((w_new, h_new), Image.BILINEAR)

        # 对图片右半边进行padding，使得宽/高比例固定=self.max_ratio
        img_padd = Image.new('RGB', (32 * self.max_ratio, 32), (0, 0, 0))
        img_padd.paste(img_resize, (0, 0))

        # 随机颜色变换
        img_input = self.color_trans(img_padd)
        # Normalize
        img_input = self.trans_Normalize(img_input)

        # ----------------
        # label处理
        # ----------------

        # 构造encoder的mask
        encode_mask = [1] * ratio + [0] * (self.max_ratio - ratio)
        encode_mask = torch.tensor(encode_mask)
        encode_mask = (encode_mask != 0).unsqueeze(0)

        # 构造ground truth label
        gt = []
        gt.append(1)  # 先添加句子起始符
        for lbl in lbl_str:
            gt.append(self.lbl2id_map[lbl])
        gt.append(2)
        for i in range(len(lbl_str), self.sequence_len):  # 除去起始符终止符，lbl长度为sequence_len，剩下的padding
            gt.append(0)
        # 截断为预设的最大序列长度
        gt = gt[:self.sequence_len]

        # decoder的输入
        decode_in = gt[:-1]
        decode_in = torch.tensor(decode_in)
        # decoder的输出
        decode_out = gt[1:]
        decode_out = torch.tensor(decode_out)
        # decoder的mask
        decode_mask = self.make_std_mask(decode_in, self.pad)
        # 有效tokens数
        ntokens = (decode_out != self.pad).data.sum()

        return img_input, encode_mask, decode_in, decode_out, decode_mask, ntokens


    @staticmethod
    def make_std_mask(tgt, pad):
        """
        Create a mask to hide padding and future words.
        padd 和 future words 均在mask中用0表示
        """
        tgt_mask = (tgt != pad)
        tgt_mask = tgt_mask & Variable(subsequent_mask(tgt.size(-1)).type_as(tgt_mask.data))
        tgt_mask = tgt_mask.squeeze(0)  # subsequent返回值的shape是(1, N, N)
        return tgt_mask


    def __len__(self):

        return len(self.data)
