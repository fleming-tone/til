# pc初期化方法について
## ubuntuのライブブート
1. ubuntuのライブDVDorUSBを用意し，ubuntuを試すで起動
2. 起動したらterminalへ
## ディスクを調べ初期化
- terminalで以下のコマンドを実行
```bash 
$dmesg | grep sd
#実行後[sda][sdb]などディスクの名前が表示されるので確認
[ ] sd 0:0:0:0: [sda] 0000000000 512-byte logical blocks: (2.00 TB/1.82 TiB)
......
[ ] sd 2:0:0:0: [sdb] 0000000000 512-byte logical blocks: (2.00 TB/1.82 TiB)
......
[ ] sd 4:0:0:0: [sdc] 0000000000 512-byte logical blocks: (2.00 TB/1.82 TiB)
......
[ ] sd 5:0:0:0: [sdd] 0000000000 512-byte logical blocks: (4.00 TB/3.64 TiB)
......
```
2. shred
- 消したいディスクを選択削除
```bash
$sudo shred -v -n 3 -z /dev/sda #最後に削除したいディスクを選択
```
