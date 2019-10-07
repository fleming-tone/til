# googlecolabについて記述
- 少し前に書いた記事が発掘されたの挙げとこう！
- まぁそんな感じ
# googleCoLabって
- googleがやってる無料の計算システム（ただし制限あり）
    - ９０分ルールと１２時間ルールがあるらしい[参考リンク](https://qiita.com/tomo_makes/items/b3c60b10f7b25a0a5935#2-%E3%82%B7%E3%83%A3%E3%83%83%E3%83%88%E3%83%80%E3%82%A6%E3%83%B3%E3%81%BE%E3%81%A7%E3%81%AE%E6%AE%8B%E6%99%82%E9%96%93%E3%81%AF90%E5%88%86%E3%83%AB%E3%83%BC%E3%83%AB%E3%81%A812%E6%99%82%E9%96%93%E3%83%AB%E3%83%BC%E3%83%AB)
- 家にGPUマシンおけないよとかいう人は、お手軽に使えます。
- 記述法は、jupterNotebook形式です。
# 使い方
- 画面はこんなかんじ
![main](https://github.com/kapibarasyun/til/blob/image/googlecolab/main.png?raw=true)
- とりあえず、コードを書く場所に順番にコードを書いて行く感じ
- 基本コードはpython3&切り替えるとmarkdownでコメント~~もどき~~もかける
## ファイルのやり取りは？
- 直接ファイルをアップロードするかgoogledriveへアップロード
- まずは、かんたんな直接アップロード方法
1. メイン画面のところの黒丸のところクリック
![upload](https://github.com/kapibarasyun/til/blob/image/googlecolab/kokodayo.png?raw=true)
2. そこに直接ドラッグアンドドロップ
![upload](https://github.com/kapibarasyun/til/blob/image/googlecolab/drive.png?raw=true)

`注意`
Driveに置くとアップロードしたデータは消えないが普通にアップロードするとデータがログアウトするたび消えるので再度アップロードが必要
- googleDriveつなげ方

1.　以下のコードを実行
```bash 
from google.colab import drive
drive.mount('/content/drive')
```

2. ここでgoogledrive認証があるので認証を行う．認証コードをコピペして次実行

`注意`ここでも一旦ログアウトや長時間使わないと接続が切れますので，コードを実行し直して再度認証してください

## ディレクトリ移動方法＆apt&pipのやり方は
- 基本のpwdは以下にしめす場所
```bash
/content
#移動を行うときは
!cd /content/hogehoge
```
- !を頭につけることでコマンドが実行できます．
- ここでは試しにmecabの環境をつくる
- 参考サイト[ColaboratoryでMeCabを使えようにする。](https://qiita.com/pytry3g/items/897ae738b8fbd3ae7893)
```bash
!apt install aptitude
!aptitude install mecab libmecab-dev mecab-ipadic-utf8 git make curl xzutils
file -y
!pip install mecab-python3==0.7
```
`注意`ここでも長時間ログインしなかったり接続が切れると再度リセットです．もう一回**再生ボタン**みたいなのを押して実行し直してね
