import os
import warnings
import multiprocessing

import cv2
import numpy as np
import pandas as pd
import pydicom
from loguru import logger
from skimage.feature import graycomatrix, graycoprops
from tqdm import tqdm

class DICOMProcessor:
    """
    A class for processing DICOM files, extracting metadata, image statistics,
    and GLCM texture features, and handling parallel processing of multiple subjects.
    """
    def __init__(self, root_directory: str, num_workers: int = 4):
        """
        Initialize the DICOMProcessor class.
        
        Parameters:
            root_directory (str): The root directory containing DICOM subject folders.
            num_workers (int): Number of processes for parallel execution.
        """
        self.root_directory = root_directory
        self.num_workers = num_workers
        self.scan_types = ["FLAIR", "T1w", "T1wCE", "T2w"]
        warnings.filterwarnings("ignore")
    
    def clean_dataframe(self, df):
        """ Drop NULL columns, and create 2x (X and Y)
        columns corresponding to current PixelSpacing column """
        df = df.dropna(axis=1, how="all")  # Drop columns where all values are NaN

        if "PixelSpacing" in df.columns:
            df[["PixelSpacing_X", "PixelSpacing_Y"]] = df["PixelSpacing"].str.strip("[]").str.split(",", expand=True).astype(float)
            df = df.drop(columns=["PixelSpacing"])  # Remove original column

        return df

    def extract_dicom_metadata(self, dicom_file: str) -> dict:
        """
        Extract metadata from a DICOM file.

        Parameters:
            dicom_file (str): Path to the DICOM file.

        Returns:
            dict: A dictionary containing extracted metadata, including:
                - PatientID
                - StudyDate
                - Modality
                - Manufacturer
                - MagneticFieldStrength
                - SliceThickness
                - PixelSpacing
                - ImageType
                - BodyPartExamined
                - ContrastBolusAgent
                - RepetitionTime
                - EchoTime

            If an error occurs, returns None.
        """
        try:
            ds = pydicom.dcmread(dicom_file, stop_before_pixels=True)
            metadata_keys = [
                "PatientID", "StudyDate", "Modality", "Manufacturer", "MagneticFieldStrength",
                "SliceThickness", "PixelSpacing", "ImageType", "BodyPartExamined",
                "ContrastBolusAgent", "RepetitionTime", "EchoTime"
            ]
            metadata = {key: getattr(ds, key, None) for key in metadata_keys}
            metadata["DCMFileName"] = os.path.basename(dicom_file)
            return metadata
        except Exception as e:
            logger.error(f"Error reading {dicom_file}: {e}")
            return None
    
    def extract_image_statistics(self, dicom_file: str) -> dict:
        """
        Extract basic image statistics from a DICOM file.

        Parameters:
            dicom_file (str): Path to the DICOM file.

        Returns:
            dict: A dictionary containing the following image statistics:
                - MeanIntensity: Mean pixel intensity.
                - StdIntensity: Standard deviation of pixel intensities.
                - Entropy: Entropy of the pixel intensity distribution.

            If an error occurs, returns None.
        """
        try:
            ds = pydicom.dcmread(dicom_file)
            pixel_array = ds.pixel_array.astype(np.float32)
            pixel_array = cv2.normalize(pixel_array, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)
            mean_intensity = np.mean(pixel_array)
            std_intensity = np.std(pixel_array)
            entropy = cv2.calcHist([pixel_array], [0], None, [256], [0, 256]).flatten()
            entropy_value = -np.sum(entropy * np.log2(entropy + 1e-7))
            return {
                "MeanIntensity": mean_intensity,
                "StdIntensity": std_intensity,
                "Entropy": entropy_value
            }
        except Exception as e:
            logger.error(f"Error processing image data from {dicom_file}: {e}")
            return None
    
    def extract_glcm_features(self, dicom_file: str) -> dict:
        """
        Extract Gray-Level Co-occurrence Matrix (GLCM) texture features from a DICOM file.
        The Gray-Level Co-occurrence Matrix (GLCM) is a powerful texture analysis technique
        used in medical imaging and computer vision. It helps describe how pixel intensity 
        levels are spatially related to each other in an image. These features provide 
        valuable insights into the texture of medical images, which can improve AI-based 
        tumor segmentation and classification.
        
        Parameters:
            dicom_file (str): Path to the DICOM file.

        Returns:
            dict: A dictionary containing the following GLCM features:
                - GLCM_Contrast: Measure of intensity contrast between adjecent pixels.
                High contrast indicates a sharp difference between neighboring pixel
                values, while low contrast means smooth textures with little variation
                - GLCM_Correlation: Measure of intensity correlation.
                - GLCM_Energy: Measure of uniformity - how structured an image is. High
                energy means the image has repeated patterns or uniformity, while low
                energy means the image is chaotic or high variable. For example, Edema
                and necrotic tumors have low energy, whily healthy tissue has higher energy
                This feature can be used to calsify tumor subtypes based on texture difference.
                - GLCM_Homogeneity: Measures how similar pixel intesnites are to their 
                neighbors. High homogeneity means smooth, uniform regions. Low homogeneity
                means more variation and rough textures - Tumors often have low homogeneity
                because of irregular structures and necrosis. WM and CSF have high homogeneity
                as their textures are smoother.

            If an error occurs, returns None.
        """
        try:
            ds = pydicom.dcmread(dicom_file)
            pixel_array = ds.pixel_array.astype(np.uint8)
            glcm = graycomatrix(pixel_array, distances=[1], angles=[0], levels=256, symmetric=True, normed=True)
            return {
                "GLCM_Contrast": graycoprops(glcm, 'contrast')[0, 0],
                "GLCM_Correlation": graycoprops(glcm, 'correlation')[0, 0],
                "GLCM_Energy": graycoprops(glcm, 'energy')[0, 0],
                "GLCM_Homogeneity": graycoprops(glcm, 'homogeneity')[0, 0]
            }
        except Exception as e:
            logger.error(f"Error extracting GLCM features from {dicom_file}: {e}")
            return None
    
    def process_dicom_directory(self, directory: str) -> pd.DataFrame:
        """
        Process all DICOM files in a specified directory and extract metadata, 
        image statistics, and texture features.

        Parameters:
            directory (str): Path to the directory containing DICOM files.

        Returns:
            pandas.DataFrame: A DataFrame containing extracted features for each DICOM file, including:
                - DICOM metadata (e.g., PatientID, StudyDate, Modality)
                - Image statistics (e.g., MeanIntensity, StdIntensity, Entropy)
                - Texture features (e.g., GLCM_Contrast, GLCM_Correlation, GLCM_Energy, GLCM_Homogeneity)

            If no DICOM files are found, an empty DataFrame is returned.
        """
        data = []
        for root, _, files in os.walk(directory):
            for file in tqdm(files, desc="Processing DICOM files"):
                if file.endswith(".dcm"):
                    dicom_path = os.path.join(root, file)
                    metadata = self.extract_dicom_metadata(dicom_path)
                    image_stats = self.extract_image_statistics(dicom_path)
                    glcm_features = self.extract_glcm_features(dicom_path)
                    if metadata and image_stats and glcm_features:
                        data.append({**metadata, **image_stats, **glcm_features})
        return pd.DataFrame(data)

    def process_subject(self, subject_path) -> list:
        """
        Process all four DICOM directories (FLAIR, T1w, T1wCE, T2w) for a single subject.
        """
        # Parse subject ID
        subject_id = os.path.basename(subject_path)
        
        # For each scan type, process DICOMDIR and return parsed results
        subject_results = []
        for scan_type in self.scan_types:
            dicom_dir = os.path.join(subject_path, scan_type)
            if os.path.exists(dicom_dir):
                dicom_features = self.process_dicom_directory(dicom_dir)
                if 'PatientID' not in dicom_features:
                    dicom_features["SubjectID"] = subject_id
                dicom_features["ScanType"] = scan_type
                subject_results.append(dicom_features)
        
        return subject_results
    
    def process_all_subjects_parallel(self) -> dict:
        """
        Process all subjects in parallel using multiprocessing.

        Parameters:
            root_directory (str): Path to the root directory containing subject folders.
            num_workers (int): Number of parallel processes to use.

        Returns:
            pandas.DataFrame: DataFrame containing extracted features from all subjects.
        """
        subjects = [
            os.path.join(self.root_directory, subdir)
            for subdir in os.listdir(self.root_directory)
            if os.path.isdir(os.path.join(self.root_directory, subdir))
        ]
        
        # Create a pool of workers for subject processing
        with multiprocessing.Pool(processes=self.num_workers) as pool:
            results = list(tqdm(pool.imap(self.process_subject, subjects), total=len(subjects), desc="Processing Subjects"))
        
        # Create scan-type dictionary 
        scan_types_dict = {scan_type: [] for scan_type in self.scan_types}
        for subject_results in results:
            for scan_df in subject_results:
                scan_type = scan_df['ScanType'].unique()[0]
                scan_types_dict[scan_type].append(scan_df)
        
        return {scan_type: pd.concat(scan_types_dict[scan_type]) for scan_type in scan_types_dict}
    
if __name__ == "__main__":
    from brain_tumor_segmentation.config import BRATS_2021_DICOMDIR
    root_dir = os.path.join(BRATS_2021_DICOMDIR, 'IvyGAP') 
    processor = DICOMProcessor(root_dir)
    processed_data = processor.process_all_subjects_parallel()
