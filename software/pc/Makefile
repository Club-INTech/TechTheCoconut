copies-IPython: install-ubuntu clean
	if not(test -d ~/.ipython) then mkdir ~/.ipython
	sudo cp ipython/fonctions_ipython.py /usr/share/pyshared/IPython/UserConfig/
	sudo cp ipython/ipy_user_conf.py /usr/share/pyshared/IPython/UserConfig/
	sudo cp ipython/ipy_user_conf.py ~/.ipython/
	sudo cp ipython/fonctions_ipython.py  ~/.ipython/

install-ubuntu:
	sudo apt-get install python-nose python-sphinx python-serial python-pygame ipython

clean:
	find . -name "*.pyc" -exec rm -rf {} \;

