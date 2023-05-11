
# Table of Contents

1.  [Purpose](#org62caa6b)
2.  [Instructor container](#org7e7f99f)
    1.  [Customization](#orgf151814)
        1.  [`instructor-container/nbgrader_config.py`](#orgc93c15a)
        2.  [`instructor-container/notebook.py`](#orgcb48782)
        3.  [`instructor-container/remove_test_from_feedback.py`](#orgab0d55e)
        4.  [`instructor-container/Dockerfile`](#org87fa639)
    2.  [Creating the container image](#org9949d2c)
    3.  [Running the container](#org3759423)
3.  [Student container](#org5ea856c)
    1.  [`student-container/Dockerfile`](#org39883d0)
4.  [Sample notebook](#org6ca7ded)



<a id="org62caa6b"></a>

# Purpose

This project contains all the files requiered to build:

-   a container image for the instructor with Jupyter notebooks, a Java Kernel and NBGrader to create assignments
-   a container image for the students with Jupyter notebooks and a Java Kernel to do the assignments.

Students can run the container inside a small virtual machine (with Alpine Linux) or remotely via JupyterHub:


<a id="org7e7f99f"></a>

# Instructor container


<a id="orgf151814"></a>

## Customization


<a id="orgc93c15a"></a>

### `instructor-container/nbgrader_config.py`

```
c = get_config()
c.CourseDirectory.course_id = "Tareas"
c.CourseDirectory.root="/home/jovyan/Tareas"

# This is the folder where the assigments will be stored to deliver via jupyterhub
c.Exchange.root = "/srv/nbgrader/exchange"

c.ClearSolutions.begin_solution_delimeter = "BSOL"
c.ClearSolutions.end_solution_delimeter = "ESOL"

# Short names for BEGIN SOLUTION and for BEGIN HIDDEN TESTS
c.ClearHiddenTests.begin_test_delimeter = "BTEST"
c.ClearHiddenTests.end_test_delimeter = "ETEST"
```

Where it is specified:

-   That all the notebooks will be created under a folder named `Tareas` and will be located under `/home/jovyan`.
-   The folder where the assignments will be deployed by nbgrader is `/srv/nbgrader/exchange`.
-   The instructor will use `//BSOL` and `//ESOL` to write the solution. All the code that is between those comments will be removed when nbgrader generates the student version of the assigments.
-   Test that are between `//BTEST` and `//ETEST` will not be included in the student version.

You can adapt all these values to your needs before creating the container image. **If you change the CourseDirectory values you will have to adapt that accordingly in the Dockerfile and in the python file remove_test_from_feedback.py**.


<a id="orgcb48782"></a>

### `instructor-container/notebook.py`

```
{
  "load_extensions": {
    "hide_input/main": true
  },
  "CodeCell": {
    "cm_config": {
      "indentUnit": 3
    }
  }
}
```


Where it is specified the indentation (3 spaces in this example).

<a id="orgab0d55e"></a>

### `instructor-container/remove_test_from_feedback.py`

This file is used to remove the solution from the feedback (according to the delimiters defined in `container/nbgrader_config.py`:

```
#!/usr/bin/env python3
import sys
import re

START = '<span class="c1">// BTEST</span>'
END='<span class="c1">// ETEST</span>'
html_path = sys.argv[1].rstrip()
with open(html_path, 'r') as content_file:
    content = content_file.read()

def replaceTextBetween(originalText, delimeterA, delimterB, replacementText):
    index_from = 0
    index_to = len(originalText)
    if delimeterA in originalText:
        index_from = originalText.index(delimeterA)

    if delimterB in originalText:
        index_to = originalText.index(delimterB) + len(delimterB)

    return originalText[0:index_from] + originalText[index_to:]

while START in content:
    content = replaceTextBetween(content, START, END, '')
with open(html_path, 'w+') as stream:
    stream.write(content)
```


<a id="org87fa639"></a>

### `instructor-container/Dockerfile`

```
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
```


From the base image with a Java kernel, all the depedendencies are installed and the configurations files are copied to the image.

Finally nbgrader is configured to use the folder `Tareas` (you can change that folder, but remember to be consistent across all provided files).

<a id="org9949d2c"></a>

## Creating the container image

```
cd instructor-container
# This instruction assumes that you have docker in your machine
docker build . -t jupyter-java-nbgrader:1.0
```


<a id="org3759423"></a>

## Running the container

```
# This is the folder where the assigments and student versions will be in
# your file system. Adapt to your needs
courseDir=/home/instructor/course/

# Directory with the assignments
dirTareas=$courseDir/Tareas
mkdir -p $dirTareas

# Directory where nbgrader will export the student version of the assignments
dirExchange=$courseDir/exchange
mkdir -p $dirExchange

# Running the container the first time
docker run --name jnb -v $dirExchange:/srv/nbgrader/exchange -v $dirTareas:/home/jovyan/Tareas -p 8888:8888 jupyter-java-nbgrader:1.0
# Check the URL with the token and open your browser

# Stopping the container
docker stop jnb

# Restating the container
docker start jnb

# Check the logs to see the URL and the token
docker logs jnb
```


<a id="org5ea856c"></a>

# Student container


<a id="org39883d0"></a>

## `student-container/Dockerfile`

```
FROM  jupyter/base-notebook:2023-05-08

USER root
# Install dependencies
RUN apt-get update && \
    apt-get install -y software-properties-common unzip git

# Install Zulu OpenJdk 11 (customize to your needs)
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

# This is the working directory for students (customize to your needs)
RUN mkdir -p /home/jovyan/work && \
    chown -R jovyan:users /home/jovyan/work

# Set user back to priviledged user.
USER $NB_USER
ENV JAVA_HOME=/usr/lib/jvm/zulu-11-amd64/
WORKDIR /home/jovyan/work
```

<a id="org6ca7ded"></a>

# Sample notebook

There is a folder with an example of the student version (generated by nbgrader) of an assignment about Java Interfaces (this sample notebook is in Spanish). This notebook includes some test, so students can check whether their solutions are correct.
