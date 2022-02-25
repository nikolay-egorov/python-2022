#docker build . -t me --tag latex-drawer
docker build . --tag latex-drawer
#docker run -t -i latex-drawer /bin/bash -c "python main.py"
docker run -t -i --mount type=bind,source="$(pwd)",target=/home/latex-drawer latex-drawer /bin/bash -c \
 "cd home/latex-drawer; python main.py"