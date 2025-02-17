# Dataset Name

Brain Tumor Segmentation Dataset - BraTS2021 Challenge

| Name        | BraTS2021 |
|------------|-------------------------------|
| About      | Brain Tumor Segmentation Task - BraTS2021 Challenge |
| Title      | BraTS2021 - Brain Tumor Segmentation Challenge |
| Path       | `/data/raw/PKG-RSNA-ASNR-MICCAI-BraTS-2021/RSNA-ASNR-MICCAI-BraTS-2021` |
| Split(s)   | `dataset_*_v1.json` |
| Version    | v1 |


## Dataset Description

This dataset includes brain MRI scans of adult brain glioma patients, comprising of 4 structural modalities (i.e., T1, T1c, T2, T2-FLAIR) and associated manually generated ground truth labels for each tumor sub-region (enhancement, necrosis, edema), as well as their MGMT promoter methylation status. These scans are a collection of data from existing TCIA collections, but also cases provided by individual institutions and willing to share with a cc-by license.

## Parent Sources

- [Cancer Imaging Archive](https://www.cancerimagingarchive.net/analysis-result/rsna-asnr-miccai-brats-2021/)
- [BraTS 2021 Challenge](https://www.synapse.org/Synapse:syn25829067/wiki/610863)

## Reference

Manuscripts which have to be cited (along side flagship manuscript) include:
[1] U.Baid, et al., The RSNA-ASNR-MICCAI BraTS 2021 Benchmark on Brain Tumor Segmentation and Radiogenomic Classification, arXiv:2107.02314, 2021.

[2] B. H. Menze, A. Jakab, S. Bauer, J. Kalpathy-Cramer, K. Farahani, J. Kirby, et al. "The Multimodal Brain Tumor Image Segmentation Benchmark (BRATS)", IEEE Transactions on Medical Imaging 34(10), 1993-2024 (2015) DOI: 10.1109/TMI.2014.2377694

[3] S. Bakas, H. Akbari, A. Sotiras, M. Bilello, M. Rozycki, J.S. Kirby, et al., "Advancing The Cancer Genome Atlas glioma MRI collections with expert segmentation labels and radiomic features", Nature Scientific Data, 4:170117 (2017) DOI: 10.1038/sdata.2017.117

More information on the Data Usage Agreemnet and Citations can be found on [THIS](https://www.synapse.org/Synapse:syn25829067/wiki/626944) page.

## Known Issues

TCIA dataset:
- DICOM files are available for only 560 participants
- NIfTI files are available for ALL ~1250 participants
- Some participants do not possess all 4x image modalities
- NIfTI files are corrupted, specifically, in a NIfTI (Neuroimaging Informatics Technology Initiative) file, srow_x, srow_y, and srow_z are part of the affine transformation matrix, which defines the relationship between voxel coordinates (index-based) and real-world coordinates (scanner space).This means that the sform matrix (which describes the spatial orientation of the image) is effectively undefined or meaningless. Possible Causes:
    - Corrupt or improperly converted NIfTI file:
        -If the software generating the NIfTI file didn't properly set spatial information, it might default to zeros.
    - The image has no meaningful spatial orientation:
        - If the file was created from raw data without proper spatial metadata.
    - Conversion issues (DICOM → NIfTI):
        - Some DICOM to NIfTI conversion tools may fail to propagate the correct transformation matrix.
        - Some conversion tools require extra flags to preserve spatial information.
    - The file lacks real-world coordinate information:
        - Some NIfTI files only store voxel indices rather than real-world positioning.