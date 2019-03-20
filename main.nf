#!/usr/bin/env nextflow

/*
===============================================================================================================
                  O P E N E B E N C H  W O R K F L O W   O U T B R E A K  D E T E C T I O N
===============================================================================================================
 #### Homepage / Documentation
 https://github.com/BU-ISCIII/openebench_gmi
 @#### Authors
 Sara Monzon <smonzon@isciii.es>
----------------------------------------------------------------------------------------
----------------------------------------------------------------------------------------
Pipeline overview:
 - 1. : Validation & Check Results
    - 1.1. : GetIDsFromNewick
    - 1.2. : CheckNewickFormat
 - 2. : Metrics
 	- 2.1: Robin-Foulds calculation between participant result and golden dataset.
 	- 2.2: Metrics consolidation.
 - 3. : Visualization

 ----------------------------------------------------------------------------------------
*/

def helpMessage() {
    log.info"""
    =========================================
     BU-ISCIII/openebench_gmi : OpenEBench pipeline for Outbreak detection challenge v${version}
    =========================================
    Usage:

    The typical command for running the pipeline is as follows:

    nextflow run BU-ISCIII/openebench_gmi --tree_test {test.newick.file} --golden_newick {golden.newick.file} --even_id {event.id}

    Mandatory arguments:
      --tree_test                   Path to input data (must be surrounded with quotes).
      --golden_newick               Path to reference data. Golden dataset.
      --event_id                    Event identifier.
      --tree_format					Format tree ["nexus","newick"].

    Other options:
      --outdir                      The output directory where the results will be saved
    """.stripIndent()
}

/*
 * SET UP CONFIGURATION VARIABLES
 */

// Pipeline version
version = '1.0'

// Show help message
params.help = false
if (params.help){
    helpMessage()
    exit 0
}

/*
* DEFAULT AND CUSTOM VALUE FOR CONFIGURABLE VARIABLES
*/

if(params.tree_test){
	tree_test_file = file(params.tree_test)
	if (!tree_test_file.exists()) exit 1, "Input Newick file not found: ${params.tree_test}"
}

if(params.golden_newick){
	golden_newick_file = file(params.golden_newick)
	if (!golden_newick_file.exists()) exit 1, "Input Golden newick file not found: ${params.golden_newick}"
}

params.tree_format = "newick"
if ( ! (params.tree_format =~ /newick|nexus/) ) {
	exit 1, 'Please provide a valid --tree_format option [newick,nexus]'
}

/*
* CHECK MANDATORY INPUTS
*/

params.golden_newick = false
if(! params.golden_newick){
	exit 1, "Missing golden newick file : $params.golden_newick. Specify path with --golden_newick"
}

params.tree_test = false
if(! params.tree_test){
	exit 1, "Missing tree test file : $params.tree_test. Specify path with --tree_test"
}

params.event_id = false
if(! params.event_id){
	exit 1, "Missing Event identifier : $params.event_id. Specify path with --event_id"
}


/*
* HEADER LOG INFO
*/
log.info "========================================="
log.info " BU-ISCIII/openebench_gmi : OpenEBench pipeline for Outbreak detection challenge v${version}"
log.info "========================================="
def summary = [:]
summary['Test tree input']   = params.tree_test
summary['Golden Newick input'] = params.golden_newick
summary['Event ID']            = params.event_id
if(workflow.revision) summary['Pipeline Release'] = workflow.revision
summary['Current home']        = "$HOME"
summary['Current user']        = "$USER"
summary['Current path']        = "$PWD"
summary['Working dir']         = workflow.workDir
summary['Output dir']          = params.outdir
summary['Script dir']          = workflow.projectDir
summary['Config Profile'] = workflow.profile
log.info summary.collect { k,v -> "${k.padRight(21)}: $v" }.join("\n")
log.info "===================================="


// Check that Nextflow version is up to date enough
// try / throw / catch works for NF versions < 0.25 when this was implemented
nf_required_version = '0.25.0'
try {
    if( ! nextflow.version.matches(">= $nf_required_version") ){
        throw GroovyException('Nextflow version too old')
    }
} catch (all) {
    log.error "====================================================\n" +
              "  Nextflow version $nf_required_version required! You are running v$workflow.nextflow.version.\n" +
              "  Pipeline execution will continue, but things may break.\n" +
              "  Please run `nextflow self-update` to update Nextflow.\n" +
              "============================================================"
}

/*
===============================
PIPELINE
===============================
*/


/*
* Assuring the preconditions (in this case, the docker images) are in place
*/
process dockerPreconditions {
  //tag
  publishDir path: "${params.outdir}", mode: 'copy', overwrite: true

  input:

  output:
    file docker_image_dependency

  """
  echo "$baseDir"
  docker build -t openebench_gmi/sample-checkresults:latest -f $baseDir/containers/checkFormat/Dockerfile $baseDir
  docker build -t openebench_gmi/sample-getqueryids:latest -f $baseDir/containers/getQueryIds/Dockerfile $baseDir
  #docker build -t openebench_gmi/sample-getresultsids:latest -f $baseDir/containers/getResultsIds/Dockerfile $baseDir
  docker build -t openebench_gmi/sample-robinsonfoulds:latest -f $baseDir/containers/robinsonFouldsMetric/Dockerfile $baseDir
  #docker build -t openebench_gmi/sample-consolidate:latest -f $baseDir/containers/consolidateMetrics/Dockerfile $baseDir
  touch docker_image_dependency
  """

}


/*
* The instance generated from this docker file has to check the syntax of the submitted results.
*/
process checkResults {

  container 'openebench_gmi/sample-checkresults'

  publishDir path: "${params.outdir}", mode: 'copy', overwrite: true

  input:
  file tree from tree_test_file
  file image_dependency from docker_image_dependency

  output:
  file "tree.nwk" into canonical_getresultsids,canonical_robinsonfoulds

  """
  checkTreeFormat.py --tree_file ${tree} --tree_format ${params.tree_format}
  """

}

/*
* The instance generated from this docker file knows how to extract query ids from the query.
*/
process getQueryIds {

  container 'openebench_gmi/sample-getqueryids'

  publishDir path: "${params.outdir}", mode: 'copy', overwrite: true

  input:
  file tree from tree_test_file
  file image_dependency from docker_image_dependency


  output:
  file "*.json" into query_ids_json

  """
  getLeavesFromNewick.py --event_id ${params.event_id} --tree_file $tree --tree_format ${params.tree_format} --output queryids.json
  """

}

/*
* The instance generated from this docker file knows how to extract results ids from the results canonical formats.
*/
process getResultsIds {

  container 'openebench_gmi/sample-getqueryids'

  publishDir path: "${params.outdir}", mode: 'copy', overwrite: true

  input:
  file tree from canonical_getresultsids
  file image_dependency from docker_image_dependency

  output:
  file "*.json" into result_ids_json

  """
  getLeavesFromNewick.py --event_id ${params.event_id} --tree_file $tree --output resultsids.json
  """

}

/*
* The instance generated from this docker file compute metrics based on the number of lines and words.
*/
process RobinsonFouldsMetrics {

  container 'openebench_gmi/sample-robinsonfoulds'

  publishDir path: "${params.outdir}", mode: 'copy', overwrite: true

  input:
  file tree1 from canonical_robinsonfoulds
  file tree2 from golden_newick_file
  file docker_image_dependency

  output:
  file "*.json" into metrics_robinsonfoulds_json

  """
  calculateRobinsonFouldsMetric.py --tree_file1 $tree1 --tree_file2 $tree2
  """

}

///*
//* The instance generated from this docker file computed metrics based on the results of the previous dockers.
//*/
//process ConsolidateMetrics {
//
//  container 'openebench_gmi/sample-consolidate'
//
//  publishDir 'nextflow_working_directory', mode: 'copy', overwrite: true
//
//  input:
//  file metrics_linemetrics_json
//  file metrics_wordmetrics_json
//  file docker_image_dependency
//
//  output:
//  file metrics_consolidated_json
//
//  """
//  metricsConsolidator.sh . unusedparam metrics_consolidated_json
//  """
//
//}
//
