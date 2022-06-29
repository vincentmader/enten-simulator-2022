#!/usr/bin/env python3
from PIL import Image
import matplotlib.pyplot as plt
import numpy as np
from tqdm import tqdm
import os

name = "ducks"

path = f"../resources/sprites/{name}.png"
os.system(f"mkdir -p ../resources/sprites/{name}")
image = Image.open(path)
arr = np.asarray(image)

nr_of_rows = 8 
nr_of_cols = 12 
cell_width = int(arr.shape[1] / nr_of_cols)
cell_height = int(arr.shape[0] / nr_of_rows)

for row_id, row in tqdm(list(enumerate(arr))[::cell_height]):
    for col_id, col in list(enumerate(row))[::cell_width]:
        img = []
        for y in range(row_id, row_id+cell_height):
            res_row = []
            for x in range(col_id, col_id+cell_width):
                res_row.append(arr[y][x])
            img.append(res_row)
        img = np.array(img)
            
        fix, ax = plt.subplots(figsize=(2, 2))
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['bottom'].set_visible(False)
        ax.spines['left'].set_visible(False)
        ax.get_xaxis().set_ticks([])
        ax.get_yaxis().set_ticks([])

        plt.imshow(img)
        filename = f"{int(col_id/cell_width)}_{int(row_id/cell_height)}.png"
        plt.savefig(f"../resources/sprites/{name}/{filename}", dpi=100, transparent=True)
        plt.close()
