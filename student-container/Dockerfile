FROM  jupyter/base-notebook:2023-05-08

USER root
# Install dependencies
RUN apt-get update && \
    apt-get install -y software-properties-common unzip git curl


# Install Zulu OpenJdk 17 (LTS)
RUN curl -s https://repos.azul.com/azul-repo.key | sudo gpg --dearmor -o /usr/share/keyrings/azul.gpg && \
    echo "deb [signed-by=/usr/share/keyrings/azul.gpg] https://repos.azul.com/zulu/deb stable main" | sudo tee /etc/apt/sources.list.d/zulu.list && \
    apt-get update && \
    apt-get -y install zulu17-jdk

RUN wget https://github.com/SpencerPark/IJava/releases/download/v1.3.0/ijava-1.3.0.zip -O ijava-kernel.zip
RUN unzip ijava-kernel.zip -d ijava-kernel \
  && cd ijava-kernel \
  && python3 install.py --sys-prefix

# Cleanup
RUN rm ijava-kernel.zip

RUN mkdir -p /home/jovyan/work && \
    chown -R jovyan:users /home/jovyan/work 

# Set user back to default user.
USER $NB_USER
WORKDIR /home/jovyan/work

