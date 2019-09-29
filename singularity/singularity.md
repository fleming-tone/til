# singularityとは
- dockerのようなコンテナシステム自分で環境構築して、サクッと実行環境を作ること
- GPUにも対応してるのでdeeplearningもできるよくん
- sudo権限がいらないから、何でも感でもroot権限にするdockerよりまし
# 実際にやってみよう
## インストール
- 基本は、[singularityのホームページ](https://sylabs.io/guides/3.4/user-guide/quick_start.html)にそってやる。(version3.4)
- まずは必要ツールからinstall
```bash
$ sudo apt-get update && sudo apt-get install -y \
    build-essential \
    libssl-dev \
    uuid-dev \
    libgpgme11-dev \
    squashfs-tools \
    libseccomp-dev \
    wget \
    pkg-config \
    git
```
- GO環境が必要なのでinstall
```bash
$ export VERSION=1.12 OS=linux ARCH=amd64 && \  # Replace the values as needed
  wget https://dl.google.com/go/go$VERSION.$OS-$ARCH.tar.gz && \ # Downloads the required Go package
  sudo tar -C /usr/local -xzvf go$VERSION.$OS-$ARCH.tar.gz && \ # Extracts the archive
  rm go$VERSION.$OS-$ARCH.tar.gz    # Deletes the ``tar`` file
```
- 環境変数設定
```bash
$ echo 'export PATH=/usr/local/go/bin:$PATH' >> ~/.bashrc && \
  source ~/.bashrc
```
- singularityをgitclone
```bash
$ export VERSION=3.4.0 && # adjust this as necessary \
    wget https://github.com/sylabs/singularity/releases/download/v${VERSION}/singularity-${VERSION}.tar.gz && \
    tar -xzf singularity-${VERSION}.tar.gz && \
    cd singularity
```
- make!
```bash
$ ./mconfig && \
    make -C builddir && \
    sudo make -C builddir install
```
`注意`
- とあるサイトによると公式に記載のaptに足りないものがあるらしい！！
- 以下のエラーメッセージがでたら注意
- [Singularityのインストールと実行をしてみた](https://qiita.com/Nahuel/items/6c0fac8176340d749bc7)
```bash
unable to find the cryptsetup program, is the package cryptsetup-bin installed?

$ sudo apt install cryptsetup-bin
```
## 実際に環境作ってみる
- 手順は以下のよう
1. [dockerhub](https://hub.docker.com/)か[singularityのlibrary](https://cloud.sylabs.io/library)からいい感じのベース環境を取ってくる
- コンテナの効率的な作り方は[こちら](https://qiita.com/pottava/items/452bf80e334bc1fee69a)から
2. それに追加でなんか必要ならpipとかaptで必要ライブラリ追加
3. 試しに実行してプログラム動けばOK
- まずここではdefファイルの書き方のあとにsandboxを説明する
```Dockerfile
#ここでベース環境指定
#libraryはsingularityのライブラリ
#dockerはdockerhub
Bootstrap: library or docker
#どっから取ってきたねんを記述
From: ubuntu:18.04

%setup
    touch /file1
    touch ${SINGULARITY_ROOTFS}/file2

%files
    /file1
    /file1 /opt

%environment
    export LISTEN_PORT=12345
    export LC_ALL=C

%post
    apt-get update && apt-get install -y netcat
    NOW=`date`
    echo "export NOW=\"${NOW}\"" >> $SINGULARITY_ENVIRONMENT

%runscript
    echo "Container was created $NOW"
    echo "Arguments received: $*"
    exec echo "$@"

%startscript
    nc -lp $LISTEN_PORT

%test
    grep -q NAME=\"Ubuntu\" /etc/os-release
    if [ $? -eq 0 ]; then
        echo "Container base is Ubuntu as expected."
    else
        echo "Container base is not Ubuntu."
    fi

%labels
    Author d@sylabs.io
    Version v0.0.1

%help
    This is a demo container used to illustrate a def file that uses all
    supported sections.
```


