# pythonの3.8.0をベースにする
FROM python:3.8.0

# linuxの環境設定
RUN apt-get update \
    && apt-get upgrade -y \
    # imageのサイズを小さくするためにキャッシュ削除
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* \
    # pipのアップデート
    && pip install --upgrade pip

# 作業するディレクトリを変更
WORKDIR /home/
COPY requirements.txt ${PWD}

# pythonのパッケージをインストール
RUN pip install -r ./requirements.txt

# dataディレクトリを作って、そこにdataをコピーする。
RUN mkdir /home/data
WORKDIR /home/data
COPY ./data ${PWD}

# デフォルトの最初の作業ディレクトリを指定
WORKDIR /home






















