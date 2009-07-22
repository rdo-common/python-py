%{!?python_sitelib: %define python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}

%define prerelease b8

Name:           python-py
Version:        1.0.0
Release:        0%{?prerelease:.%{prerelease}}%{?dist}
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
Source:         http://pypi.python.org/packages/source/p/py/py-%{version}%{?prerelease}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  python-devel
BuildRequires:  python-setuptools-devel
# needed by the testsuite:
BuildRequires:  subversion
BuildRequires:  python-docutils
BuildRequires:  python-pygments
BuildRequires:  pylint
BuildRequires:  pexpect

%define doctarget %{buildroot}%{_docdir}/%{name}-%{version}


%description
The py lib aims at supporting a decent development process addressing
deployment, versioning, testing and documentation perspectives.


%prep
%setup -q -n py-%{version}%{?prerelease}

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
find %{buildroot}%{python_sitelib} \( -name '*.py' -o -name 'py.*' \) \
   -exec sed -i '1{/^#!/d}' {} \; \
   -exec chmod u=rw,go=r {} \;

# move some txt files to the doc directory
mkdir -p %{doctarget}
mv %{buildroot}%{python_sitelib}/py/LICENSE %{doctarget}
mv %{buildroot}%{python_sitelib}/py/compat/LICENSE %{doctarget}/compat_LICENSE
mv %{buildroot}%{python_sitelib}/py/execnet/NOTES %{doctarget}/execnet_NOTES
mv %{buildroot}%{python_sitelib}/py/execnet/improve-remote-tracebacks.txt \
   %{doctarget}/execnet_improve-remote-tracebacks.txt
mv %{buildroot}%{python_sitelib}/py/path/gateway/TODO.txt %{doctarget}/path_gateway_TODO.txt
mv %{buildroot}%{python_sitelib}/py/path/svn/quoting.txt %{doctarget}/svn_quoting_path.txt
cp -pr doc example contrib %{doctarget}

# remove this and that
find %{buildroot}%{python_sitelib} -name '*.cmd' -exec rm {} \;

# remove (most) files only used by the testsuite
#find %{buildroot}%{python_sitelib} -type d -name testing -prune -exec rm -r {} \;
#find %{buildroot}%{python_sitelib} -name 'conftest.py*' -exec rm {} \;


%check
# some tests need to be skipped currently
PYTHONPATH=$(pwd)/py %{__python} py/bin/py.test \
  '-k-test_make_sdist_and_run_it -TestWCSvnCommandPath.test_not_versioned -TestWCSvnCommandPath.test_versioned' \
  py


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%{_bindir}/py.*
%{python_sitelib}/*
%{_docdir}/%{name}-%{version}


%changelog
* Wed Jul 22 2009 Thomas Moschny <thomas.moschny@gmx.de> - 1.0.0-0.b8
- Update to 1.0.0b8.
- Remove patches applied upstream.
- Greenlets have been removed upstream. So, package is noarch and
  - installs to %%{python_sitelib} again
  - %%ifarch sections have been removed.
- Don't remove files used by the testsuite for now.
- Add dependency on python-pygments, pylint and pexpect (for the
  testsuite).

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
