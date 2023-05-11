FROM docker.io/jbindinga/java-notebook:latest
USER root
RUN apt install -y libffi-dev
RUN pip install -U jupyter-client &&     pip install -U jupyter &&     pip install -U markupsafe &&     pip install -U nbformat &&     pip install -U traitlets

RUN pip install --ignore-installed nbgrader &&     jupyter nbextension install --sys-prefix --py nbgrader --overwrite &&     jupyter nbextension enable --sys-prefix --py nbgrader &&     jupyter serverextension enable --sys-prefix --py nbgrader

# Change uid and gid of jovyan to match my host uid and gid
RUN groupmod -g 1001 users && usermod -u 1001 -g 1001 jovyan

RUN mkdir -p /srv/nbgrader/exchange && chmod a+rw /srv/nbgrader/exchange && chown jovyan:users /srv/nbgrader/exchange

USER jovyan
COPY nbgrader_config.py /home/jovyan/.jupyter/
COPY edit.json /home/jovyan/.jupyter/nbconfig/
COPY remove_test_from_feedback.py /home/jovyan/.jupyter/remove_test_from_feedback.py
COPY notebook.json /home/jovyan/.jupyter/nbconfig/
RUN nbgrader quickstart Tareas
