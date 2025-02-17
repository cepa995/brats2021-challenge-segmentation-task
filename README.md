# BraTS 2021 Challenge - Segmentation Task

This repository is designed to evaluate state-of-the-art machine learning methods for brain tumor segmentation using multi-parametric MRI (mpMRI) scans. It provides a structured framework for data organization, model development, and evaluation, adhering to best practices in data science project management.

## Project Organization

```
├── Makefile           <- Makefile with convenience commands like `make data` or `make train`
├── README.md          <- The top-level README for developers using this project.
├── data
│   ├── processed      <- The final, canonical data sets for modeling.
│   └── raw            <- The original, immutable data dump.
│
├── docs               <- Project documentation
│
├── models             <- Trained and serialized models, model predictions, or model summaries
│
├── notebooks          <- Jupyter notebooks. Naming convention is a number (for ordering),
│
├── pyproject.toml     <- Project configuration file with package metadata for 
│                         brain_tumor_segmentation and configuration for tools like black
│
├── references         <- Data dictionaries, manuals, and all other explanatory materials.
│
├── reports            <- Generated analysis as HTML, PDF, LaTeX, etc.
│   └── figures        <- Generated graphics and figures to be used in reporting
│
├── requirements.txt   <- The requirements file for reproducing the analysis environment, e.g.
│                         generated with `pip freeze > requirements.txt`
│
├── setup.cfg          <- Configuration file for flake8
│
└── brain_tumor_segmentation   <- Source code for use in this project.
    │
    ├── __init__.py             <- Makes brain_tumor_segmentation a Python module
    │
    ├── config.py               <- Store useful variables and configuration
    │
    ├── dataset.py              <- Scripts to download or generate data
    │
    ├── features.py             <- Code to create features for modeling
    │
    ├── modeling                
    │   ├── __init__.py 
    │   ├── predict.py          <- Code to run model inference with trained models          
    │   └── train.py            <- Code to train models
    │
    └── plots.py                <- Code to create visualizations
```

--------

## TODO List

| Task | Status |
|------|--------|
| Set up DVC for data versioning | ❌ Not Started |
| Implement UNETR baseline Model | ❌ Not Started |
| Implement V-Net baseline Model | ❌ Not Started |
| Implement Swin-UNETR baseline Model | ✅ Done |
| Optimize preprocessing pipeline | ⏳ In Progress |
| Add unit tests for data processing scripts | ❌ Not Started |
| Export trained model to ONNX format | ❌ Not Started |
| Setup CI/CD pipeline for automated training & deployment | ❌ Not Started |
| Deploy inference model via FastAPI or Flask | ❌ Not Started |

## Getting Started

### Clone the Repository
```bash
git clone https://github.com/cepa995/brats2021-challenge-segmentation-task.git
```

## Set Up the Environment

Ensure you have Python 3.10 installed. Install the required dependencies:
```bash
pip install -r requirements.txt
```

## Data Preparation
1. Download the BraTS 2021 dataset from the official source.
2. Place the data in the data/raw/ directory.
3. Run preprocessing scripts as needed to prepare the data for modeling.

## Training and Evaluation
### Training
Utilize the train.py script to train your models. Ensure that your data is properly organized and preprocessed before initiating training.

###Evaluation
After training, use the evaluate.py script to assess model performance on validation datasets.

## Contributing
Contributions are welcome! Please fork the repository and submit a pull request with your enhancements or bug fixes.