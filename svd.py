from PIL import Image
import numpy as np
from pillow_heif import register_heif_opener
import time
import hashlib
import os

def get_file_md5(path):
    # 获取 该path中的图片的hash
    with open(path, 'rb') as f:
        return hashlib.md5(f.read()).hexdigest()
    
def svd(image):
    register_heif_opener() 

    # 保证一定有这样一个文件夹
    script_path = os.path.abspath(__file__)
    script_dir = os.path.dirname(script_path)
    cache_dir = os.path.join(script_dir, 'svd_cache')

    if not os.path.exists(cache_dir):
        os.makedirs(cache_dir)

    path = image.filename
    img_hash = get_file_md5(path)
    cache_path = os.path.join(cache_dir, f"{img_hash}.npz")

    if os.path.exists(cache_path):
        data = np.load(cache_path)
        U = data['U']
        S = data['S']
        Vt = data['Vt']
    else:
        arr = np.array(image)
        images_arr = [arr[:,:,i] for i in range(3)]

        U = []
        S = []
        Vt = []

        for i in range(3):
            u, s, vt = np.linalg.svd(images_arr[i], full_matrices=False)
            U.append(u)
            S.append(s)
            Vt.append(vt)
        np.savez_compressed(cache_path, U = U, S = S, Vt = Vt)

    return U, S, Vt

def stack(U, S, Vt, k):
    new_image_arrs = [U[i][:, :k] @ (S[i][:k, None] * Vt[i][:k, :]) for i in range(3)]
    new_image_arr = np.stack(new_image_arrs, axis= 2)
    
    new_image_arr = np.clip(new_image_arr, 0, 255).astype(np.uint8)
    out_put_image = Image.fromarray(new_image_arr)
    return out_put_image

def ratio(S, k):
    if k <= 0:
        return "0%"
    #  print(self.image.shape)
    total_energy = 0
    captured_energy = 0

    for s in S:
        total_energy += np.sum(s ** 2)
        captured_energy += np.sum(s[:k] ** 2)

    return (f'{(captured_energy / total_energy):.8%}')