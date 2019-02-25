[![License: GPL v3](https://img.shields.io/badge/License-GPL%20v3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)[![Scif](https://img.shields.io/badge/Filesystem-Scientific-brightgreen.svg)](https://sci-f.github.io)

# Nextflow pipeline using containers for a Outbreak detection challenge using OpenEbench platform

This repository intends to be a nextflow + container implementation of OpenEbench workflow for a Outbreak detection challenge. 


## Datasets
First of all, needed datasets have been colled in: [datasets folder](datasets)

1. Input dataset: fastq input data obtained from [GMI WGS standards and benchmarks repository](https://github.com/globalmicrobialidentifier-WG3/datasets). [Here](datasets/inputDataset/Readme.me) you can find instructions for download.
2. Golden dataset
3. Input dataset ids
4. Test dataset

## Nextflow pipeline and containers
Second a pipeline has been developed which is splitted in four steps following OpenEbench specifications:

1. Validation and data preprocessing: 
