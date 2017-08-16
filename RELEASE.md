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

- Check `_version.py` and make sure its version is larger than the currently released version
- `python setup.py sdist upload`
- `python setup.py bdist_wheel`
- `git tag -a X.X.X -m 'comment'`. You can also draft a release on GitHub if you prefer (push first).
- Update `_version.py` (generally by incrementing minor)
- `git add` and `git commit`
- `git push`
- `git push --tags` (or `git fetch` if you drafted the release on GitHub so you get the new tags)

If you get a legacy error of some sort saying that PyPI is now deprecated, make sure you are using an up-to-date version of Python (see [here](https://packaging.python.org/guides/migrating-to-pypi-org/#uploading) for supported version).

## To release a new version of aispace2 on NPM:
- Make sure the version number in `js/package.json` is the same as the version you published on PyPI above
- `npm install`
- `npm publish`
- Update the version number in `js/package.json` to reflect the next version
