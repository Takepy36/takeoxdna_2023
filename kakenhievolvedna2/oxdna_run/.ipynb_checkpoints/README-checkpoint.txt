手順書

###初期データセットの作成

1. 構造探索ツールを用意します

git clone https://bitbucket.org/leo-cazenille/kakenhievolvedna.git
cd kakenhievolvedna
tar xvf nupack3.2.2.tar.gz
cd nupack3.2.2
mkdir build && cd build
cmake .. && make -j 20
make install
pip3 install -r requirements.txt

2. 構造探索ツールを稼働します

/scripts/runAllExpes.sh
全ての実行結果が得られます。あるいは、

./scripts/illuminate.py -c <conf_filepath> -p multithreading
これにより選んだ設定ファイルに応じて結果を得られます。

(例)
./scripts/illuminate.py -c conf/peppercorn30x400x2000-L2-meanStruct1x30-nbActive2x7-log10ReactionCount1.0x5.0-length1x550-Grid3x50x55--SparseBinaryGA3-300000x40-0.5x0.5x1x2-7.yaml -p multithreading

3.設定を記述します
oxdna_runに移動してconfig.pyを開き、設定を確認・変更します

4. make_first_dataset.pyを実行します

python3 make_first_dataset.py 

###ループの実行

簡単に行うには

python3 test_loop.py <出力先ディレクトリパス> <初期データセットのディレクトリパス> <ストランドaの長さ> <ストランドbの長さ> <構造の最大規模> <ループ回数>

自動的にモデル作成、グリッド配置、oxDNAによるエネルギー計算、再学習が行われます