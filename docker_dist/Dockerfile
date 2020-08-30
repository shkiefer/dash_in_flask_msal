FROM continuumio/miniconda3
ARG conda_env_fn
ARG conda_env
ARG port

WORKDIR /app_dir

# Create the environment:
COPY $conda_env_fn ./
COPY app ./app/
#COPY migrations/ ./migrations/
COPY docker_dist/wsgi.py ./
COPY docker_dist/boot.sh ./
COPY config.py ./

RUN conda env create -f $conda_env_fn
RUN echo "source activate $conda_env" > ~/.bashrc
ENV PATH /opt/conda/envs/$conda_env/bin:$PATH

EXPOSE $port

# fix line endings and allow to run as executable
RUN sed -i 's/\r$//' boot.sh  && \
        chmod +x boot.sh

ENTRYPOINT []
