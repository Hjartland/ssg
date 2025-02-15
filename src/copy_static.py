import os
import shutil

def copy_static(src_dir, dst_dir):
    if not os.path.exists(dst_dir):
        os.makedirs(dst_dir)
    contents = os.listdir(src_dir)
    for content in contents:
        new_dst = os.path.join(dst_dir, content)
        new_src = os.path.join(src_dir, content)
        if os.path.isfile(new_src):
            shutil.copy(new_src, new_dst)
        else:
            copy_static(new_src, new_dst)