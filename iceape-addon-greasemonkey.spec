%define		_realname	greasemonkey
Summary:	Greasemonkey lets you add Javascript to any web page
Name:		iceape-addon-%{_realname}
Version:	0.8.2
Release:	1
License:	BSD-like
Group:		X11/Applications/Networking
Source0:	http://downloads.mozdev.org/xsidebar/mods/%{_realname}-%{version}-mod.xpi
# Source0-md5:	fec6e717552e2e5c9653a0316f6f9d06
URL:		http://xsidebar.mozdev.org/modifiedmisc.html#greasemonkey
BuildRequires:	unzip
Requires(post,postun):	iceape >= 1.1
Requires(post,postun):	textutils
Requires:	iceape >= 1.1
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_iceapedir	%{_libdir}/iceape
%define		_iceapedatadir	%{_datadir}/iceape

%description
Greasemonkey is an iceape extension which lets you to add bits of
DHTML ("user scripts") to any web page to change its behavior. In much
the same way that user CSS lets you take control of a web page's
style, user scripts let you easily control any aspect of a web page's
design or interaction.

%prep
%setup -q -c -T
install %{SOURCE0} %{_realname}.xpi
unzip %{_realname}.xpi

INST="chrome/%{_realname}-installed-chrome.txt"
echo 'content,install,url,jar:resource:/chrome/greasemonkey.jar!/content/' > $INST

for LANG in en-US ca-AD cs-CZ da-DK de-DE es-ES eu-ES fa-IR \
		fi-FI fr-FR gl-ES he-IL it-IT ja-JP ko-KR nl-NL \
		pl-PL pt-BR pt-PT ru-RU sk-SK sl-SI sv-SE tr-TR \
		uk-UA zh-CN zh-TW; do
	echo "locale,install,url,jar:resource:/chrome/greasemonkey.jar!/locale/$LANG/"
done >> $INST

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_iceapedir} \
	$RPM_BUILD_ROOT%{_iceapedatadir}/defaults/pref

cp -rv components $RPM_BUILD_ROOT%{_iceapedir}
cp -rv chrome $RPM_BUILD_ROOT%{_iceapedatadir}
install defaults/preferences/greasemonkey.js $RPM_BUILD_ROOT%{_iceapedatadir}/defaults/pref

%clean
rm -rf $RPM_BUILD_ROOT

%post
if [ "$1" = 1 ]; then
	%{_sbindir}/iceape-chrome+xpcom-generate
fi

%postun
[ ! -x %{_sbindir}/iceape-chrome+xpcom-generate ] || %{_sbindir}/iceape-chrome+xpcom-generate

%files
%defattr(644,root,root,755)
%{_iceapedatadir}/chrome/%{_realname}.jar
%{_iceapedatadir}/chrome/%{_realname}-installed-chrome.txt
%{_iceapedatadir}/chrome/icons/default/%{_realname}.ico
%{_iceapedatadir}/defaults/pref/%{_realname}.js
%{_iceapedir}/components/gm*.xpt
%{_iceapedir}/components/%{_realname}.js
