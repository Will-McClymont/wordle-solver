FROM ubuntu

RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    git

RUN mkdir -p wordle-solver \
    && git clone https://github.com/Will-McClymont/wordle-solver/

RUN pip install -r wordle-solver/requirements.txt
