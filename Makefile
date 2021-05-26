# install:
#     conda create -n betaSTT python3.7 -y
#     conda activate betaSTT
#     conda install pytorch torchvision -c pytorch
#     conda install pytorch cudatoolkit=10.1 torchvision -c pytorch
#     pip install mmcv-full -f https://download.openmmlab.com/mmcv/dist/cu101/torch1.5/index.html
#     git clone https://github.com/open-mmlab/mmcv.git
#     cd mmcv
#     MMCV_WITH_OPS=1 pip install -e .  # package mmcv-full, which contains cuda ops, will be installed after this step
#     # OR pip install -e .  # package mmcv, which contains no cuda ops, will be installed after this step
#     cd ..
#     git clone git@github.com:open-mmlab/mmpose.git
#     cd mmpose
#     pip install -r requirements.txt
#     python setup.py develop

    
