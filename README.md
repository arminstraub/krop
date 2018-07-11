# Krop [![License: GPL v3](https://img.shields.io/badge/License-GPL%20v3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
*Make yor PDF files fit in every e-book reader*


Krop is a simple graphical tool to crop the pages of PDF files and can automatically split pages to fit the screen of e-book readers.

![Screenshot](http://arminstraub.com/images/krop/screenshot-nook.png)

## Give krop a try without installing
Download the [source package](http://arminstraub.com/downloads/krop/krop-0.5.0.tar.gz) and start krop directly¹

```bash
tar xzf krop-0.5.0.tar.gz
cd krop-0.5.0
python -m krop
```
¹ *Requires: **PyQT**, **python-poppler-qt5** and **PyPDF2** (Also works with python-poppler-qt4 and pyPdf)*



## Install

### Snap

Visit https://snapcraft.io/krop or use the command:

```shell
sudo snap install krop --channel 
```


### Debian, Ubuntu and derivatives

```
sudo gdebi krop_0.5.0-1_all.deb
sudo apt-get install python-poppler-qt5 python-pypdf2
sudo dpkg -i krop_0.5.0-1_all.deb
```


### Fedora

```
yum install krop
```


### Gentoo

```
emerge krop
```
