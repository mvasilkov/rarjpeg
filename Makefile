this_dir       = '$(shell pwd)'
python_version = 3.3
python         = $(this_dir)/python/bin/python$(python_version)
easy_install   = $(python) $(this_dir)/python/bin/easy_install-$(python_version)
pip            = $(python) $(this_dir)/python/bin/pip$(python_version)
setuptools     = https://bitbucket.org/pypa/setuptools/raw/bootstrap/ez_setup.py
site_packages  = $(this_dir)/python/lib/python$(python_version)/site-packages
pep8           = $(python) python/bin/pep8
bower_version  = 1.2

test: python_dev
	$(pep8) rarjpeg
	./manage.py test -v2

dependencies:
	# Python $(python_version)
	python$(python_version) -h >/dev/null
	# Bower $(bower_version)
	[[ $$(bower -v) == $(bower_version)* ]]

python: dependencies requirements.txt
	- pyvenv-$(python_version) python
	mkdir -p python/local
	- ln -s ../bin python/local/bin
	rm -f $(site_packages)/setuptools*.{egg,pth} # setuptools bug
	cd /tmp; curl -C - '-#' $(setuptools) | $(python)
	$(easy_install) pip
	$(pip) install -r requirements.txt

python_dev: python requirements_dev.txt
	$(pip) install -r requirements_dev.txt

_pub: python
	./manage.py collectstatic -l

clean:
	rm -rf _pub python
