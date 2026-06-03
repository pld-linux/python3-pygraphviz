#
# Conditional build:
%bcond_without	doc	# Sphinx documentation
%bcond_with	tests	# unit tests (fail with current graphviz)

%define 	module	pygraphviz
Summary:	pygraphviz - Python interface to the Graphviz graph layout and visualization package
Summary(pl.UTF-8):	pygraphviz - pythonowy interfejs do pakietu struktur i wizualizacji grafów Graphviz
Name:		python-%{module}
# keep 1.5 here for python2 support
Version:	1.5
Release:	1
License:	BSD
Group:		Libraries/Python
#Source0Download: https://pypi.org/simple/pygraphviz/
Source0:	https://files.pythonhosted.org/packages/source/p/pygraphviz/%{module}-%{version}.zip
# Source0-md5:	c186f5f6567e523a862063fc62ddcd2f
URL:		https://pygraphviz.github.io/
BuildRequires:	graphviz-devel
BuildRequires:	pkgconfig
BuildRequires:	python-devel >= 1:2.7
BuildRequires:	python-setuptools
%if %{with tests}
BuildRequires:	python-doctest-ignore-unicode >= 0.1.2
BuildRequires:	python-mock >= 2.0.0
BuildRequires:	python-nose >= 1.3.7
%endif
BuildRequires:	rpm-build >= 4.6
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
BuildRequires:	unzip
%if %{with doc}
BuildRequires:	sphinx-pdg-2
%endif
Requires:	python-modules >= 1:2.7
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
pygraphviz is a Python wrapper to the graph data structure of the
graphviz graph layout and visualization package.

%description -l pl.UTF-8
pygraphviz to pythonowy interfejs do struktury danych grafów pakietu
do opisu i wizualizacji grafów graphviz.

%package apidocs
Summary:	API documentation for Python pygraphviz module
Summary(pl.UTF-8):	Dokumentacja API modułu Pythona pygraphviz
Group:		Documentation
BuildArch:	noarch

%description apidocs
API documentation for Python pygraphviz module.

%description apidocs -l pl.UTF-8
Dokumentacja API modułu Pythona pygraphviz.

%prep
%setup -q -n %{module}-%{version}

%build
%py_build

%if %{with tests}
PYTHONPATH=$(readlink -f build-2/lib.*) \
nosetests-%{py_ver} build-2/lib.*/pygraphviz/tests
%endif

%if %{with doc}
PYTHONPATH=$(readlink -f build-2/lib.*) \
%{__make} -C doc html \
	SPHINXBUILD=sphinx-build-2
%endif

%install
rm -rf $RPM_BUILD_ROOT

%py_install

%py_postclean

%{__rm}  $RPM_BUILD_ROOT%{py_sitedir}/pygraphviz/graphviz.i
%{__rm}  $RPM_BUILD_ROOT%{py_sitedir}/pygraphviz/graphviz_wrap.c
%{__rm} -r $RPM_BUILD_ROOT%{py_sitedir}/pygraphviz/tests

# packaged as %doc / in examplesdir
%{__rm} -r $RPM_BUILD_ROOT%{_docdir}/pygraphviz-%{version}

install -d $RPM_BUILD_ROOT%{_examplesdir}
cp -pr examples $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc LICENSE README.rst
%dir %{py_sitedir}/pygraphviz
%{py_sitedir}/pygraphviz/_graphviz.so
%{py_sitedir}/pygraphviz/*.py[co]
%{py_sitedir}/pygraphviz-%{version}-py*.egg-info
%{_examplesdir}/%{name}-%{version}

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc doc/build/html/{_static,reference,*.html,*.js}
%endif
