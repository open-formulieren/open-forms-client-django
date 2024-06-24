=========
Changelog
=========

0.4.0
=====

*June 24, 2024*

* Make retrieval of forms lazy to avoid loading forms on
  application startup

0.3.0
=====

*February 13, 2024*

* Add configurable client timeout to config

0.2.3
=====

*November 22, 2022*

* Fixed startup errors due to no configuration present.
* Added more gotcha's to the README.

0.2.2
=====

*October 3, 2022*

* Fixed length of slugfield (default is now 100 instead of 50) which matches
  the slug length in Open Forms.


0.2.1
=====

*September 29, 2022*

* Fixed various documentation issues.


0.2.0
=====

*September 29, 2022*

* Added ``OpenFormsSlugField`` and renamed ``OpenFormsField`` to
  ``OpenFormsUUIDField``.
* Added tests for templatetags.
* Fixed various documentation issues.


0.1.0
=====

*September 27, 2022*

* Initial release
