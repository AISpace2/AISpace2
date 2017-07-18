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

- Update _version.py (set release version, remove 'dev')
- `git add` and `git commit`
- `python setup.py sdist upload -r pypi`
- `python setup.py bdist_wheel`
- `git tag -a X.X.X -m 'comment'`
- Update _version.py (add 'dev' and increment minor)
- `git add` and `git commit`
- `git push`
- `git push --tags`

If you get a legacy error of some sort saying that PyPI is now deprecated, make sure you are using an up-to-date version of Python (see [here](https://packaging.python.org/guides/migrating-to-pypi-org/#uploading) for supported version).

## To release a new version of aispace2 on NPM:

- `git clean -fdx # nuke the  `dist` and `node_modules``
- `npm install`
- `npm publish`
