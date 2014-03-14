SHELL = /bin/bash

this_dir       := '$(shell pwd)'
python_version := 3.3
python         := $(this_dir)/python/bin/python$(python_version)
easy_install   := $(python) $(this_dir)/python/bin/easy_install-$(python_version)
pip            := $(python) $(this_dir)/python/bin/pip$(python_version)
setuptools     := https://bitbucket.org/pypa/setuptools/raw/bootstrap/ez_setup.py
site_packages  := $(this_dir)/python/lib/python$(python_version)/site-packages
pep8           := $(python) python/bin/pep8
npm_version    := 1.3
tap            := mkdir -p .make; touch
bower          := node_modules/.bin/bower
jshint         := node_modules/.bin/jshint
vendor_files    = $(addsuffix .gz, $(filter-out %.gz, $(wildcard pub/vendor/*)))

export PIP_DOWNLOAD_CACHE = .cache

test: postgresql_running .make/python_dev node_modules _pub.json
	$(jshint) bin
	$(pep8) rarjpeg manage.py
	./manage.py test -v2

.make/dependencies:
	# Python $(python_version)
	python$(python_version) -h >/dev/null
	# npm $(npm_version)
	[[ $$(npm -v) == $(npm_version)* ]]
	$(tap) $@

postgresql_running:
	pgrep postgres >/dev/null

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

bower_components: .make/dependencies node_modules bower.json
	mkdir -p pub/vendor
	$(bower) install
	$(bower) list -p | bin/bower_ln.js | xargs -I _ -n 1 ln -f _ pub/vendor/

node_modules: .make/dependencies package.json
	npm install

_pub: python bower_components $(vendor_files)
	mkdir -p _pub
	./manage.py collectstatic --noinput -cl

%.gz: %; gzip -9cn $< >$@

_pub.json: _pub
	find _pub -type f -or -type l | bin/crc32_pub.js > _pub.json

clean:
	rm -rf .make _pub{.json,} bower_components node_modules pub/vendor python
