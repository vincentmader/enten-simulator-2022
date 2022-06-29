from PIL import Image
import matplotlib.pyplot as plt
import numpy as np
from tqdm import tqdm
import os

name = "penguins"

path = f"./sprites/{name}.png"
os.system(f"mkdir -p ./sprites/{name}")
image = Image.open(path)
arr = np.asarray(image)

for row_id, row in tqdm(list(enumerate(arr))[::48]):
    for col_id, col in list(enumerate(row))[::48]:
        img = []
        for y in range(row_id, row_id+48):
            res_row = []
            for x in range(col_id, col_id+48):
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
        # plt.xlim(0, 48)
        # plt.ylim(0, 48)

        plt.imshow(img)
        filename = f"{int(col_id/48)}_{int(row_id/48)}.png"
        plt.savefig(f"./sprites/{name}/{filename}", dpi=100, transparent=True)
        plt.close()
