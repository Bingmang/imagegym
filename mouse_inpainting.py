"""
可视化用opencv的impaint函数修复图像
usage: python mouse_inpainting.py
"""

import cv2
import numpy as np
from skimage import measure


class MouseInpainting:
    '鼠标移动绘制mask图像修复, 左键绘制mask，按m会隔两列置0，右键修复图像，按q退出'
    name = 'MouseInpaiting'
    drawing = False
    mask = None
    org_img = None
    tmp_img = None
    dst_img = None
    pen_size = 5
    inpaint_radius = 2
    inpaint_mode = cv2.INPAINT_NS

    def __init__(self, image):
        self.org_img = image
        self.tmp_img = image.copy()
        self.mask = np.zeros(image.shape).astype(np.uint8)
        cv2.namedWindow(self.name)
        cv2.setMouseCallback(self.name, self.drawCallback)
        cv2.createTrackbar('inpaint_radius', self.name,
                           1, 30, lambda *args: None)
        switch = '0: NS 1: TELEA'
        cv2.createTrackbar(switch, self.name, 0, 1, lambda *args: None)
        while True:
            cv2.imshow(self.name, self.tmp_img)
            self.inpaint_radius = cv2.getTrackbarPos(
                'inpaint_radius', self.name)
            self.inpaint_mode = cv2.INPAINT_TELEA if cv2.getTrackbarPos(
                switch, self.name) else cv2.INPAINT_NS
            if cv2.waitKey(1) & 0xFF == ord('m'):  # 按m键会隔两列置0
                self.zeroByTwoColumns()
            if cv2.waitKey(1) & 0xFF == ord('q'):  # 按q键退出
                break
        cv2.destroyAllWindows()

    def drawCallback(self, event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            self.drawing = True
        elif event == cv2.EVENT_MOUSEMOVE and flags == cv2.EVENT_FLAG_LBUTTON:
            if self.drawing:
                self.mask[y - self.pen_size: y + self.pen_size,
                          x - self.pen_size: x + self.pen_size] = 255
                self.tmp_img[y - self.pen_size: y + self.pen_size,
                             x - self.pen_size: x + self.pen_size] = 255
        elif event == cv2.EVENT_LBUTTONUP:
            self.drawing = False
        elif event == cv2.EVENT_RBUTTONDOWN:
            self.inpaint()
            self.showResultImage()
            self.mask[:] = 0
            self.tmp_img = self.org_img.copy()

    def inpaint(self):
        self.dst_img = cv2.inpaint(
            self.org_img, self.mask, self.inpaint_radius, self.inpaint_mode)

    def zeroByTwoColumns(self):
        for i in range(0, self.tmp_img.shape[1] - 2, 3):
            self.tmp_img[:, i + 1] = 0
            self.tmp_img[:, i + 2] = 0
            self.mask[:, i + 1] = 255
            self.mask[:, i + 2] = 255

    def showResultImage(self):
        ssim = round(measure.compare_ssim(self.org_img, self.dst_img), 3)
        mse = round(measure.compare_mse(self.org_img, self.dst_img), 3)
        cv2.imshow('mode: %s radius: %s ssim: %s mse: %s' %
                   ('TELEA' if self.inpaint_mode else 'NS', self.inpaint_radius, ssim, mse), self.dst_img)


def main():
    img = cv2.imread('datasets/dendriticCrystal.jpg', 0)
    MouseInpainting(img)


if __name__ == '__main__':
    main()
