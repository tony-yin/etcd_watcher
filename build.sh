cd `dirname $0`
tar -zcvf etcd_watcher_venv.tgz etcd_watcher_venv/
mkdir -p ./rpmbuild/{BUILD,RPMS,SPECS,SOURCES}
/usr/bin/python setup.py sdist --dist-dir=./rpmbuild/SOURCES
cp etcd_watcher.spec rpmbuild/SPECS
cd ./rpmbuild
rpmbuild --define "%_topdir `pwd`" -bb SPECS/etcd_watcher.spec
cd -
