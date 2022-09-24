

Open Forms Client (for Django)
==============================

:Version: 0.1.0
:Source: https://github.com/open-formulieren/open-forms-client-django
:Keywords: Open Forms, Client, Django
:PythonVersion: 3.7

|build-status| |code-quality| |black| |coverage|

|python-versions| |django-versions| |pypi-version|

About
=====

Easily integrate `Open Forms`_ in your Django application. There are 3 main 
features:

#. Configuration to connect to Open Forms is added to your Django admin.
#. By adding an ``OpenFormsField`` in any Django model, you get a list of forms
   in Open Forms to choose from in the Django admin or other Django forms.
#. You get templatetags to render an Open Forms form in your webpage.

If you have `Sentry`_ installed and you enable Sentry in the Open Forms client
configuration admin page, it will use your existing configuration to connect to
Sentry.

|screenshot-1| |screenshot-2| |screenshot-3|


Installation
============

Requirements
------------

* Python 3.7 or newer
* Django 3.2 or newer

Install
-------

You can install Open Forms Client either via the Python Package Index (PyPI) or 
from source.

To install using ``pip``:

.. code-block:: bash

    pip install open-forms-client-django


Usage
=====

To use this with your project you need to follow these steps:

#. Add ``open_forms_client`` to ``INSTALLED_APPS`` in your Django project's 
   ``settings.py``:

   .. code-block:: python

      INSTALLED_APPS = (
          # ...,
          "open_forms_client",
      )

   Note that there are no dashes in the module name, only underscores.

#. Add an ``OpenFormsField`` to your relevant models:

   .. code-block:: python

      class Page(models.Model):
          # ...
          form = OpenFormsField(blank=True)

#. Add the templatetags to your templates, to render an Open Forms form:

   .. code-block:: html
 
      {% load openforms %}
      <!-- Optional to render Open Forms in the proper language -->
      <html lang="nl">
      <head>
          <!-- Required for icons used by Open Forms -->
          <meta charset="utf-8">
  
          {% openforms_sdk_media %}
      </head>
      <body>
  
      {% if page.form %}
          {% openforms_form page.form %}
      {% else %}
          <p>This page has no form</p>
      {% endif %}
  
      </body>
      </html>

#. Configure your Open Forms connection and settings in the admin, under 
   **Open Forms client configuration**. Once the **status** field shows a green 
   icon, your configuration is working.

#. Done.


Licence
=======

Copyright © `Maykin Media B.V.`_, 2022

Licensed under the `MIT`_.

.. _`Maykin Media B.V.`: https://www.maykinmedia.nl
.. _`MIT`: LICENSE
.. _`Open Forms`: https://github.com/open-formulieren/open-forms
.. _`Sentry`: https://sentry.io/


.. |build-status| image:: https://github.com/open-formulieren/open-forms-client-django/workflows/Run%20CI/badge.svg
    :alt: Build status
    :target: https://github.com/open-formulieren/open-forms-client-django/actions?query=workflow%3A%22Run+CI%22

.. |code-quality| image:: https://github.com/open-formulieren/open-forms-client-django/workflows/Code%20quality%20checks/badge.svg
     :alt: Code quality checks
     :target: https://github.com/open-formulieren/open-forms-client-django/actions?query=workflow%3A%22Code+quality+checks%22

.. |black| image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :target: https://github.com/psf/black

.. |coverage| image:: https://codecov.io/gh/open-formulieren/open-forms-client-django/branch/main/graph/badge.svg
    :target: https://codecov.io/gh/open-formulieren/open-forms-client-django
    :alt: Coverage status

.. |python-versions| image:: https://img.shields.io/pypi/pyversions/open-forms-client.svg

.. |django-versions| image:: https://img.shields.io/pypi/djversions/open-forms-client.svg

.. |pypi-version| image:: https://img.shields.io/pypi/v/open-forms-client.svg
    :target: https://pypi.org/project/open-forms-client/

.. |screenshot-1| image:: https://github.com/open-formulieren/open-forms-client-django/raw/main/docs/_assets/screenshot_admin_config.png
    :alt: Ordered dashboard with dropdown menu.
    :target: https://github.com/open-formulieren/open-forms-client-django/raw/main/docs/_assets/screenshot_admin_config.png

.. |screenshot-2| image:: https://github.com/open-formulieren/open-forms-client-django/raw/main/docs/_assets/screenshot_admin_model_field.png
    :alt: Ordered dashboard with dropdown menu.
    :target: https://github.com/open-formulieren/open-forms-client-django/raw/main/docs/_assets/screenshot_admin_model_field.png

.. |screenshot-3| image:: https://github.com/open-formulieren/open-forms-client-django/raw/main/docs/_assets/screenshot_form_rendering.png
    :alt: Ordered dashboard with dropdown menu.
    :target: https://github.com/open-formulieren/open-forms-client-django/raw/main/docs/_assets/screenshot_form_rendering.png