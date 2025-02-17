from pathlib import Path

from dotenv import load_dotenv
from loguru import logger

# Load environment variables from .env file if it exists
load_dotenv()

# Root project path
PROJ_ROOT = Path(__file__).resolve().parents[1]
logger.info(f"PROJ_ROOT path is: {PROJ_ROOT}")

# Data-related paths
DATA_DIR = PROJ_ROOT / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
INTERIM_DATA_DIR = DATA_DIR / "interim"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
PROCESSED_METADATA_DIR = PROCESSED_DATA_DIR / "DICOM_Metadata"
DATASPLIT_DIRECTORY = PROJ_ROOT / "notebooks" / "data-engineering" / "dataset-split-strategies"
EXTERNAL_DATA_DIR = DATA_DIR / "external"
BRATS_2021_DICOMDIR =  DATA_DIR / "raw" / "PKG-RSNA-ASNR-MICCAI-BraTS-2021" / "RSNA-ASNR-MICCAI-BraTS-2021" / "BraTS2021_DICOMDIR"
BRATS_2021_NIfTI_DIR =  DATA_DIR / "raw" / "PKG-RSNA-ASNR-MICCAI-BraTS-2021" / "RSNA-ASNR-MICCAI-BraTS-2021" / "BraTS2021_NIfTI"

# Other paths
MODELS_DIR = PROJ_ROOT / "models"
REPORTS_DIR = PROJ_ROOT / "reports"
FIGURES_DIR = REPORTS_DIR / "figures"

# If tqdm is installed, configure loguru with tqdm.write
# https://github.com/Delgan/loguru/issues/135
try:
    from tqdm import tqdm

    logger.remove(0)
    logger.add(lambda msg: tqdm.write(msg, end=""), colorize=True)
except ModuleNotFoundError:
    pass
