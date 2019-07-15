# etcd_watcher 
## Introduction

Implement service ha by election of etcd which used `CAS` and `TTL`.

## Install

```
./build.sh
rpm -ivh ./rpmbuild/RPMS/noarch/etcd_watcher-0.1.0-1.noarch.rpm
```

## Init election

![etcd init election][1]

## More details

[document for this project][2]


[1]: http://cdn.tony-yin.site/etcd_init_election.gif
[2]: https://www.tony-yin.site/2019/05/15/Etcd_Service_HA/
