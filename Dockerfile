FROM python:3.9.0-buster

RUN  apt-get update -y
RUN  apt-get install mc -y
RUN  pip install --upgrade pip && \
     pip install libscrc

RUN  mkdir -p /home/git/SetLineid
COPY . /home/git/SetLineid

#ENTRYPOINT python3

# line generator tests
CMD python3 /home/git/SetLineid/Test_SL.py

# run lines generator script.
#    Replace curly brackets parts with corresponding data.
# CMD python3 /home/git/SetLineid/SetLineid.py /opt/yarn --BCKP /opt/backup

