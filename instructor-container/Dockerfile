FROM  jupyter/base-notebook:2023-05-08

USER root
# Install dependencies
RUN apt-get update && \
    apt-get install -y software-properties-common unzip git


RUN apt-get install -y curl gnupg ca-certificates

# Install Zulu OpenJdk 17 (LTS)
RUN curl -s https://repos.azul.com/azul-repo.key | sudo gpg --dearmor -o /usr/share/keyrings/azul.gpg && \
    echo "deb [signed-by=/usr/share/keyrings/azul.gpg] https://repos.azul.com/zulu/deb stable main" | sudo tee /etc/apt/sources.list.d/zulu.list && \
    apt-get update && \
    apt-get -y install zulu17-jdk


# Unpack and install the kernel
RUN wget https://github.com/SpencerPark/IJava/releases/download/v1.3.0/ijava-1.3.0.zip -O ijava-kernel.zip
RUN unzip ijava-kernel.zip -d ijava-kernel \
  && cd ijava-kernel \
  && python3 install.py --sys-prefix

# Cleanup
RUN rm ijava-kernel.zip

# Create dirs and copy files
RUN mkdir -p /srv/nbgrader/exchange && chmod a+rw /srv/nbgrader/exchange && chown jovyan:users /srv/nbgrader/exchange

# Install LSP server
RUN  pip install jupyter_server && \
     pip install jupyter-lsp && \
     pip install jupyterlab-lsp && \
     pip install 'python-lsp-server[all]' 

# Install nbgrader
RUN pip install nbgrader && \
    jupyter labextension enable --level=system nbgrader && \
    jupyter server extension enable --system --py nbgrader

#RUN pip install --ignore-installed nbgrader && \
#    jupyter nbextension install --sys-prefix --py nbgrader --overwrite && \
#    jupyter nbextension enable --sys-prefix --py nbgrader && \
#    jupyter serverextension enable --sys-prefix --py nbgrader

USER jovyan

COPY nbgrader_config.py /home/jovyan/.jupyter/
COPY edit.json /home/jovyan/.jupyter/nbconfig/
COPY remove_test_from_feedback.py /home/jovyan/.jupyter/remove_test_from_feedback.py
COPY notebook.json /home/jovyan/.jupyter/nbconfig/
RUN nbgrader quickstart Tareas


