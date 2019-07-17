# windows10とububtuを2台のSSDを使ってブートする方法を解説
## 手順
[参考URL](https://qiita.com/udai1532/items/4893af6ea4da3e20b302)
1. Ubuntuの入ったUSB　or　DVDを作成<br>
***ここでウブンツのインストールディスクだけ接続***
2. UEFIの設定は解除してBIOSよりブート優先順位を設定
3. まるっとUbuntuをインストール<br>
***ここでwindowsのディスクもつないでウブンツの方を起動***
4. **grubの設定**
```bash:grub
sudo apt install grub
```
このままだとwindowsが認識されないのでもうちょっと作業<br>
理由としては/boot/grub/grub.cfgにWindowsの記述がないため
```bash:grub2
sudo update-grub
```
確認コマンド
```bash:grub3
grep windows /boot/grub/grub.cfg
menuentry 'Windows Boot Manager (on /dev/sda2)' --class windows --class os $menuentry_id_option 'osprober-efi-4A71-DC25' {
#以上のようなメッセージが出ればOK
```

