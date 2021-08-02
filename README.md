library containing utilities for handling the dataset.

generate_labels: it generates label images via a label file in json VGG format.

	- arguments:
		- split_dataset: is the dataset splitted into training and validation set? in that case, you need
		  to provide the path to the parent directory of those dirs. Otherwise, just add the directory 
		  of the main directory you want to analyze.
		  
		- dataset_path: path to the main dir you want to start analyzing from (whether it contains train and
		  and valid or not)
		  
		- check_labels: command used for checking which image do still need to be labeled. Current labels 
		  are stored inside the Vgg json file you provide via command line
		  
	        - label_file_path: path to the label file we use to generate label mask from.
		
		- label_name: label name to look for in the label file. Labels can be multitple: in that case,just 
		  provide a list. 

		- count_labels: bool for renaming every file inside in a specified folder incrementally
		
		- starting_point: startgin number for naming each file in the dataset
