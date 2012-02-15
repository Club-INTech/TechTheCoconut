copies-IPython: install-ubuntu clean
	if ( test ! -d ~/.ipython);then mkdir ~/.ipython; fi
	sudo cp ipython/fonctions_ipython.py /usr/share/pyshared/IPython/UserConfig/
	sudo cp ipython/ipy_user_conf.py /usr/share/pyshared/IPython/UserConfig/
	cp ipython/ipy_user_conf.py ~/.ipython/
	cp ipython/fonctions_ipython.py  ~/.ipython/

install-ubuntu:
	sudo apt-get install python-nose python-sphinx python-serial python-pygame ipython

clean:
	find . -name "*.pyc" -exec rm -rf {} \;

