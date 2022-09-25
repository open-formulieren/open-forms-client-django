

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

If you have `Sentry`_ installed and you enable Sentry in the Django admin
configuration page, it will use your existing configuration to connect to
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

    pip install django-open-forms-client


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

#. Add an ``OpenFormsField`` to your relevant models (like a ``Page`` model):

   .. code-block:: python

      class Page(models.Model):
          # ...
          form = OpenFormsField(blank=True)

#. Add the templatetags ``{% openforms_sdk_media %}`` and 
   ``{% openforms_form page.form %}`` to your templates, to render an Open 
   Forms form:

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


Templatetags
------------

There are 4 templatetags available with several parameters. All parameters
translate to `Open Forms SDK`_ parameters.

.. code-block:: python

   openforms_form(form_id, csp_nonce=None, base_path=None, lang=None, html_id=None)
   openforms_sdk_media()
   openforms_sdk_js()
   openforms_sdk_css()


Gotcha's
--------

Open Forms configuration
~~~~~~~~~~~~~~~~~~~~~~~~

Make sure the domain where you host your webapplication is in the Open Forms
``ALLOWED_HOSTS`` setting. Note that this is **not** the setting in your own
webapplication but in the setting in the Open Forms installation.


CPS headers
~~~~~~~~~~~

When your webapplication uses `CSP headers`_ you need to pass the ``csp_nonce``
to the ``openforms_form`` templatetag as well. If you use `Django-CSP`_ you can
do this:
   
.. code-block:: html
 
   {% load openforms %}
   {% openforms_form page.form csp_nonce=csp_nonce=request.csp_nonce %}

Additionally, you need to allow your webapplication to load styles and scripts 
from the Open Forms SDK and connect to the Open Forms API. When using 
`Django-CSP`_ some options need to be changed in your ``settings.py``:

.. code-block:: python

    # The Open Forms SDK files might differ from the API domain.
    OPEN_FORMS_API_DOMAIN = "forms.example.com"
    OPEN_FORMS_SDK_DOMAIN = OPEN_FORMS_API_DOMAIN

    # Allow your webapp to load styles from Open Forms SDK.
    CSP_STYLE_SRC = ("'self'", OPEN_FORMS_SDK_DOMAIN)

    # Allow your webapp to load script from Open Forms SDK.
    CSP_SCRIPT_SRC = ("'self'", OPEN_FORMS_SDK_DOMAIN)

    # Allow your webapp to load images from Open Forms SDK.
    CSP_IMG_SRC = ("'self'", OPEN_FORMS_SDK_DOMAIN)

    # Allow your webapp to load fonts from Open Forms SDK.
    CSP_FONT_SRC = ("'self'", OPEN_FORMS_SDK_DOMAIN)

    # Allow your webapp to connect to the Open Forms API.
    CSP_CONNECT_SRC = ("'self'", OPEN_FORMS_API_DOMAIN)


Make page refreshes work
~~~~~~~~~~~~~~~~~~~~~~~~

The URL changes when you start a form, indicating the step you are currently 
on. Refreshing the page will result in a HTTP 404 because this URL does not 
actually exist. You need to catch these URL-patterns and redirect the user 
back to the form. You can so like this:

.. code-block:: python
   
   # urls.py
   
   # The view thats starts the form
   path("page/<slug:slug>", PageView.as_view(), name="page"),
   # Whenever you refresh the page that has the form, the URL might be changed
   # and needs to redirect the user to the start of the form.
   re_path("^page/(?P<slug>\w+)/", FormRedirectView.as_view()),


Licence
=======

Copyright © `Maykin Media B.V.`_, 2022

Licensed under the `MIT`_.

.. _`Maykin Media B.V.`: https://www.maykinmedia.nl
.. _`MIT`: LICENSE
.. _`Open Forms`: https://github.com/open-formulieren/open-forms
.. _`Open Forms SDK`: https://github.com/open-formulieren/open-forms-sdk
.. _`Sentry`: https://sentry.io/
.. _`CSP headers`: https://developer.mozilla.org/en-US/docs/Web/HTTP/CSP
.. _`Django-CSP`: https://github.com/mozilla/django-csp

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
    :width: 49%

.. |screenshot-3| image:: https://github.com/open-formulieren/open-forms-client-django/raw/main/docs/_assets/screenshot_form_rendering.png
    :alt: Ordered dashboard with dropdown menu.
    :target: https://github.com/open-formulieren/open-forms-client-django/raw/main/docs/_assets/screenshot_form_rendering.png
    :width: 50%
