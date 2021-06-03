import re
import os
import csv
import shutil
import subprocess
import numpy as np
import cv2 as cv
import networkx
from networkx.algorithms.components.connected import connected_components

'''

FFMPEG options:

-i: input url
-f: output format
-b: bitrate (default: 200kbps)
-r: fps/frame rate (default 25)
-y: overwrite output file without asking
-g: gop size
    GOP size is 300 means one intra frame every 10 seconds for 29.97fps input video

-vf: video filter
-vsync: video sync
    0: Each frame is passed with its timestamp from the demuxer to the muxer

_:v - for video
_:a - for audio 

'''

# [DECODING]: convert video into images sequence
def extract_images_from_video(images_path, fps):
    if not os.path.isdir(images_path):
        return

    for fname in os.listdir(images_path):
        if "png" not in fname:
            continue
        else:
            os.remove(os.path.join(images_path, fname))

    encoded_vid_path = os.path.join(images_path, "temp.mp4")
    extacted_images_path = os.path.join(images_path, "%010d.png")
    decoding_result = subprocess.run(["ffmpeg", "-y",
                                      "-i", encoded_vid_path,
                                      "-pix_fmt", "yuvj420p",
                                    #   "-g", "8", 
                                      "-r", fps,
                                      "-q:v", "2",
                                    #   "-vsync", "0", 
                                      "-start_number", "0",
                                      extacted_images_path],
                                     stdout=subprocess.PIPE,
                                     stderr=subprocess.PIPE,
                                     universal_newlines=True)
    if decoding_result.returncode != 0:
        print("DECODING FAILED")
        print(decoding_result.stdout)
        print(decoding_result.stderr)
        exit()
    
    print("done. imgs in ", images_path)

    # fnames = sorted(
    #     [os.path.join(images_path, name)
    #      for name in os.listdir(images_path) if "png" in name])
    # fids = sorted(list(set([r.fid for r in req_regions.regions])))
    # fids_mapping = zip(fids, fnames) # one-to-one mapping => fids_mapping = [(fid1, fname1), (fid2, fname2), ...]
    # for fname in fnames:
    #     # Rename temporarily
    #     os.rename(fname, f"{fname}_temp")

    # for fid, fname in fids_mapping:
    #     os.rename(os.path.join(f"{fname}_temp"),
    #               os.path.join(images_path, f"{str(fid).zfill(10)}.png"))

fps = "2"
images_path = "../dataset/for_decode_fps/r_2"
extract_images_from_video(images_path, fps)