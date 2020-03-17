## Visualization
### REST-API Internal Interface

As explained in the previous sections, the available functions are:
•	search_address: this option shows the different probabilities of a given address to be a class.
•	list_classes: it shows the different classes available in the system.
•	class_checker: given an address, a class type and a confidence it returns a boolean for the given prediction.

### Internal Interface
The internal interface will be available typing XXX.XXX.XXX.XXX:8810 in any browser, where XXX.XXX.XXX.XXX is the IP of the machine where you have installed the interface. This module is created in python using flask and javascript, and it allows users to show the results of predictions in a friendly way.
The Interface allows users to choose which calls to compute by selecting a radio button, Classifier (first call), List Class (second call) and Confidence (third call).


### First Call (Search Address)
The user must indicate the address he wants to look for, then the system returns a graph with the class percentage that the predictor assigns to the entity related to the requested address. Among the information, will be available the cluster label assigned to the entity and the version of the used classifier.

![alt text](example.jpg "Example")

### Second Call (Class list)
To see the list of the available classes during the classification and their abbreviations. This call is useful to know the training classes and for example for using the result in the third call. To get the list of the available classes, the user must check the second radio button and then click on the button, without introducing any other information.

### Third Call (Entity checker)
The user must indicate an address, an abbreviation of the class related to the entity which belong the indicated address and a percentage of the classification (or confidence value) to be verified. The system returns a Red Light if the condition will be not verified (for example for wrong indicated class or value of confidence indicated lower than the value predicted), a Green Light otherwise. 
