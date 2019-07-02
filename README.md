# People Counter

## Dependencies

### server
- python 3.7.1
- opencv 4.1.0
- imutils 0.5.2
- python-osc 1.7.0

### client
- python 3.7.1
- python-osc

## Usage
- `python client.py --ip 127.0.0.1 --port 5000 --address /people --id 2`
    - -i, --ip : OSCのIP （default : "127.0.0.1")
    - -p, --port : OSCのPORT (default : 5000)
    - -a, --address : OSCのアドレス (defualt : "/people")
    - -c, --confidence : 認識の閾値 (default : 0.4)
    - -s, --skip-frames : 何フレームに一回認識プログラム動かすか (default : 1)
- 上記パラメータを必要に応じて書く、デフォルトの場合は書かない
