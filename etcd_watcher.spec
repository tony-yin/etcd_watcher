%define name etcd_watcher
%define version 0.1.0
%define unmangled_version 0.1.0
%define unmangled_version 0.1.0
%define release 1

Summary: A centralized coordination service for ha.
Name: %{name}
Version: %{version}
Release: %{release}
Source0: %{name}-%{unmangled_version}.tar.gz
License: GNU General Public License v3
Group: Development/Libraries
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
Prefix: %{_prefix}
BuildArch: noarch
Vendor: etcd_watcher <1241484989@qq.com>
Url: https://github.com/tony-yin/etcd_watcher
BuildRequires:  python-devel
BuildRequires:  python-setuptools

%description
==========
etcd_watcher
==========


.. image:: https://img.shields.io/pypi/v/etcd_watcher.svg
        :target: https://pypi.python.org/pypi/etcd_watcher

.. image:: https://img.shields.io/travis/tony-yin/etcd_watcher.svg
        :target: https://travis-ci.org/tony-yin/etcd_watcher

.. image:: https://readthedocs.org/projects/etcd_watcher/badge/?version=latest
        :target: https://etcd_watcher.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status




A centralized coordination service for ha.


* Free software: GNU General Public License v3
* Documentation: https://etcd_watcher.readthedocs.io.


Features
--------

* TODO


=======
History
=======

0.1.0 (2019-01-12)
------------------

* First release on PyPI.


%prep
%setup -n %{name}-%{unmangled_version} -n %{name}-%{unmangled_version}

%build
/usr/bin/python setup.py build

%install
/usr/bin/python setup.py install --single-version-externally-managed -O1 --root=$RPM_BUILD_ROOT --record=INSTALLED_FILES

%post
tar -zxvf /opt/etcd_watcher_venv.tgz -C /opt/
systemctl enable etcd_watcher
systemctl start etcd_watcher

%clean
rm -rf $RPM_BUILD_ROOT

%files -f INSTALLED_FILES
%defattr(-,root,root)
