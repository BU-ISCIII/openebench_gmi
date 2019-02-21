# Choose any base image you prefer, like bioconda, ubuntu, alpine, etc..
# or using a multistage deployment
FROM centos:latest

# Use a single LABEL (multiple ones are discouraged because each one creates a new layer)
LABEL	description="Sample ids extractor" vendor="ISCIII" version="0.1" maintainer="Sara Monzon <smonzon@isciii.es>"

COPY ./scif_app_recipes/* /opt/
COPY ./containers/getQueryIds//getLeavesFromNewick.py /opt/

# First, install all the dependencies needed by the results checking procedure
RUN echo "Install basic development tools" && \
    yum -y groupinstall "Development Tools" && \
    yum -y update && yum -y install wget curl && \
    echo "Install python2.7 setuptools and pip" && \
    yum -y install python-setuptools && \
    easy_install pip && \
    echo "Installing SCI-F" && \
    pip install scif ipython


# Now, we get the validation program in some way (copying, git clone, etc...)
# which should also write the results in the canonical format expected by the
# community metrics docker instances.
# The return value tells whether the validation and the translation to
# the canonical format whether worked or failed

RUN	echo "Installing checkTreeFormat script" && \
         scif install /opt/checkTreeFormat_v1.0_centos7.scif

ENTRYPOINT	["/opt/docker-entrypoint.sh"]
CMD [checkTreeFormat.py]
