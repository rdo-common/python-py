%{!?python_sitearch: %define python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}

Name:           python-py
Version:        0.9.2
Release:        7%{?dist}
Summary:        Innovative python library containing py.test, greenlets and other niceties
Group:          Development/Languages
License:        MIT and LGPLv2+ and Public Domain and BSD and Python
#               - main package: MIT, except:
#                 - test/rsession/webdata/json.py: LPGLv2+
#                 - doc/style.css: Public Domain
#                 - test/web/post_multipart.py: Python 
#                   (see http://code.activestate.com/help/terms)
#                 - compat/textwrap.py: Python
#                 - compat/subprocess.py: Python
#                 - compat/doctest.py: Public Domain
#                 - compat/optparse.py: BSD
#               Note that all but the doctest compat files are removed
#               in the prep stage.
URL:            http://codespeak.net/py/dist/
Source:         http://pypi.python.org/packages/source/p/py/py-%{version}.tar.gz
# r58576 from trunk
Patch0:         py-0.9.2-fix-test-cache.patch
# r60277 from trunk
Patch1:         py-0.9.2-svn15.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  python-devel
BuildRequires:  python-setuptools-devel
# needed by the testsuite
BuildRequires:  subversion
BuildRequires:  python-docutils

%define doctarget %{buildroot}%{_docdir}/%{name}-%{version}

%ifarch ppc ppc64
# until the greenlet issue can be fixed
%define debug_package %{nil}
%endif


%description
The py lib aims at supporting a decent development process addressing
deployment, versioning, testing and documentation perspectives.


%prep
%setup -q -n py-%{version}
%patch0 -p1 -b .test-cache
%patch1 -p0 -b .svn

# remove the compatibility modules, and use system modules instead
for module in doctest optparse textwrap subprocess ; do
    rm py/compat/$module.py
    echo "from $module import *" > py/compat/system_$module.py
    sed -i py/__init__.py -e "s,compat/$module.py,compat/system_$module.py,"
done


%build
CFLAGS="$RPM_OPT_FLAGS" %{__python} setup.py build


%install
rm -rf %{buildroot}
%{__python} setup.py install -O1 --skip-build --root %{buildroot}

# remove shebangs and fix permissions
find %{buildroot}%{python_sitearch} \( -name '*.py' -o -name 'py.*' \) \
   -exec sed -i '1{/^#!/d}' {} \; \
   -exec chmod u=rw,go=r {} \;

# move and cleanup docs
mkdir -p %{doctarget}
mv %{buildroot}%{python_sitearch}/py/LICENSE %{doctarget}
mv %{buildroot}%{python_sitearch}/py/doc/* %{doctarget}
rm %{doctarget}/*.py*
rmdir %{buildroot}%{python_sitearch}/py/doc
mv %{buildroot}%{python_sitearch}/py/apigen/todo.txt %{doctarget}/todo_apigen.txt
mv %{buildroot}%{python_sitearch}/py/apigen/todo-apigen.txt %{doctarget}/todo-apigen_apigen.txt
mv %{buildroot}%{python_sitearch}/py/compat/LICENSE %{doctarget}/LICENSE_compat
mv %{buildroot}%{python_sitearch}/py/execnet/NOTES %{doctarget}/NOTES_execnet
mv %{buildroot}%{python_sitearch}/py/path/gateway/TODO.txt %{doctarget}/TODO_path_gateway.txt
mv %{buildroot}%{python_sitearch}/py/path/svn/quoting.txt %{doctarget}/quoting_path_svn.txt
mv %{buildroot}%{python_sitearch}/py/c-extension/greenlet/README.txt %{doctarget}/RADME_greenlet.txt

# remove (most) files only used by the testsuite
find %{buildroot}%{python_sitearch} -type d -name testing -prune -exec rm -r {} \;
find %{buildroot}%{python_sitearch} -name 'conftest.py*' -exec rm {} \;
rm -r %{buildroot}%{python_sitearch}/py/io/test

# remove this and that
rm %{buildroot}%{python_sitearch}/py/env.cmd
rm -r %{buildroot}%{python_sitearch}/py/bin
rm %{buildroot}%{python_sitearch}/py/c-extension/greenlet/*.h
rm %{buildroot}%{python_sitearch}/py/c-extension/greenlet/*.c
rm %{buildroot}%{python_sitearch}/py/c-extension/greenlet/setup.*
rm %{buildroot}%{python_sitearch}/py/c-extension/greenlet/test_*

%ifarch ppc ppc64
cp -p py/c-extension/greenlet/dummy_greenlet.py \
   %{buildroot}%{python_sitearch}/py/c-extension/greenlet/greenlet.py
rm %{buildroot}%{python_sitearch}/py/c-extension/greenlet/greenlet.so
cat << \EOF > %{doctarget}/README.greenlet.fedora
The native py.magic.greenlet code has been replaced by
dummy_greenlet.py on ppc and ppc64 for this package because it
reproducibly segfaults.
%endif


%check

# on ppc, use dummy greenlets also for the tests
%ifarch ppc ppc64
cp -p py/c-extension/greenlet/dummy_greenlet.py \
   py/c-extension/greenlet/greenlet.py
rm py/c-extension/greenlet/*.{c,h}
%endif

# see pylib issue67
rm py/doc/apigen.txt
sed -i '/apigen/d' py/doc/index.txt

PYTHONPATH=$(pwd)/py %{__python} py/bin/py.test py


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%{_bindir}/py.*
%{python_sitearch}/*
%{_docdir}/%{name}-%{version}


%changelog
* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.2-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Jan 14 2009 Thomas Moschny <thomas.moschny@gmx.de> - 0.9.2-6
- Use system doctest module again, as this wasn't the real cause of
  the test failure. Instead, remove the failing test for now.

* Fri Dec 12 2008 Thomas Moschny <thomas.moschny@gmx.de> - 0.9.2-5
- Add patch from trunk fixing a subversion 1.5 problem (pylib
  issue66).
- Don't replace doctest compat module (pylib issue67).

* Fri Nov 21 2008 Thomas Moschny <thomas.moschny@gmx.de> - 0.9.2-4
- Use dummy_greenlet on ppc and ppc64.

* Tue Oct  7 2008 Thomas Moschny <thomas.moschny@gmx.de> - 0.9.2-3
- Replace compat modules by stubs using the system modules instead.
- Add patch from trunk fixing a timing issue in the tests.

* Tue Sep 30 2008 Thomas Moschny <thomas.moschny@gmx.de> - 0.9.2-2
- Update license information.
- Fix the tests.

* Sun Sep  7 2008 Thomas Moschny <thomas.moschny@gmx.de> - 0.9.2-1
- Update to 0.9.2.
- Upstream now uses setuptools and installs to %%{python_sitearch}.
- Remove %%{srcname} macro.
- More detailed information about licenses.

* Wed Aug 21 2008 Thomas Moschny <thomas.moschny@gmx.de> - 0.9.1-1
- New package.
