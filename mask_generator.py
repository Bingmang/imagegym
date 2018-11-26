import argparse
from PIL import Image
import numpy as np

parser = argparse.ArgumentParser()
parser.add_argument('--size', required=True, type=int, help='the size of the image')
parser.add_argument('--line', required=True, type=int, help='the gap between two line')
parser.add_argument('--out',  default='generated_mask.png', help='path to save mask')

opt = parser.parse_args()
print(opt)

BG_VALUE = 0        # background value
FR_VALUE = 255      # front value

def generate_mask(size, line, out):
    mask = np.full((size, size), FR_VALUE, dtype=np.uint8)
    for row in range(0, size, 1 + line):
        mask[row, :] = BG_VALUE
    return mask

def main():
    generated_mask = generate_mask(opt.size, opt.line, opt.out)
    img = Image.fromarray(generated_mask).save(opt.out)
    return

if __name__ == '__main__':
    main()
