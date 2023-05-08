# -*- coding: utf-8 -*-
"""SAM Model.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1kFyn1fs9Y0AdTTU3UGCQNdVcFXuBsQUi
"""

#https://blog.roboflow.com/how-to-use-segment-anything-model-sam/#:~:text=How%20to%20Use%20the%20Segment%20Anything%20Model%20%28SAM%29,Convert%20Object%20Detection%20Datasets%20into%20Segmentation%20Masks%20
#Activate GPUs

!nvidia-smi

import os
HOME=os.getcwd()

# Commented out IPython magic to ensure Python compatibility.
# %cd {HOME}
import sys
!{sys.executable} -m pip install 'git+https://github.com/facebookresearch/segment-anything.git'

!pip install -q jupyter_bbox_widget roboflow dataclasses-json supervision

# Commented out IPython magic to ensure Python compatibility.
# %cd {HOME}
!mkdir {HOME}/weights
# %cd {HOME}/weights

!wget -q https://dl.fbaipublicfiles.com/segment_anything/sam_vit_h_4b8939.pth

import os
CHECKPOINT_PATH=os.path.join(HOME,"weights","sam_vit_h_4b8939.pth")

# Commented out IPython magic to ensure Python compatibility.
# %cd {HOME}
!mkdir {HOME}/data
# %cd {HOME}/data

import torch
from segment_anything import sam_model_registry

DEVICE = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
MODEL_TYPE = "vit_h"

sam = sam_model_registry[MODEL_TYPE](checkpoint=CHECKPOINT_PATH)
sam.to(device=DEVICE)

import cv2
from segment_anything import SamAutomaticMaskGenerator

mask_generator = SamAutomaticMaskGenerator(sam)
IMAGE_PATH='/content/data/satim.jpg'
image_bgr = cv2.imread(IMAGE_PATH)
image_rgb = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2RGB)
result = mask_generator.generate(image_rgb)



import supervision as sv


mask_annotator = sv.MaskAnnotator()
detections = sv.Detections.from_sam(result)
annotated_image = mask_annotator.annotate(image_bgr, detections,opacity=1)
#sv.plot_images_grid(images=[image_bgr,annotated_image],grid_size=(1,2))
sv.plot_image(image=annotated_image)













