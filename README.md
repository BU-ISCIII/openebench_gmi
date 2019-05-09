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
nextflow run BU-ISCIII/openebench_gmi --tree_test {test.newick.file} --goldstandard_dir {golden.folder.path} --assess_dir {assessment.path} --public_ref_dir {path.to.info.ref.dataset} --event_id {event.id}

Mandatory arguments:
  --tree_test                   Path to input data (must be surrounded with quotes).
  --goldstandard_dir            Path to reference data. Golden datasets.
  --public_ref_dir              Path where public dataset info is stored for validation.
  --assess_dir                  Path where benchmark data is stored.
  --event_id                    Event identifier.
  --participant_id              Participant identifier.
  --tree_format                 Format tree ["nexus","newick"].

Other options:
  --outdir                      The output directory where the results will be saved
```


## Datasets
First of all, needed datasets have been collected in: [datasets folder](datasets)

1. **Input dataset:** fastq input data obtained from [GMI WGS standards and benchmarks repository](https://github.com/globalmicrobialidentifier-WG3/datasets). [Here](datasets/inputDataset/Readme.me) you can find instructions for download.
2. **Gold standard dataset:** confirmed phylogeny for the outbreak being investigated.
3. **Input dataset ids:** input dataset ids in .txt and .json format.
4. **Test dataset:** a test tree for comparing with gold standard result. In this case just the same golden dataset. Robinson-Foulds metrics must be 0.
5. **benchmark_data**: path where benchmark results are stored.

## Nextflow pipeline and containers
Second, a pipeline has been developed which is splitted in three steps following OpenEbench specifications following this [repo](https://github.com/inab/opeb-submission) as an example:

### Nextflow processes
1. **Validation and data preprocessing:**
   1. *Check results format:* 
      - Tree input: User input tree format is validated, nexus and newick formats are allowed being newick the canonical format. If format validated, a tree is outputted in the canonical format (.nwk).
      - VCF input:
    
   2. *Get query ids:* 
      - Tree input: ids are extracted for user input tree in newick or nexus format. IDs are writed in: queryids.json 
    
   3. *Validate query ids:* 
      - Tree input: query ids are validated against ref input ids.

2. **Metrics:**
   1. *Precision/Recall calculation:* common (TP), source (FP) and ref(FN) edges are calculated in the comparison of ref and test tree topologies. Recall and precision are calculated using this values and stored in a json file called {participant_id}_snprecision.json.
   2. *Robinson-Foulds metric calculation:* Normalized Robinson-Foulds test is performed between user tree and every participant tree already analyzed and stored in the benchmark_data folder in order to compare their topologies. Result value is writted to participant_matrix.json file.
  
3. **Data visualization and consolidation:**
  1. Precision/Recall graph is created, classifying each participant inside a quartile.
  2. A all participant vs all participant heatmap is created usign normalized robinson-foulds matrix.

### Containers info

Each step runs in its own container. Containers are built using a Dockerfile recipe which makes use of [SCI-F](https://sci-f.github.io/) recipes for software installation. All scif recipes are available in [scif_app_recipes repository](https://github.com/BU-ISCIII/scif_app_recipes). Singularity recipes are also provided (Not yet adapted in nextflow pipeline).
