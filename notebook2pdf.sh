echo "convert $1 ..."
ipython nbconvert $1 --to latex --post pdf --SphinxTransformer.author='Joe Hart' --SphinxTransformer.title='Test'
echo "clean ..."
make clean