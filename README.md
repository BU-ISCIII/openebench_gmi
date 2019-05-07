[![License: GPL v3](https://img.shields.io/badge/License-GPL%20v3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0) [![Scif](https://img.shields.io/badge/Filesystem-Scientific-brightgreen.svg)](https://sci-f.github.io)

# Nextflow pipeline using containers for an Outbreak detection challenge using OpenEbench platform

This repository intends to be a nextflow + container implementation of OpenEbench workflow for an Outbreak detection challenge. 
## How to use it

```Bash
git clone https://github.com/BU-ISCIII/openebench_gmi.git
cd openebench_gmi.git
git submodule init
git submodule update
nextflow run main.nf -profile docker 
```
Parameters available:
```Bash
nextflow run main.nf --help
```

```
Usage:
nextflow run BU-ISCIII/openebench_gmi --tree_test {test.newick.file} --golden_newick {golden.newick.file} --even_id {event.id} --tree_format ["nexus","newick"] --outdir {path/name.output}

Mandatory arguments:
  --tree_test                 Path to input data (must be surrounded with quotes).
  --golden_newick             Path to reference data. Golden dataset.
  --event_id                  Event identifier.
  --tree_format               Format tree ["nexus","newick"].

Other options:
  --outdir                    The output directory where the results will be saved
```


## Datasets
First of all, needed datasets have been collected in: [datasets folder](datasets)

1. **Input dataset:** fastq input data obtained from [GMI WGS standards and benchmarks repository](https://github.com/globalmicrobialidentifier-WG3/datasets). [Here](datasets/inputDataset/Readme.me) you can find instructions for download.
2. **Gold standard dataset:** confirmed phylogeny for the outbreak being investigated.
3. **Input dataset ids:** input dataset ids in .txt and .json format.
4. **Test dataset:** a test tree for comparing with gold standard result. In this case just the same golden dataset. Robinson-Foulds metrics must be 0.

## Nextflow pipeline and containers
Second, a pipeline has been developed which is splitted in three steps following OpenEbench specifications following this [repo](https://github.com/inab/opeb-submission) as an example:

### Nextflow processes
1. **Validation and data preprocessing:**
   1. *Check results format:* 
      - Tree input: User input tree format is validated, nexus and newick formats are allowed being newick the canonical format. If format validated, a tree is outputted in the canonical format (.nwk).
      - VCF input:
    
   2. *Get query ids:* 
      - Tree input: ids are extracted for user input tree in newick or nexus format. IDs are writed in: queryids.json 
    
   3. *Get result ids:* 
      - Tree input: ids are extracted from canonical tree format. IDs are writed in resultsids.json

2. **Metrics:**
   1. *Robinson-Foulds metric calculation:* Robinson-Foulds test is performed between user tree and gold standard tree in order to compare its topologies. Result value is writted to robinsonfoulds.json file.
  
3. **Data visualization and consolidation:**
  **TODO**

### Containers info

Each step runs in its own container. Containers are built using a Dockerfile recipe which makes use of [SCI-F](https://sci-f.github.io/) recipes for software installation. All scif recipes are available in [scif_app_recipes repository](https://github.com/BU-ISCIII/scif_app_recipes). Singularity recipes are also provided (Not yet adapted in nextflow pipeline).
