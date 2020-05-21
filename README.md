# heuristica

----

Simple tool to manually develop heuristics based on a user defined rule set. As of now there's only an code example which applies one specific rule on a given binary classification problem and visualize the results in a scatter matrix (as shown in the screenshot below). 

The Future plans are:

- Definition and application of multiple used defined rules
- Development of a graphical user interface for defining rules and visualizing the results (based on PySide2, maybe later HTML)
- Different means for result evaluation
  - Integration of different rule metrics
  - Interactive selection of scatter attributes
- Rule suggestion mechanism
- Different rule concatenations

![scatter_example](images/scatter_example.png)

## Installation

Create the python environment using:
`conda env create -f environment.yml`

