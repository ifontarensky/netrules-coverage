# Variable
PYTHON=$(shell which python3)
PIP=$(which pip3)

# Set important Paths
PROJECT := netrules_coverage
DOCPATH := docs

# Variable used for documentation
SPHINXOPTS   =
SPHINXBUILD  = sphinx-build
SPHINXPROJ   = sphinx
SOURCEDIR    = .
BUILDDIR     = _build


.PHONY: help test clean build

.DEFAULT: help

help:
	@echo "Please use \`make <target>' where <target> is one of"
	@echo "  clean    to remove build files"
	@echo "  test     to run tests"
	@echo "  doc      to build sphinx documentation"
	@echo "  build    to build pip package"
	@echo "  beta     to increment beta version"
	@echo "  install  to install last version build previsouly"

# Clean build files
clean:
	find . -name "*.pyc" -print0 | xargs -0 rm -rf
	find . -name "__pycache__" -print0 | xargs -0 rm -rf
	-rm -rf htmlcov
	-rm -rf .coverage
	-rm -rf build
	-rm -rf dist
	-rm -rf $(PROJECT).egg-info

doc: build
	-rm -rf $(DOCPATH)/build/*
	mkdir -p $(DOCPATH)/build
	-$(PIP) uninstall $(PROJECT) -y
	$(PIP) install dist/$(PROJECT)-*-py2-none-any.whl --upgrade
	make -C  $(DOCPATH) html;

test:
	$(PYTHON) -m unittest discover -b -v tests


build:
	( \
	$(PYTHON) setup.py sdist bdist_wheel; \
	)

beta:
	$(PYTHON) -c "import $(PROJECT).version; $(PROJECT).version.increment_beta()"
	git add $(PROJECT)/version.py
	git commit -m "increment beta version"
	git push

install:
	( \
	$(PIP) install --upgrade dist/*.whl; \
	)
