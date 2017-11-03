# Data Generation
Lower Jawbone Data Generation for Deep Learning Tools under MeVisLab

To use medical datasets for training deep learning segmentation nets, a preparation of data is obligatory. 
Therefore, a network of MeVisLab image processing modules ("Save Slices for Deep Learning") is provided.
This network ensures an automatic and separate storage of the slices of a dataset and the ground truth contours are converted into binary masks. Moreover, data augmentation methods are implemented with an own MeVisLab macro module ("SaveAsSingleSlices") to increase a small amount of available training images.
Hence, geometric transformations including flipping, rotation and scaling as well as adding noise (Uniform, Gaussian and Salt and Pepper) is permitted with the generated macro module. Generally, this macro module is a practicable support to save original and
deformed images separately, and independently of a specific task.



Please cite this paper, if you use the software:
Birgit Pfarrkirchner, Christina Gsaxner, Lydia Lindner, Norbert Jakse, Jürgen Wallner, Dieter Schmalstieg, Jan Egger. 
"Lower Jawbone Data Generation for Deep Learning Tools under MeVisLab".  
SPIE Medical Imaging 2018.




