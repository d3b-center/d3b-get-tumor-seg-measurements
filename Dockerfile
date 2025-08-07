FROM python:3.9.7-slim-buster

ENV FLYWHEEL="/flywheel/v0"
WORKDIR ${FLYWHEEL}

COPY run.py manifest.json README.md requirements.txt $FLYWHEEL/
COPY fw_gear_functions ${FLYWHEEL}/fw_gear_functions 

# Install main deps
RUN pip3 install -r requirements.txt

# Configure entrypoint
RUN chmod a+x $FLYWHEEL/run.py
ENTRYPOINT ["python","/flywheel/v0/run.py"]
