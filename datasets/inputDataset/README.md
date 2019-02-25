## Info

We are going to use as input Dataset a simulated benchmark dataset with known phylogeny and SNP locations: data generated using TreeToReads. 250bp, 40X coverage, 150 var sites, S.Bareilly GCA_000439415.1 anchor genome. This dataset has been developed by GMI WG 3, you can find more information in this [repo](https://github.com/globalmicrobialidentifier-WG3/datasets)


## Download input Dataset
```Bash
export PATH=$PATH:${PWD}/scripts
GenFSGopher.pl -o data --layout cfsan ./Salmonella_enterica_1203NYJAP-1.simulated.tsv
```

## Dependencies
1. edirect
2. sra-toolkit, built from source: https://github.com/ncbi/sra-tools/wiki/Building-and-Installing-from-Source
3. Perl 5.12.0
4. Make
5. wget
6. sha256sum

### References
Timme, Ruth E., et al. "Benchmark datasets for phylogenomic pipeline validation, applications for foodborne pathogen surveillance." PeerJ 5 (2017): e3893.
