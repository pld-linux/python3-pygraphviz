#
# Conditional build:
%bcond_with	doc	# Sphinx documentation (fails: missing gallery file?)
%bcond_without	tests	# unit tests

%define 	module	pygraphviz
Summary:	pygraphviz - Python interface to the Graphviz graph layout and visualization package
Summary(pl.UTF-8):	pygraphviz - pythonowy interfejs do pakietu struktur i wizualizacji grafów Graphviz
Name:		python3-%{module}
Version:	1.14
Release:	1
License:	BSD
Group:		Libraries/Python
#Source0Download: https://pypi.org/simple/pygraphviz/
Source0:	https://files.pythonhosted.org/packages/source/p/pygraphviz/%{module}-%{version}.tar.gz
# Source0-md5:	670ba4e63d7b28fb3b6748d4d4c54b15
URL:		https://pygraphviz.github.io/
BuildRequires:	graphviz-devel
BuildRequires:	pkgconfig
BuildRequires:	python3-devel >= 1:3.10
BuildRequires:	python3-setuptools >= 1:61.2
%if %{with tests}
BuildRequires:	python3-pytest
%endif
BuildRequires:	rpm-build >= 4.6
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
BuildRequires:	unzip
%if %{with doc}
BuildRequires:	python3-numpydoc
BuildRequires:	python3-pydata_sphinx_theme
BuildRequires:	sphinx-pdg-3
%endif
Requires:	python3-modules >= 1:3.10
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
%py3_build

%if %{with tests}
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
PYTHONPATH=$(readlink -f build-3/lib.*) \
%{__python3} -m pytest build-3/lib.*/pygraphviz/tests
%endif

%if %{with doc}
PYTHONPATH=$(readlink -f build-3/lib.*) \
%{__make} -C doc html \
	SPHINXBUILD=sphinx-build-3
%endif

%install
rm -rf $RPM_BUILD_ROOT

%py3_install

%{__rm} $RPM_BUILD_ROOT%{py3_sitedir}/pygraphviz/graphviz.i
%{__rm} $RPM_BUILD_ROOT%{py3_sitedir}/pygraphviz/graphviz_wrap.c
%{__rm} -r $RPM_BUILD_ROOT%{py3_sitedir}/pygraphviz/tests

install -d $RPM_BUILD_ROOT%{_examplesdir}
cp -pr examples $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc LICENSE README.rst
%dir %{py3_sitedir}/pygraphviz
%{py3_sitedir}/pygraphviz/_graphviz.cpython-*.so
%{py3_sitedir}/pygraphviz/*.py
%{py3_sitedir}/pygraphviz/__pycache__
%{py3_sitedir}/pygraphviz-%{version}-py*.egg-info
%{_examplesdir}/%{name}-%{version}

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc doc/build/html/{_static,reference,*.html,*.js}
%endif
