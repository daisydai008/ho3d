Description:
	HO-3D_v3 is a dataset with 3D pose annotations for hand-objects interactions. It contains 103,462 hand-object 3D pose annotated RGB images and their corresponding depth maps. 10 different human subjects (3 female and 7 male) and 10 different objects from the YCB [1] dataset are used in this dataset. The MANO hand model [2] is used for estimating the hand pose.

Terms and conditions:
	The download and use of the dataset is for academic research only and it is free to researchers from educational institutes or public or private research labs for strictly non-commercial purposes. When downloading the dataset you agree to (unless with expressed permission of the authors): not redistribute, modificate, or commercial usage of this dataset in any way or form, either partially or entirely.

	If using this dataset, please cite the following paper:

	@ARTICLE{hampali2019honnotate,
    	      title={HOnnotate: A method for 3D Annotation of Hand and Object Poses},
              author={Shreyas Hampali and Mahdi Rad and Markus Oberweger and Vincent Lepetit},
	      booktitle = {Proc. Computer Vision and Pattern Recognition (CVPR), IEEE},
              year={2020}
             }


Contents:
	1. train: Folder with 55 sequences containing RGB, Depth and annotation files.
	2. evaluation: Folder with 13 sequences containing RGB, Depth and additional files to aid in hand pose estimation task. 
	3. train.txt: List of all training images in <sequence name>/<file id> format
	4. evaluation.txt: List of all training images in <sequence name>/<file id> format
	5. HO3D_v2_segmentations_rendered: Rendered segmentations of hand and object for all frames in the training dataset using annotated poses. Note that the segmentations are rendered at 1/4th the resolution of RGB images.
	6. calibration: Folder containing exterinsic parameters of the multi-camera setup. The parameters are provided for each of the multi-camera sequences. See 'vis_pcl_all_cameras.py' for using these parameters.
	7. manual_annotations: Folder containing manually annotated fingertip locations for 53 frames.

sequences:
	Each sequence folder consists of RGB, Depth and annotation files. The 16-bit depth map (after scaling) is strored in RGB format with LSB in red channel and MSB in green channel. Please refer to read_depth_img() function in vis_HO3D.py for decoding depth images.

annotations:
	The annotations are provided in pickled files under meta folder for each sequence. The pickle files in the training data contain a dictionary with the following keys:
	objTrans: A 3x1 vector representing object translation
	objRot: A 3x1 vector representing object rotation in axis-angle representation
	handPose: A 48x1 vector represeting the 3D rotation of the 16 hand joints including the root joint in axis-angle representation. The ordering of the joints follow the MANO model convention (see joint_order.png) and can be directly fed to MANO model.
	handTrans: A 3x1 vector representing the hand translation
	handBeta: A 10x1 vector representing the MANO hand shape parameters
	handJoints3D: A 21x3 matrix representing the 21 3D hand joint locations
	objCorners3D: A 8x3 matrix representing the 3D bounding box corners of the object
	objCorners3DRest: A 8x3 matrix representing the 3D bounding box corners of the object before applying the transormation
	objName: Name of the object as given in YCB dataset
	objLabel: Object label as given in YCB dataset
	camMat: Intrinsic camera parameters
	handVertContact: A 778D boolean vector whose each element represents whether the corresponding MANO vertex is in contact with the object. A MANO vertex is in contact if its distance to the object surface is <4mm
	handVertDist: A 778D float vector representing the distance of MANO vertices to the object surface.
	handVertIntersec: A 778D boolean vector specifying if the MANO vertices are inside the object surface.
	handVertObjSurfProj: A 778x3 matrix representing the projection of MANO vertices on the object surface.

	IMPORTANT NOTE: Some of the images in the train and evaluation folders do NOT contain annotations and the above described fields for these images are set to 'None'. Our optimization method failed to obtain accurate poses for these images. The training and evaluation set provided in 'train.txt' and 'evaluation.txt' do not contain any unannotated images and only these set of files should be used for training and evaluation.


	The hand pose annotations for the evaluation images are withheld. However, some additional information to aid the hand pose estimation task is provided in the pickle files in the meta folder of each evaluation sequence. The pickle files in the evaluation data contain a dictionary with the following keys:
	objTrans: A 3x1 vector representing object translation
	objRot: A 3x1 vector representing object rotation in Rodrigues representation
	handJoints3D: A 3x1 vector representing the 3D location of the root joint
	handBoundingBox: A 4 element list representing the 2D bounding box of the hand in the format, [topLeftX, topLeftY, bottomRightX, bottomRightY]

object models:
	Download the object models from 'https://rse-lab.cs.washington.edu/projects/posecnn/' to a folder named 'models'.

information:
	1. All annotations assume openGL coordinate system i.e., hand/objects are along negative z-axis in a right-handed coordinate system with origin at camera optic center.

[1] Y. Xiang, T. Schmidt, V. Narayanan, and D. Fox. PoseCNN: A Convolutional Neural Network for 6D Object Pose Estimation in Cluttered Scenes. In RSS, 2018.
[2] J. Romero, D. Tzionas, and M. J. Black. Embodied Hands: Modeling and Capturing Hands and Bodies Together. TOG, 36(6):245, 2017
