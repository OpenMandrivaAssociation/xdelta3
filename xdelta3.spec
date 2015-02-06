%define version		3.0v2
%define fversion	30v2
%define frealversion	3.0v
%define release		2
%define name		xdelta3

%define build_staticlib 0
%{?_with_staticlib: %global build_staticlib 1}

Summary:		A binary delta generator
Name:			%{name}
Version:		%{version}
Release:		%mkrel %{release}
Source0:		http://xdelta.googlecode.com/files/xdelta%{version}.tar.bz2
Patch0:			xdelta%{version}-optflags.patch
URL:			http://xdelta.org
License:		GPL
Group:			File tools
BuildRequires:		zlib-devel
BuildRoot:		%{_tmppath}/%{name}-%{version}-root

%description
Xdelta3 is the third and latest release of Xdelta, which is a set of
tools and APIs for reading and writing compressed deltas. Deltas
encode the differences between two versions of a document. This
release features a completely new compression engine, several
algorithmic improvements, a fully programmable interface modelled
after zlib, in addition to a command-line utility, use of the RFC3284
(VCDIFF) encoding, a python extension, and now 64-bit support.

%if %build_staticlib
%package devel
Summary: Static libraries and header files for development with XDelta3
Group: Development/C
Requires: %{name}

%description devel
This package contains the static libraries and header files
required to develop applications using Xdelta3.
%endif

%prep
%setup -q -n xdelta%{frealversion}
%patch0 -p1 -b .optflags

%build
RPM_OPT_FLAGS="%{optflags}" make RPM_OPT_FLAGS="%{optflags}" all \
	xdelta3 \
	xdelta3-decoder \
	xdelta3-tools \
	xdelta3-everything \
	xdelta3-all.o
ar cr libxdelta3.a xdelta3-all.o
ranlib libxdelta3.a
chmod 644 COPYING

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{_bindir}
%if %build_staticlib
mkdir -p %{buildroot}%{_libdir}	%{buildroot}%{_includedir}
%endif

install -m 755 xdelta3 \
	xdelta3-decoder \
	xdelta3-tools \
	xdelta3-everything %{buildroot}%{_bindir}
%if %build_staticlib
install -m 644 libxdelta3.a %{buildroot}%{_libdir}
install -m 644 xdelta3.h %{buildroot}%{_includedir}
%endif

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc COPYING
%{_bindir}/*

%if %build_staticlib
%files devel
%defattr(-,root,root)
%{_includedir}/*.h
%{_libdir}/*.a
%endif



%changelog
* Sun Nov 21 2010 Giuseppe Ghibò <ghibo@mandriva.com> 3.0v2-1mdv2011.0
+ Revision: 599401
- Upgrade to release 3.0v2.

* Wed Sep 09 2009 Thierry Vignaud <tv@mandriva.org> 3.0t-2mdv2010.0
+ Revision: 435073
- rebuild

* Mon Jan 07 2008 Giuseppe Ghibò <ghibo@mandriva.com> 3.0t-1mdv2008.1
+ Revision: 146203
- Release 3.0t.

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Thu May 31 2007 Giuseppe Ghibò <ghibo@mandriva.com> 3.0q-1mdv2008.0
+ Revision: 33122
- Import xdelta3



* Thu May 31 2007 Giuseppe Ghib� <ghibo@mandriva.com> 3.0q-1mdv2008.0
- Use -O2 instead of %%{optflags} as there are problems compiling with
  fortify enabled.
- initial release.
