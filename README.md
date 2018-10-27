# Krop [![License: GPL v3](https://img.shields.io/badge/License-GPL%20v3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
*Make your PDF files fit in every e-book reader*


Krop is a simple graphical tool to crop the pages of PDF files and can automatically split pages to fit the screen of e-book readers.

![Screenshot](http://arminstraub.com/images/krop/screenshot-nook.png)


For more information, see the [official website](http://arminstraub.com/software/krop).


## Give krop a try without installing
Download the [source package](http://arminstraub.com/downloads/krop/krop-0.5.1.tar.gz) and start krop directly¹:

```bash
tar xzf krop-0.5.1.tar.gz
cd krop-0.5.1
python -m krop
```
¹ *Requires: **PyQT5**, **python-poppler-qt5** and **PyPDF2** (also works with PyQT4, python-poppler-qt4 and pyPdf)*

This should work using either version 2 or 3 of Python. On some distributions, including Ubuntu 18.04, you need to replace python with python3 in order to use Python 3.



## Install

### Snap

Visit https://snapcraft.io/krop or use the command:

```shell
sudo snap install krop --channel 
```


### Debian, Ubuntu and derivatives

Download the [debian package](http://arminstraub.com/downloads/krop/krop-0.5.1-1_all.deb) and install it:

```
sudo gdebi krop_0.5.1-1_all.deb
```

For older distributions, you will need to download older packages (try version 0.5.0) or install krop in some other way.


### Fedora

```
yum install krop
```


### Gentoo

```
emerge krop
```
