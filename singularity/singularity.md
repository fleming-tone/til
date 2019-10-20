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
#### 追加項目（2019/10/12)
- dockerコンテナの選び方というか助言
- 現在のサポートubuntuLTSは18.04なのでそちらを選んだほうが良い
- サポートしてないバーションだとpythonが古かったり、apt pipが古くてうまく更新でいないことがある。
- 各cudaバージョンで最新のubuntuを使ってるものを紹介
- すべてubuntuは18.04
- いまのところ18.04では、cuda9.2~10.1までしかない

|tags|cuda version|cudnn version|
|:----------------------------:|:-:|:-:|
|9.2-cudnn7-runtime-ubuntu18.04|9.2|7|
|10.0-cudnn7-runtime-ubuntu18.04|10.0|7|
|10.1-cudnn7-runtime-ubuntu18.04|10.1|7|

2. それに追加でなんか必要ならpipとかaptで必要ライブラリ追加
3. 試しに実行してプログラム動けばOK
- まずここではdefファイルの書き方のあとにsandboxを説明する
### .defから作る
- 最小構成の雛形はこんな感じ
```Dockerfile
#ここでベース環境指定
#libraryはsingularityのライブラリ
#dockerはdockerhub
Bootstrap: library or docker
#どっから取ってきたねんを記述
From: ubuntu:18.04
#インストールしたいものを記述
%post
    #apt
    apt update 
    apt -y upgrade
    apt -y install hogehoge
    #pip
    pip install hogehoge
#環境変数設定
%environment
    export LC_ALL=C
#誰が作ったのか記述する場所
%labels
    Author hogehoge
    Version v0.0.0
```
- 作った.defファイルはsudo権限で.sif(singulairty image file)に変換する
- コードは以下のよう
```bash
$ sudo singularity build hoge.sif hoge.def
```
### sandboxから作る
- sandboxとは開発環境を作るときにパッケージインストール（aptやpipを行いながら）開発を行うときに便利なシステム
- とりあえず以下のコマンド実行
```bash
sudo singularity build --sandbox ch_sandbox docker://chainer/chainer:latest-python3 # --sandboxオプションは-sと省略可
```
- このコマンドでは、dockerhubからchainerをサンドボックスとして読み出したもの
- カレントディレクトリにch_chainerが作られる
- ここからオプションが２つある
```bash 
$ singularity shell ch_sandbox #.sifファイルと同じ扱い
$ sudo singularity shell --writable ch_sandbox #書き換え可能
```
- writableの違い
  
|-writable|何もなし |
----|----|
|書き込みできる|読み込み専門|
|他のディレクトリマウントできない|.sifのようになる|
|apt pip install可能|pipのみインストール可能|
- 開発環境を思考錯誤したい人は使うといいが
- 今後のメンテナンス性を考えてdefにしておくことをおすすめする。
- sandboxもsifにできる。
```bash
$ sudo singularity build my_chainer.sif ch_sandbox
```
## 実行方法
- .sifまでできればあとは簡単
- 他の人に.sifだけ渡せば権限なくても使えます（dockerとの一番の違い）
```bash
#GPUを使ってshellを使うとき
$ singularity shell --nv  hogehoge.sif
#GPUを使って何かしらコマンドを動かすとき
$ singularity exec --nv hogehoge.sif nvidia-smi
```
- 基本マウントは、/homeがマウントされます。（めちゃ便利）
- --nvをつけることでGPU使用可です。
# 参考リンク
- 参考リンクくらい載せようぜってことで載せときます。
- [sylab-singularity](https://sylabs.io/singularity/)
- [検証用コンテナはDocker？いいえ、Singularityです。-quita](https://qiita.com/mkt3/items/b9f86f5ddf9eb0f43608)
- [Singularityのインストールと実行をしてみた-quita](https://qiita.com/Nahuel/items/6c0fac8176340d749bc7)
- [Singularity-HPC](https://www.hpc.co.jp/product/software/singularity/)
# 追加項目(2019/10/20)
- singularityコンテナともとｐｃとの環境依存について
    - あたりまえかもしれないが，同じｐｃにsingularityで入れたライブラリと同じものが入っているともとから入っているライブラリが使われる．
    - 例を挙げると，pytorchのライブラリをcondaやpipを使って追加したなら，singularity内で宣言したライブラリのバージョンは，conda&pipで入れたバージョンに依存します．

`ポイント`
singularityで特定のバージョンを使いたいなら，ベース環境はで，conda,pip,aptでライブラリを共存させないようにしましょう．

