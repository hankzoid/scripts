import argparse
import os
import json

import numpy as np
from scipy.spatial.transform import Rotation as R

def parse_args():
    parser = argparse.ArgumentParser(description="Create camera path from transforms.json")
    
    parser.add_argument("--scene", "--training_data", default="", help="The scene to load. Can be the scene's name or a full path to the training data.")
    
    args = parser.parse_args()
    return args

if __name__ == "__main__":
    args = parse_args()
    path = os.getcwd().replace("\\","/")
    path = os.path.join(path, args.scene)
    path = path.replace("\\","/")
    # path = path.replace("/","\\")
    

    def nerf_to_ngp(xf):
        mat = np.copy(xf)
        mat = mat[:-1,:]
        mat[:,1] *= -1 # flip axis
        mat[:,2] *= -1
        mat[:,3] *= 0.33 #scale
        mat[:,3] += [0.5, 0.5, 0.5] #offset
        
        mat = mat[[1,2,0], :] # swap axis
        
        rm = R.from_matrix(mat[:,:3]) 

        # quaternion (x, y, z, w) and translation
        #  + 0.025
        return rm.as_quat(), mat[:,3]

    def smooth_camera_path(path_to_transforms, ):
        out = {"path":[], "time":1.0}
        with open(path_to_transforms + '/transforms.json') as f:
            data = json.load(f)
        
        n_frames = len(data['frames'])
        # fov = 85.0
        fov = data["camera_angle_y"] * 180 / np.pi
        print(fov)
        xforms = {}
        for i in range(n_frames):
            # file = int(data['frames'][i]['file_path'].split('/')[-1][:-4])
            file = int(data['frames'][i]['file_path'].split('/')[-1][-7:-4])
            xform = data['frames'][i]['transform_matrix']
            xforms[file] = xform
            
        xforms = dict(sorted(xforms.items()))
        indexes = list(xforms.keys())
        
        # linearly take n (4) transformation from transforms.json
        for ind in np.linspace(0, n_frames - 1, 4, endpoint=True, dtype=int):
            
            q, t = nerf_to_ngp(np.array(xforms[indexes[ind]]))
            
            out['path'].append({
                "R": list(q),
                "T": list(t),
                "aperture_size":0.0,
                "fov":fov,
                "glow_mode":0,
                "glow_y_cutoff":0.0,
                "scale":1.25,
                "slice":0.0
            })
            
        with open(path_to_transforms+'/base_cam_script.json', "w") as outfile:
            json.dump(out, outfile, indent=2)

    smooth_camera_path(path)
