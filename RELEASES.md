# Tagging

Check version and edit pyproject.toml:

  ```
  version = "1.0.2"
  ```

Push all changes:

```shell
git commit -a
git push
```

_After pushing the last commit_, add a local tag (shall be added AFTER the commit):

```shell
git tag # list local tags
git tag v1.0.2
```

Push this tag to the origin, which starts the publish workflow (GitHub Action):

```shell
git push origin v1.0.2
git ls-remote --tags https://github.com/Ircama/pysnmp-sync-adapter # list remote tags
```

Check the published tag here: https://github.com/Ircama/pysnmp-sync-adapter/tags

It shall be even with the last commit.

Check the GitHub Action: https://github.com/Ircama/pysnmp-sync-adapter/actions

# Updating the same tag (using a different build number for publishing)

Example: small documentation update to version 1.0.2

- Update the README.md file

- Edit pyproject.toml and add [".post1" to the version](https://packaging.python.org/en/latest/specifications/version-specifiers/)
  ```
  version = "1.0.2.post1"
  ```

- `git push --delete origin v1.0.2`
- `git tag -d v1.0.2`
- `git commit -a --amend`
- `git push --force`
- `git tag v1.0.2 && git push origin v1.0.2`

```shell
git tag # list tags
git ls-remote --tags https://github.com/Ircama/pysnmp-sync-adapter # list remote tags
```

# PyPI

- https://pypi.org/project/pysnmp-sync-adapter/
- https://test.pypi.org/project/pysnmp-sync-adapter/
