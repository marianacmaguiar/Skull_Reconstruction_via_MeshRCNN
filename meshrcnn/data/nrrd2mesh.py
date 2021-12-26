import open3d
import matplotlib.pylab as plt
import sys
import numpy as np
import nrrd
import os
import scipy
from skimage import measure, morphology
from glob import glob

def re_sample(image, current_spacing, new_spacing):
    resize_factor = current_spacing / new_spacing
    new_shape = image.shape * resize_factor
    new_shape = np.round(new_shape)
    actual_resize_factor = new_shape / image.shape
    new_spacing = current_spacing / actual_resize_factor

    image_resized = scipy.ndimage.interpolation.zoom(image, actual_resize_factor)

    return image_resized, new_spacing


def nrrd2mesh_complete(skull_list):
    
    for file in range(len(skull_list)):
        print('generating data:', skull_list[file])
        ct_data,ct_header=nrrd.read(skull_list[file])


        ct_spacing = np.asarray([ct_header['space directions'][0, 0],
                             ct_header['space directions'][1, 1],
                             ct_header['space directions'][2, 2]])

        ct_origin = np.asarray([ct_header['space origin'][0],
                            ct_header['space origin'][1],
                            ct_header['space origin'][2]])

        print('20.0')
        # cut the head region. if the head is approx 18 cm high, calculate the number of slices using the slice thickness
        # for PET, i also try to crop the brain
        if ct_spacing[2] > 0:
            num_slices = int(180 / ct_spacing[2])
            ct_data = ct_data[:, :, -num_slices:]

        # resample data to uniform spacing of 1x1x1mm
        if ct_spacing[2] > 0:
            ct_data_resampled, _ = re_sample(ct_data, ct_spacing, new_spacing=[1, 1, 1])
        else:
            ct_data_resampled = ct_data

        print('40.0')
        # mask skin area
        skin_masked = ct_data_resampled


        skin_verts, skin_faces, skin_norm, skin_val = measure.marching_cubes_lewiner(skin_masked,step_size=1)
        skin_verts = skin_verts
        skin_points = skin_verts[:, [1, 0, 2]]
        # create mesh
        skin_mesh = open3d.geometry.TriangleMesh()
        skin_mesh.vertices = open3d.utility.Vector3dVector(skin_points)
        skin_mesh.triangles = open3d.utility.Vector3iVector(skin_faces)
        skin_mesh.compute_vertex_normals()
    
        # write mesh
        filename = complete_mesh_dir+skull_list[file][-8:-5]
        open3d.utility.set_verbosity_level(open3d.utility.VerbosityLevel.Error)
        open3d.io.write_triangle_mesh(filename + '.obj', skin_mesh)
        open3d.utility.set_verbosity_level(open3d.utility.VerbosityLevel.Info)
   
    

def nrrd2mesh_defective(skull_list):
    
    for file in range(len(skull_list)):
        print('generating data:', skull_list[file])
        ct_data,ct_header=nrrd.read(skull_list[file])
    
        ct_spacing = np.asarray([ct_header['space directions'][0, 0],
                             ct_header['space directions'][1, 1],
                             ct_header['space directions'][2, 2]])

        ct_origin = np.asarray([ct_header['space origin'][0],
                            ct_header['space origin'][1],
                            ct_header['space origin'][2]])

        print('20.0')
        # cut the head region. if the head is approx 18 cm high, calculate the number of slices using the slice thickness
        # for PET, i also try to crop the brain
        if ct_spacing[2] > 0:
            num_slices = int(180 / ct_spacing[2])
            ct_data = ct_data[:, :, -num_slices:]

        # resample data to uniform spacing of 1x1x1mm
        if ct_spacing[2] > 0:
            ct_data_resampled, _ = re_sample(ct_data, ct_spacing, new_spacing=[1, 1, 1])
        else:
            ct_data_resampled = ct_data

        print('40.0')
        # mask skin area
        skin_masked = ct_data_resampled


        skin_verts, skin_faces, skin_norm, skin_val = measure.marching_cubes_lewiner(skin_masked,step_size=1)
        skin_verts = skin_verts
        skin_points = skin_verts[:, [1, 0, 2]]
        # create mesh
        skin_mesh = open3d.geometry.TriangleMesh()
        skin_mesh.vertices = open3d.utility.Vector3dVector(skin_points)
        skin_mesh.triangles = open3d.utility.Vector3iVector(skin_faces)
        skin_mesh.compute_vertex_normals()
    
        # write mesh
        filename = defective_mesh_dir+skull_list[file][-8:-5]
        open3d.utility.set_verbosity_level(open3d.utility.VerbosityLevel.Error)
        open3d.io.write_triangle_mesh(filename + '.stl', skin_mesh)
        open3d.utility.set_verbosity_level(open3d.utility.VerbosityLevel.Info)
   
    
    

if __name__ == '__main__':
 
    #****** create directories to save the meshes *******
    
    if not os.path.exists('../../../../data/meshes'):
        os.makedirs('../../../../data/meshes')
        
    if not os.path.exists('../../../../data/meshes/complete_skull'):
        os.makedirs('../../../../data/meshes/complete_skull')
        
    if not os.path.exists('../../../../data/meshes/defective_skull'):
        os.makedirs('../../../../data/meshes/defective_skull')
        
    

    #****** Get list of nrrd files and folder definition, then call function to convert to mesh ******
    
    # COMPLETE SKULL
    complete_skull_dir=glob('{}/*.nrrd'.format('../../../../data/training_set/novas/'))
    complete_mesh_dir = '../../../../data/meshes/novas/'
    nrrd2mesh_complete(complete_skull_dir)
    
    
    # DEFECTIVE SKULL
    #defected_skull_dir=glob('{}/*.nrrd'.format('../../../../data/training_set/novas/'))
    #defective_mesh_dir='../../../../data/meshes/defective_skull/'
#    nrrd2mesh_defective(defected_skull_dir)

    
        
