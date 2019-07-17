# Releasing a new version of AISpace2 on PyPI
By releasing a new version to PyPI, users will be able to get the latest updates whenever they install the extension for the first time or run `pip3 install aispace2 --user --upgrade`. We will assume you have already cloned this repo and have working knowledge of git and GitHub before proceeding.

## Initial Setup

You will need to have a [PyPI](https://pypi.python.org) account _and_ permission to push to our PyPI package name in order to release a new version of AISpace2. If you do not have permission to, have an owner of the project refer to the following instructions:

- Login to [PyPI](https://pypi.python.org/pypi), then go to [this link](https://pypi.python.org/pypi?:action=role_form&package_name=aispace2). You can also search for `aispace2` on PyPI, and  click 'roles'.
- You should see a page like this (_PyPI is undergoing some major changes right now, so this page may look completely different in the near future_): ![role maintenance python package index](https://user-images.githubusercontent.com/955189/29436260-914aa8be-835f-11e7-8e6c-1662ebc6cd98.png)
- Replace `their_pypi_username` with the username they provided you. If you would also like them to be able to add other owners and maintainers (along with the ability to delete the package altogether), set **Role to Add** as **Owner**.
- Click **Add Role**. They should appear under **Existing Roles**.
- They can now release new packages.


Next, you will need to configure the file `~/.pypirc` with the following contents:

```yaml
[distutils]
index-servers =
  pypi
  pypitest

[pypi]
username=pypi username # no quotes or initial space
password=pypi password # no quotes or initial space

[pypitest]
repository=https://test.pypi.org/legacy/
username=pypi username # no quotes or initial space
password=pypi password # no quotes or initial space
```

You may also omit the password line completely, and it will prompt you each time it needs it.

## Release Procedure
1. Check `aispace2/_version.py` and make sure its version is larger than the [currently released version](https://pypi.python.org/pypi/aispace2/).
2. Make sure you are on the master branch (`git checkout master`) and that they are no unpushed changes.
3. Run `python3 setup.py sdist bdist_wheel upload` to upload the package to PyPI. At this point, users should be able to download the new version through `pip`. You may also add `-r pypitest` to the end of that command to upload the package to the [PyPI Test Server](https://testpypi.python.org/pypi/aispace2) and verify everything is the way you expect. 
    - If you get a legacy error of some sort saying that PyPI is now deprecated, make sure you are using an up-to-date version of Python (see [here](https://packaging.python.org/guides/migrating-to-pypi-org/#uploading) for supported version). This is true even if you are using Python 3.3+, since some of the changes were carried out in patch releases.
4. Go to our [Releases](https://github.com/AISpace2/AISpace2/releases) page and click **Draft a new release**.
5. Fill in the tag version and release title with the version specified inside `aispace2/_version.py` and list user-facing changes.
6. Update `aispace2/_version.py` (generally by incrementing minor) to the next version you plan on releasing. You should also update the version number in `js/package.json` for consistency.
7. Run the following commands:  
    ```sh
    git add aispace2/_version.py js/package.json
    git commit -m "Prepare for next version X"
    git push
    ```
8. Run `git fetch --tags` to synchronize the tag you created on GitHub locally. This will be useful if you need to quickly checkout a version to examine a bug, for example.
