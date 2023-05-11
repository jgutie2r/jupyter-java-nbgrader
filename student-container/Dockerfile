FROM  jupyter/base-notebook:2022-10-17

USER root
# Install dependencies
RUN apt-get update && \
    apt-get install -y software-properties-common unzip git

# Install Zulu OpenJdk 11 (LTS)
RUN apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys 0xB1998361219BD9C9 \
  && apt-add-repository 'deb http://repos.azulsystems.com/ubuntu stable main' \
  && apt install -y zulu-11 \
  && rm -rf /var/lib/apt/lists/

# Unpack and install the kernel
RUN wget https://github.com/SpencerPark/IJava/releases/download/v1.3.0/ijava-1.3.0.zip -O ijava-kernel.zip
RUN unzip ijava-kernel.zip -d ijava-kernel \
  && cd ijava-kernel \
  && python3 install.py --sys-prefix

# Cleanup
RUN rm ijava-kernel.zip

RUN mkdir -p /home/jovyan/.jupyter/custom
COPY custom.css /home/jovyan/.jupyter/custom/cuscom.css
RUN mkdir -p /home/jovyan/work && \
    chown -R jovyan:users /home/jovyan/work && \
    chown -R jovyan:users /home/jovyan/.jupyter/custom

# Set user back to priviledged user.
USER $NB_USER
ENV JAVA_HOME=/usr/lib/jvm/zulu-11-amd64/
WORKDIR /home/jovyan/work
