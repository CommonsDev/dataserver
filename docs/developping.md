

Hello Unisson/Commons developpers. 


## Git-flow

The config is all by default, except `versiontag` which is `dataserver-`, to get nice versions numbers (eg `git flow release … 1.2.3` produces a tag/version named `dataserver-1.2.3`).

```
[gitflow "prefix"]
        feature = feature/
        release = release/
        hotfix = hotfix/
        support = support/
        versiontag = dataserver-
```

If you already released a version without this configuration, you can always rename a tag before pushing, with the following `git` alias in you `~/.gitconfig`:

```
mvtag = !sh -c 'git tag $1 $0 && git tag -d $0 && git push origin :refs/tags/$0'
```

And then `git mvtag old_version dataserver-old_version`



## Release management

To easily release new data-server versions, include the following snippet in your shell .RC file:

```
function dataserver_release() {

    if ! grep -q 'version = ' dataserver/__init__.py >/dev/null 2>&1; then
        echo "must be in dataserver project root."
        return
    fi

    if [[ -z "${1}" ]]; then
        grep version dataserver/__init__.py | tr -d "'" \
            | sed -e 's/^version =/current version:/'

    else
        NEED_STASH=`git --no-pager diff --shortstat`

        if [[ -n "${NEED_STASH}" ]]; then git stash; fi

        echo "Creating release ${1}…"
        git rs ${1} || return

        echo -e "\nversion = '${1}'\n" > dataserver/__init__.py
        git add dataserver/__init__.py
        git commit -m "version bump for ${1}."

        git rf -m ${1} ${1}
        echo "Done creating release ${1}."

        if [[ -n "${NEED_STASH}" ]]; then git stash pop; fi
    fi
}

```
