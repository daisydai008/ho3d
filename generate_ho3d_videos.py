"""
Simple video generation for MC sequences in HO3D dataset
Compatible with Python 2.7
"""
from __future__ import print_function, unicode_literals
import os
import cv2
import numpy as np
import argparse
from utils.vis_utils import *

def setup_mano():
    """Setup MANO model for hand pose visualization"""
    MANO_MODEL_PATH = './mano/models/MANO_RIGHT.pkl'
    
    if not os.path.exists(MANO_MODEL_PATH):
        raise Exception('MANO model missing! Please run setup_mano.py to setup mano folder')
    
    try:
        from mano.webuser.smpl_handpca_wrapper_HAND_only import load_model
        return load_model, MANO_MODEL_PATH
    except ImportError:
        raise Exception('MANO model not properly installed')

def forwardKinematics(fullpose, trans, beta, load_model_func, model_path):
    '''MANO parameters --> 3D pts, mesh'''
    assert fullpose.shape == (48,)
    assert trans.shape == (3,)
    assert beta.shape == (10,)

    m = load_model_func(model_path, ncomps=6, flat_hand_mean=True)
    m.fullpose[:] = fullpose
    m.trans[:] = trans
    m.betas[:] = beta

    return m.J_transformed.r, m

# mapping of joints from MANO model order to simple order(thumb to pinky finger)
jointsMapManoToSimple = [0,
                         13, 14, 15, 16,
                         1, 2, 3, 17,
                         4, 5, 6, 18,
                         10, 11, 12, 19,
                         7, 8, 9, 20]

def create_annotated_video(base_dir, seq_name, output_dir, load_model_func, model_path):
    """Create video with hand pose and object annotations"""
    print("Processing sequence with annotations: {}".format(seq_name))
    
    # Get all RGB images
    rgb_dir = os.path.join(base_dir, 'train', seq_name, 'rgb')
    if not os.path.exists(rgb_dir):
        print("RGB directory not found: {}".format(rgb_dir))
        return False
    
    # Get frame files
    frame_files = sorted([f for f in os.listdir(rgb_dir) if f.endswith('.jpg') or f.endswith('.png')])
    frame_ids = [os.path.splitext(f)[0] for f in frame_files]
    
    if len(frame_files) == 0:
        print("No frames found")
        return False
    
    print("Found {} frames".format(len(frame_files)))
    
    # Read first frame for dimensions
    first_img = read_RGB_img(base_dir, seq_name, frame_ids[0], 'train')
    height, width = first_img.shape[:2]
    
    # Setup video writer
    output_path = os.path.join(output_dir, '{}_annotated.avi'.format(seq_name))
    fourcc = 1196444237  # MJPG fourcc value that works
    video_writer = cv2.VideoWriter(output_path, fourcc, 45.0, (width, height))
    
    if not video_writer.isOpened():
        print("Failed to open video writer")
        return False
    
    print("Creating annotated video...")
    
    successful_frames = 0
    skipped_frames = 0
    
    # Process frames
    for i, frame_id in enumerate(frame_ids):
        if i % 100 == 0:
            print("Progress: {}/{}".format(i, len(frame_ids)))
        
        try:
            # Read image and annotation
            img = read_RGB_img(base_dir, seq_name, frame_id, 'train')
            anno = read_annotation(base_dir, seq_name, frame_id, 'train')
            
            # Create annotated image
            imgAnno = np.copy(img)
            
            # Add annotations if available
            if anno is not None and anno.get('objRot') is not None:
                # Get object 3D corner locations
                if 'objCorners3DRest' in anno and anno['objCorners3DRest'] is not None:
                    try:
                        objCorners = anno['objCorners3DRest']
                        objCornersTrans = np.matmul(objCorners, cv2.Rodrigues(anno['objRot'])[0].T) + anno['objTrans']
                        objKps = project_3D_points(anno['camMat'], objCornersTrans, is_OpenGL_coords=True)
                        imgAnno = showObjJoints(imgAnno, objKps, lineThickness=2)
                    except:
                        pass
                
                # Get hand pose
                if (anno.get('handPose') is not None and anno.get('handTrans') is not None and 
                    anno.get('handBeta') is not None):
                    try:
                        handJoints3D, handMesh = forwardKinematics(anno['handPose'], anno['handTrans'], 
                                                                 anno['handBeta'], load_model_func, model_path)
                        handKps = project_3D_points(anno['camMat'], handJoints3D, is_OpenGL_coords=True)
                        imgAnno = showHandJoints(imgAnno, handKps[jointsMapManoToSimple])
                        successful_frames += 1
                    except:
                        skipped_frames += 1
                        pass
                else:
                    skipped_frames += 1
            else:
                skipped_frames += 1
            
            # Add frame info
            font = cv2.FONT_HERSHEY_SIMPLEX
            cv2.putText(imgAnno, 'Seq: {} Frame: {}'.format(seq_name, frame_id), 
                       (10, 30), font, 0.7, (255, 255, 255), 2)
            
            video_writer.write(imgAnno)
            
        except Exception as e:
            print("Error processing frame {}: {}".format(frame_id, str(e)))
            # Write original frame
            try:
                img = read_RGB_img(base_dir, seq_name, frame_id, 'train')
                video_writer.write(img)
            except:
                pass
    
    video_writer.release()
    print("Annotated video saved: {}".format(output_path))
    print("Successful annotations: {}, Skipped: {}".format(successful_frames, skipped_frames))
    return True

def create_simple_video(base_dir, seq_name, output_dir):
    """Create a simple video from RGB frames with basic annotations"""
    print("Processing sequence: {}".format(seq_name))
    
    # Get all RGB images
    rgb_dir = os.path.join(base_dir, 'train', seq_name, 'rgb')
    if not os.path.exists(rgb_dir):
        print("RGB directory not found: {}".format(rgb_dir))
        return False
    
    # Get frame files
    frame_files = sorted([f for f in os.listdir(rgb_dir) if f.endswith('.jpg') or f.endswith('.png')])
    if len(frame_files) == 0:
        print("No frames found")
        return False
    
    print("Found {} frames".format(len(frame_files)))
    
    # Read first frame for dimensions
    first_frame_path = os.path.join(rgb_dir, frame_files[0])
    first_img = cv2.imread(first_frame_path)
    height, width = first_img.shape[:2]
    
    # Setup video writer
    output_path = os.path.join(output_dir, '{}_simple.avi'.format(seq_name))
    # Use integer fourcc value for MJPG (known to work from earlier test)
    fourcc = 1196444237  # This is the MJPG fourcc value from our earlier test
    video_writer = cv2.VideoWriter(output_path, fourcc, 45.0, (width, height))
    
    if not video_writer.isOpened():
        print("Failed to open video writer")
        return False
    
    print("Creating video...")
    
    # Process frames
    for i, frame_file in enumerate(frame_files):
        if i % 100 == 0:
            print("Progress: {}/{}".format(i, len(frame_files)))
        
        frame_path = os.path.join(rgb_dir, frame_file)
        img = cv2.imread(frame_path)
        
        if img is not None:
            # Add frame info
            font = cv2.FONT_HERSHEY_SIMPLEX
            cv2.putText(img, 'Seq: {} Frame: {}'.format(seq_name, i), 
                       (10, 30), font, 0.7, (255, 255, 255), 2)
            
            video_writer.write(img)
    
    video_writer.release()
    print("Video saved: {}".format(output_path))
    return True

def main():
    parser = argparse.ArgumentParser(description='Generate videos for MC sequences')
    parser.add_argument('ho3d_path', type=str, help='Path to HO3D dataset')
    parser.add_argument('-o', '--output', type=str, default='videos', help='Output directory')
    parser.add_argument('-s', '--sequences', nargs='+', default=['GSF11'],
                       help='Sequences to process')
    parser.add_argument('--annotated', action='store_true', help='Create annotated videos with hand poses')
    
    args = parser.parse_args()
    
    if not os.path.exists(args.output):
        os.makedirs(args.output)
    
    # Setup MANO if creating annotated videos
    load_model_func = None
    model_path = None
    if args.annotated:
        try:
            load_model_func, model_path = setup_mano()
            print("MANO model loaded successfully")
        except Exception as e:
            print("Error setting up MANO: {}".format(str(e)))
            print("Falling back to simple videos...")
            args.annotated = False
    
    success_count = 0
    for seq_name in args.sequences:
        print("\n" + "="*50)
        try:
            if args.annotated:
                success = create_annotated_video(args.ho3d_path, seq_name, args.output, load_model_func, model_path)
            else:
                success = create_simple_video(args.ho3d_path, seq_name, args.output)
                
            if success:
                success_count += 1
        except Exception as e:
            print("Error processing {}: {}".format(seq_name, str(e)))
    
    print("\n" + "="*50)
    print("Completed! {} out of {} sequences processed".format(success_count, len(args.sequences)))

if __name__ == '__main__':
    main()