
Changelog
=========

v0.3.0 (2026-04-10)
-------------------

* Changed minimum Python to 3.10.
* Added mapping of ANAF locality ids in ``siruta.anaf``.
* Added ``siruta.data.LOCALITY_ALIASES`` - mapping parents to most important child.
  This is not ideal but ANAF uses the parent instead of the child for company data.

v0.2.1 (2025-10-19)
-------------------

* Move ``msgspec`` to optional dependencies (it has some big issues on 3.14). It's not really optional but perhaps a fork may work better on 3.14.

v0.2.0 (2025-10-13)
-------------------

* Replace ``siruta.extras.LOCALITIES_BY_NAME`` with ``siruta.extras.LOCALITIES_BY_COUNTY_ID_BY_NAME`` (to avoid name collisions).

v0.1.1 (2025-10-10)
-------------------

* First release on PyPI.
