# heuristica

Simple tool to manually develop heuristics based on a user defined rule set. As of now there's only an code example which applies one specific rule on a given binary classification problem and visualize the results in a scatter matrix (as shown in the screenshot below). 

![scatter_example](images/scatter_example.png)

The Future plans are:

- Definition and application of multiple used defined rules
- Development of a graphical user interface for defining rules and visualizing the results (based on PySide2, maybe later HTML)
- Different means for result evaluation
  - Integration of different rule metrics
  - Interactive selection of scatter attributes
- Rule suggestion mechanism
- Different rule concatenations

Mockup of the planned UI:

![ui_sketch](images/ui_sketch.png)

Current state of the UI stub:

![ui_stub](images/ui_stub.png)

## Installation

Create the python environment using:

```shell
conda env create -f environment.yml
```

Activate Environment:

```shell
conda activate heuristica
```

Run Notebook-Server and open the notebook :

```shell
jupyter lab notebook/Rule_Scatter.ipynb
```

The UI stub can be started by the following commands:

```shell
cd src
python app.py
```


