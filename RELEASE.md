## To release a new version of aispace2 on PyPI:

First make sure you have `~/.pypirc` setup, with the following contents:

```yaml
[distutils]
index-servers =
  pypi
  pypitest

[pypi]
username=pypi username
password=pypi password

[pypitest]
repository=https://test.pypi.org/legacy/
username=pypi username
password=pypi password
```

- Update `_version.py` if necessary, removing 'dev' if this is a production release
- `git add` and `git commit` the version changes
- `python setup.py sdist upload`
- `python setup.py bdist_wheel`
- `git tag -a X.X.X -m 'comment'`. You can also draft a release on GitHub if you prefer.
- Update `_version.py` (add 'dev' and increment minor)
- `git add` and `git commit`
- `git push`
- `git push --tags`

If you get a legacy error of some sort saying that PyPI is now deprecated, make sure you are using an up-to-date version of Python (see [here](https://packaging.python.org/guides/migrating-to-pypi-org/#uploading) for supported version).

## To release a new version of aispace2 on NPM:
- Update the version number in `js/package.json` to match the version you published in Python
- `npm install`
- `npm publish`
