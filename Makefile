this_dir       = '$(shell pwd)'
python_version = 3.3
python         = $(this_dir)/python/bin/python$(python_version)
easy_install   = $(python) $(this_dir)/python/bin/easy_install-$(python_version)
pip            = $(python) $(this_dir)/python/bin/pip$(python_version)
setuptools     = https://bitbucket.org/pypa/setuptools/raw/bootstrap/ez_setup.py
site_packages  = $(this_dir)/python/lib/python$(python_version)/site-packages
pep8           = $(python) python/bin/pep8
bower_version  = 1.2
tap            = mkdir -p .make; touch

test: .make/python_dev
	$(pep8) rarjpeg manage.py
	./manage.py test -v2

.make/dependencies:
	# Python $(python_version)
	python$(python_version) -h >/dev/null
	# Bower $(bower_version)
	[[ $$(bower -v) == $(bower_version)* ]]
	$(tap) $@

python: .make/dependencies requirements.txt
	- pyvenv-$(python_version) python
	mkdir -p python/local
	- ln -s ../bin python/local/bin
	rm -f $(site_packages)/setuptools*.{egg,pth} # setuptools bug
	cd /tmp; curl -C - '-#' $(setuptools) | $(python)
	$(easy_install) pip
	$(pip) install -r requirements.txt

.make/python_dev: python bower_components requirements_dev.txt
	$(pip) install -r requirements_dev.txt
	$(tap) $@

bower_components: .make/dependencies bower.json
	bower install
	bower list --paths | bin/bower_ln.js | xargs -I _ -n 1 ln _ pub/bower/

_pub: python bower_components
	./manage.py collectstatic -l

clean:
	rm -rf .make _pub bower_components python
