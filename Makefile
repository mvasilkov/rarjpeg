this_dir       = '$(shell pwd)'
python_version = 3.3
python         = $(this_dir)/python/bin/python$(python_version)
easy_install   = $(python) $(this_dir)/python/bin/easy_install-$(python_version)
pip            = $(python) $(this_dir)/python/bin/pip$(python_version)
setuptools     = https://bitbucket.org/pypa/setuptools/raw/bootstrap/ez_setup.py
site_packages  = $(this_dir)/python/lib/python$(python_version)/site-packages

test: python
	./manage.py test -v2

python: requirements.txt
	- pyvenv-$(python_version) python
	rm -f $(site_packages)/setuptools*.{egg,pth} # setuptools bug
	cd /tmp; curl -C - '-#' $(setuptools) | $(python)
	$(easy_install) pip
	$(pip) install -r requirements.txt

_pub: python
	./manage.py collectstatic -l

clean:
	rm -rf _pub python
