# pythonスクリプトをraspberry pi起動時に実行する方法

参考 https://qiita.com/tkato/items/6a227e7c2c2bde19521c



1. pythonプログラムを実行できるようにする

  プログラム1行目にshebangを追加

  ```python
  #!/usr/bin/env python
  ```

2. サービス内容を書く

/etc/systemd/system/サービス名.service に以下を書く

```
[Unit]
Description = 説明文（好きにに入れて良いです）
After=local-fs.target
ConditionPathExists=自動起動するプログラムが配置されているディレクトリ(/opt/パッケージ名)

[Service]
ExecStart=自動起動するプログラムへのフルパス(/opt/パッケージ名/bin/YYYY.py)
Restart=no
Type=simple


 [Install]
 WantedBy=multi-user.target
```
  
3. サービスをロード

```bash
sudo systemctl daemon-reload
```

ロードされたかは以下コマンドで確認

```bash
$ sudo systemctl status RasPiAuto.service
● RasPiAuto.service - A sample automatic execution
   Loaded: loaded (/etc/systemd/system/RasPiAuto.service; disabled; vendor preset: disabled)
   Active: inactive (dead)
```

loadedになってればOK

4. 自動起動に追加

```bash
sudo systemctl enable サービス名.service
```

自動起動になったかは以下で確認

```bash
$ sudo  systemctl status RasPiAuto.service
● RasPiAuto.service - A sample automatic execution
   Loaded: loaded (/etc/systemd/system/RasPiAuto.service; enabled; vendor preset: disabled)
   Active: inactive (dead)
```

loaded項の中にenableって書いてあればok

5. 動作確認

```bash
sudo systemctl start サービス名.service
```

動作状況は以下で確認

```bash
sudo systemctl status サービス名.service
```



ここまでで起動時にpythonプログラムが起動するようになる。