export SCENE=$1
export COLMAP=$2
export TRAIN=$3
export RNDR=$4
echo $SCENE
if $COLMAP==colmap ( yes | python3 scripts/colmap2nerf.py --colmap_matcher exhaustive --run_colmap --aabb_scale 16 --images data/$SCENE
mkdir data/data
mv data/$SCENE data/data
mkdir data/$SCENE
mv data/data data/$SCENE
mv transforms.json data/$SCENE )
if $TRAIN==train ( python3 scripts/run.py --mode nerf --scene data/$SCENE --train --save_snapshot data/$SCENE/base.msgpack
python3 scripts/tf2path.py --scene data/$SCENE )
if $RNDR==rndr python3 scripts/run.py --mode nerf --scene data/$SCENE --load_snapshot data/$SCENE/base.msgpack --video_camera_path data/$SCENE/base_cam_script.json --video_n_seconds 2 --video_fps 25 --video_output $SCENE.mp4 --height 810 --width 540
