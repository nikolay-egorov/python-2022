FROM python:3.9
MAINTAINER Nikolay Egorov

#RUN apt-get update && apt-get install -y texlive-latex-base texlive-fonts-recommended texlive-fonts-extra texlive-latex-extra
RUN apt-get update && apt-get install -y texlive-full texlive-fonts-recommended # full for babel-russian
RUN pip install --upgrade pip
RUN apt update
RUN apt-get -y update
RUN apt-get install -y graphviz
RUN pip install matplotlib==3.5.1 pydot==1.4.2 networkx==2.6.3 nikolay-egorov-python-2022-hw1==0.1.4