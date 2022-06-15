FROM selenium/standalone-chrome:98.0
USER root

ENV PYENV_ROOT="/home/.pyenv"
ENV PATH="$PYENV_ROOT/shims:$PYENV_ROOT/bin:$PATH"

RUN apt-get update \
 && apt-get install -y --no-install-recommends make build-essential libssl-dev zlib1g-dev \
    libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm libncurses5-dev xz-utils tk-dev \
    libxml2-dev libxmlsec1-dev libffi-dev liblzma-dev libpq-dev \
    git

RUN git clone --depth=1 https://github.com/pyenv/pyenv.git $PYENV_ROOT \
 && pyenv install 3.8.12 \
 && pyenv global 3.8.12

COPY requirements.txt requirements.txt
RUN pip install --disable-pip-version-check --no-cache-dir -r requirements.txt \
 && pip install --disable-pip-version-check --no-cache-dir jupyterlab

RUN echo 'alias l="ls -lA --color --group-directories-first"' >> ~/.bashrc \
 && echo 'export PS1="${debian_chroot:+($debian_chroot)}\$(date +%Hh%M) \[\033[01;32m\]\W\[\033[00m\] \$ "' >> ~/.bashrc

WORKDIR /app

ENTRYPOINT []
CMD ["bash"]
