# G16 Manager

## 概要
G16 Managerは、Pythonのtkinterライブラリを用いて開発されたGUIアプリケーションで、Gaussian計算用の`.gjf`ファイルを管理・実行する機能を提供します。ファイルはドラッグアンドドロップまたはファイル選択ダイアログを通じてリストに追加され、ユーザーはファイルをリスト内で並べ替えたり、選択したファイルをクリアしたりすることができます。`Start Calculations`ボタンを押すと、選択された計算ジョブがバックグラウンドで実行されます。

## 主な特徴
- **ファイルの追加**: ドラッグアンドドロップまたは`Add Files`ボタンを使って、計算ファイルをリストに追加。
- **リスト操作**: 選択されたファイルの並び替え（上移動/下移動）、選択解除（クリア）。
- **バックグラウンド計算**: 計算をバックグラウンドで実行し、進行状態をリアルタイムで確認。

## インストール方法
このソフトウェアを使用するには、以下の手順に従ってください：

1. このリポジトリをクローンまたはダウンロードします。
2. 必要なPythonライブラリをインストールします：
    ```bash
    pip install tkinter tkinterdnd2
    ```
3. アプリケーションを起動します：
    ```bash
    python g16_manager.py
    ```

## 使用方法
1. アプリケーションを開くと、主画面が表示されます。
2. `Add Files`ボタンをクリックして、計算に使用する`.gjf`ファイルを選択、またはファイルをウィンドウにドラッグアンドドロップします。
3. ファイルを`Pending Files`に追加した後、`Start Calculations`ボタンをクリックして計算を開始します。
4. 計算が進行すると、`Running Calculations`リストにファイルが表示され、計算完了後にはリストから自動的に削除されます。
5. 計算完了後、`Pending Files`の一番上にあるファイルの計算が自動的に進行し`Running Calculations`に表示されます。
6. `Pending Files`のすべてファイルの計算が終わり次第`Start Calculations`ボタンがアクティベ―トされます。`Pending Files`は計算中でも追加することが可能です。
7. ×ボタンを押しプログラム終了時には`atexit`モジュールを使ってGaussianのプロセスがクリーンアップされます。

## 設定のカスタマイズ
### G16コマンドのパス設定
デフォルトでは、G16 ManagerはシステムのパスからGaussianの`g16`コマンドを実行しますが、異なるシステムでこのパスは異なる場合があります。自分のシステムに合わせて、以下の手順でパスを設定してください：
1. `G16_manager.py`をテキストエディタで開きます。
2. `run_calculation`メソッドを見つけて、以下の行を探します：
    ```python
    cmd = f'g16 "{file_path}" "{output_file}"'
    ```
3. 上記の行を自分のシステムにインストールされたGaussianのパスに書き換えます。例えば：
    ```python
    cmd = f'C:\\Gaussian\\g16 "{file_path}" "{output_file}"'
    ```
4. ファイルを保存し、アプリケーションを再起動します。

## トラブルシューティング
- **G16コマンドが見つからない場合**: Gaussianのインストールディレクトリが正しく設定されているか確認してください。
- **計算が実行されない場合**: G16 Managerが適切に設定されているか、またはPythonと依存ライブラリが正しくインストールされているかを確認してください。

## 特記事項
`tkinterdnd2`モジュールを使用してファイルのドラッグアンドドロップ機能を実現しています。

## EXEファイルの生成
このアプリケーションをEXEファイルに変換するにはPyInstallerを使用します。以下の手順に従ってください：

1. PyInstallerをインストールします：
    ```bash
    pip install pyinstaller
    ```
2. 必要な`.spec`ファイルを作成し、特定のデータファイルを含めるように設定します。例えば`tkdnd2.8`フォルダを含めるためには、`.spec`ファイルに次のように記述します：
    ```python
    # g16_manager.spec
    block_cipher = None
    a = Analysis(['G16_manager.py'],
                 pathex=['C:\\Path\\To\\Your\\Project'],
                 binaries=[],
                 datas=[('C:/Users/AppData/Local/Programs/Python/Python312/tcl/tkdnd2.8', 'tkdnd2.8')],
                 hiddenimports=[],
                 hookspath=[],
                 runtime_hooks=[],
                 excludes=[],
                 win_no_prefer_redirects=False,
                 win_private_assemblies=False,
                 cipher=block_cipher,
                 noarchive=False)
    pyz = PYZ(a.pure, a.zipped_data,
              cipher=block_cipher)
    exe = EXE(pyz,
              a.scripts,
              [],
              exclude_binaries=True,
              name='G16_manager',
              debug=False,
              bootloader_ignore_signals=False,
              strip=False,
              upx=True,
              console=False)
    coll = COLLECT(exe,
                   a.binaries,
                   a.zipfiles,
                   a.datas,
                   strip=False,
                   upx=True,
                   name='G16_manager')
    ```
3. `.spec`ファイルを使用してEXEをビルドします：
    ```bash
    pyinstaller g16_manager.spec
    ```
この手順に従うことで、G16 ManagerアプリケーションをWindowsの実行可能ファイルとして利用できます。
