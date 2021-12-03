#!/bin/bash
N=$1
contract_address="0x5b1869D9A4C187F2EAa108f3062412ecf0526b24"
account=(
  0x4f3edf983ac636a65a842ce7c78d9aa706d3b113bce9c46f30d7d21715b23b1d
  0x6cbed15c793ce57650b9877cf6fa156fbef513c4e6134f022a85b1ffdd59b2a1
  0x6370fd033278c143179d81c5526140625662b8daa446c22ee2d73db3707e620c
  0x646f1ce2fdad0e6deeeb5c7e8e5543bdde65e86029e2fd9fc169899c440a7913
  0xadd53f9a7e588d003326d1cbf9e4a43c061aadd9bc938c843a79e7b4fd2ad743
  0x395df67f0c2d2d9fe1ad08d1bc8b6627011959b79c53d7dd6a3536a33ab8a4fd
  0xe485d098507f54e7733a205420dfddbe58db035fa577fc294ebd14db90767a52
  0xa453611d9419d0e56f499079478fd72c37b251a94bfde4d19872c44cf65386e3
  0x829e924fdf021ba3dbbc4225edfece9aca04b929d6e75613329ca6f1d31c0bb4
  0xb0057716d5917badaf911b193b12b910811c1497b5bada8d7711f758981c3773
  0x77c5495fbb039eed474fc940f29955ed0531693cc9212911efd35dff0373153f
  0xd99b5b29e6da2528bf458b26237a6cf8655a3e3276c1cdc0de1f98cefee81c01
  0x9b9c613a36396172eab2d34d72331c8ca83a358781883a535d2941f66db07b24
  0x0874049f95d55fb76916262dc70571701b5c4cc5900c0691af75f1a8a52c8268
  0x21d7212f3b4e5332fd465877b64926e3532653e2798a11255a46f533852dfe46
  0x47b65307d0d654fd4f786b908c04af8fface7710fc998b37d219de19c39ee58c
  0x66109972a14d82dbdb6894e61f74708f26128814b3359b64f8b66565679f7299
  0x2eac15546def97adc6d69ca6e28eec831189baa2533e7910755d15403a0749e8
  0x2e114163041d2fb8d45f9251db259a68ee6bdbfd6d10fe1ae87c5c4bcd6ba491
  0xae9a2e131e9b359b198fa280de53ddbe2247730b881faae7af08e567e58915bd
  )
source venv/bin/activate

npx ganache-cli -d -a 20 &
npx truffle migrate
ipfs --offline daemon &

cd client/event_retriever
python event_retriever.py -c $contract_address &

cd ../key_manager
for val in "${account[@]:0:$N}"; do
  sleep 0.5
  python key_manager.py -c $contract_address -s $val &
done

cd ..
export FLASK_APP=webapp
export FLASK_ENV=development
flask init-db
flask run
