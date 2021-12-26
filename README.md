<h1>A Mesh-based Approach Towards the Automatization of 3D Cranial Implants Generation</h1>

<h4>Mariana Aguiar, Victor Alves, Jan Egger, Jianning Li, Christina Gsaxner<br><br>
Victor Alves - Centro Algoritmi, University of Minho, Braga, Portugal <br>
Jan Egger, Jianning Li and Christina Gsaxner - Institute of Computer Graphics and Vision, Graz University of Technology, Graz, Austria</h4> <br>

>This project is the result of Mariana Aguiar (marianacmaguiar@gmail.com), Victor Alves (valves@di.uminho.pt), Jan Egger (egger@icg.tugraz.at) work, having been developed as part of Mariana Aguiar's master thesis. 

<br>

<h2> Abstract</h2>
<p>The evolution of modern medicine and the technologies of implant design and manufacturing have allowed the number of cranioplasties performed to increase greatly, improving the quality of life of patients who have to undergo cranial reconstruction surgery. The need to generate cranial implants adapted to the individuality of each human skull as quickly and efficiently as possible has led in recent years to the search for methods that are as automated as possible and do not compromise the quality and integrity of the implant.</p>
<p>The most traditional and popular method in recent years has been to use CAD/CAM technologies, in which patient-specific cranial implants can be reliably generated. However, the process is time-consuming, and the available software has high associated costs that require skilled professionals for implant design, not allowing it to be available in all clinical settings. </p>
<p>Due to the growing interest and success of the application of Deep Learning to 3D reconstruction, recently several works have been proposed on the application of these architectures to cranial reconstruction, allowing to obtain high-quality cranial implants automatically, not only reducing the cost of the process but also enabling its availability in a larger number of clinical contexts. </p>
<p>The work proposed in this thesis to automatically reconstruct a defected skull uses as its basis the Mesh R-CNN framework by Gkioxari et al. (2019) - https://github.com/facebookresearch/meshrcnn. Inspired by the 3D system ability to take real-world RGB images as input and, by detecting each object within its image, output a high-resolution 3D mesh representing each object in the image with high flexibility for arbitrary topologies, a similar approach was proposed to explore an end-to-end method to perform skull reconstruction based on the CT images of the patient, outputting, in the end, a 3D cranial implant that could directly be imported in CAM software to fabricate the implant.
  
<br>

<h2> Materials and Methods</h2>

<h4> Data Preparation </h4>
<p>The dataset that Mesh R-CNN uses in their work is the Pix3D dataset containing a large number of aligned 2D images, and their correspondent 3D shapes. Since the proposed work deals with a medical image dataset of head CT scans, an adaptation of the data to generate a similar dataset to Pix3D had to be done, where the final adapted dataset contains pixel-wise aligned pairs of 2D skull images and their corresponding 3D shapes, along with their image masks, bboxes, voxelized skull and the camera parameters that allow producing a 3D model based on 2D images.</p>
![image](https://drive.google.com/uc?export=view&id=1QPG9xbIWRUFv002nrSNeQwmkt7jYXXij)

<h4> Data Registration, Training Configurations and Data Loader </h4>
<p>Even though all the required data was previously acquired and prepared, a dataset registration was necessary for the data to be compatible with the Detectron2 framework. The chosen standard representation for the dataset was COCO format, a well-known format for instance detection. The format consists of a list of dictionaries, where each dictionary contains the paths to the data, camera parameters information and other information such as the format of the bounding boxes, the category label and how many objects exist in the image. </p>
<p>After creating the dataset, we registered it into the DatasetCatalog of Detectron2 for both the training and testing data.
The training and testing configurations of the DL networks of the system combine Detectron2’s default configurations well known for its results, and configurations defined by us to customize them into our context, which are merged and freezed at training time. </p>
</p>

<h4> 3D Skull Reconstruction via Mesh-RCNN </h4>
<p>The proposed system integrates different neural networks with different aims divided into two main stages: a voxel stage followed by a mesh refinement stage. First, the voxel stage inputs the 2D skull image into a backbone feature extractor network CNN that outputs a feature map for the given image. Then these feature maps are inputted in a Region Proposal Network (RPN) to generate multiple ROIs where the output is classified as either having or not the object. Then an RoI Align layer is applied to extract a small feature map from each RoI, pixel-wise aligning the extracted features with the input image to preserve the spatial locations of each object. The resulting reduced feature maps serve as input for four parallel network branches: (i) a box detection branch, (ii) a mask branch, (iii) a Z depth extent branch, and (iv) a voxel branch. The first network predict a bbox and the label for each skull, the second a mask for each skull, the third network the depth extent of the skull object in the image, and the fourth network predicts a binary voxel grid for each skull. </p>
<p>The output of the voxel branch is then fed into an algorithm, named Cubify, that replaces each occupied voxel with a cuboid triangle mesh, generating a coarse 3D skull mesh. Since the 3D mesh representing each skull based on its 2D image has a coarse shape, a mesh refinement stage is applied to convert the low-resolution mesh into a high-resolution mesh. This stage refines the vertex positions by inputting the 3D skull mesh three times through mesh refinement stages. Each mesh refinement stage is comprised of three operations: vert align that extracts the 2D skull image features for the mesh vertices, propagating the acquired information through a series of graph convolutions blocks, and then the vertex positions are updated by a vertex refinement operation. </p>
