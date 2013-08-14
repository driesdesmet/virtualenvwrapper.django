# Quickly bootstrap a Django app using virtualenvwrapper

Requires:
* virtualenvwrapper (install with 'sudo pip install virtualenvwrapper')
* git (only if your project template is a git repo)

## Installation:

    pip install virtualenvwrapper.django_template`

## To use:

    mkproject -t django_template <project_name> <django_boilerplate>

The django_boilerplate argument is anything that the 'django startproject' accepts, meaning:

* a url pointing to an archive, eg.: https://github.com/driesdesmet/django-cms-boilerplate/archive/master.zip
* a local directory

So, if you would like to start a django-cms project within a virtual enviroment that automaticlly sets up a database, fabric
and everything you need to start working on a new website with one command, simply run:

    mkproject -t django_tempolate mynewsite https://github.com/driesdesmet/django-cms-boilerplate/archive/master.zip

Good luck!