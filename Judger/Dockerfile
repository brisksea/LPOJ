FROM swift:5.9-jammy
LABEL maintainer="linzecong"
ADD . ./Judger
WORKDIR /Judger

# Install system packages
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    python2.7 \
    python3 \
    python3-pip \
    default-mysql-client \
    default-libmysqlclient-dev \
    libatomic1 \
    libssl-dev \
    zlib1g-dev \
    pkg-config \
    net-tools \
    nano \
    iputils-ping \
    time \
    cmake \
    openjdk-11-jdk \
    libseccomp-dev \
    build-essential \
    locales && \
    rm -rf /var/lib/apt/lists/*

# Configure UTF-8 locale for Chinese character support
RUN echo "en_US.UTF-8 UTF-8" > /etc/locale.gen && \
    echo "zh_CN.UTF-8 UTF-8" >> /etc/locale.gen && \
    locale-gen && \
    update-locale LANG=en_US.UTF-8

# Set environment variables for UTF-8 support
ENV LANG=en_US.UTF-8 \
    LC_ALL=en_US.UTF-8 \
    PYTHONIOENCODING=utf-8

# Setup Python 2.7 compatibility (if still needed)
RUN if [ -d /usr/lib/python2.7/site-packages ]; then \
        mv /usr/lib/python2.7/site-packages /usr/lib/python2.7/dist-packages && \
        ln -s dist-packages /usr/lib/python2.7/site-packages; \
    fi

# Install Python dependencies
RUN pip3 install --no-cache-dir paramiko==3.4.0 requests==2.31.0
RUN pip3 install --no-cache-dir mysqlclient

# Build judger core
RUN mkdir -p build && \
    cd build && \
    cmake /Judger && \
    make && \
    make install && \
    cd /Judger/JudgerCore && \
    python3 setup.py install

CMD ["python3", "main.py"]