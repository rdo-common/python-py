%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}

Name:           python-py
Version:        1.3.0
Release:        1%{?prerelease:.%{prerelease}}%{?dist}
Summary:        Rapid testing (py.test) and development utils (pylib)
Group:          Development/Languages
License:        MIT and Public Domain
#               main package: MIT, except: doc/style.css: Public Domain
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


%description
The py lib has several namespaces which help with testing, generating
and distributing code across machines.


%prep
%setup -q -n py-%{version}%{?prerelease}


%build
CFLAGS="$RPM_OPT_FLAGS" %{__python} setup.py build


%install
rm -rf %{buildroot}
%{__python} setup.py install -O1 --skip-build --root %{buildroot}

# remove shebangs and fix permissions
find %{buildroot}%{python_sitelib} \( -name '*.py' -o -name 'py.*' \) \
   -exec sed -i '1{/^#!/d}' {} \; \
   -exec chmod u=rw,go=r {} \;

# remove some backup files
rm -f doc/test/plugin/links.txt.orig \
      doc/code.txt.orig \
      doc/test/plugin/index.txt.orig


%check
%{__python} bin/py.test --report=failed,skipped


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%{_bindir}/py.*
%{python_sitelib}/*
%doc CHANGELOG LICENSE README.txt
%doc doc contrib


%changelog
* Sat May  8 2010 Thomas Moschny <thomas.moschny@gmx.de> - 1.3.0-1
- Update to 1.3.0.
- Remove some backup (.orig) files.

* Sun Feb 14 2010 Thomas Moschny <thomas.moschny@gmx.de> - 1.2.1-1
- Update to 1.2.1.

* Wed Jan 27 2010 Thomas Moschny <thomas.moschny@gmx.de> - 1.2.0-1
- Update to 1.2.0.
- Adjust summary and %%description.
- Use %%global instead of %%define.

* Sat Nov 28 2009 Thomas Moschny <thomas.moschny@gmx.de> - 1.1.1-1
- Update to 1.1.1.

* Sat Nov 21 2009 Thomas Moschny <thomas.moschny@gmx.de> - 1.1.0-1
- Update to 1.1.0. Upstream reorganized the package's structure and
  cleaned up the install process, so the specfile could be greatly
  simplified.
- Dropped licenses for files no longer present from the License tag.

* Thu Aug 27 2009 Thomas Moschny <thomas.moschny@gmx.de> - 1.0.2-1
- Update to 1.0.2.
- One failing test is no longer part of the testsuite, thus needs not
  to be skipped anymore.
- Some developer docs are missing this time in upstream's tarfile, so
  cannot be moved to %%{_docdir}

* Thu Aug 13 2009 Thomas Moschny <thomas.moschny@gmx.de> - 1.0.0-1
- Update to 1.0.0.
- Re-enable SVN tests in %%check.

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.0-1.b8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

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
