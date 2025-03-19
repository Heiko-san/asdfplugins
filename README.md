# idea

I wanted to be able to update my most important self-contained binary tools in a homogeneous way.
While asdf offers this, it lacks a way to manage/update itself.
Also having each plugin as a separate git repo from different people seems like a security issue to me.
Most of the tools are installed in a very similar way from github, so it seems obvious to have a common code base for this.

# disclaimer

I wrote the plugins with most recent versions / tool update in mind.
If the deployments worked in a different way for some tool in the past, old versions may not be installable with these plugins.
However feel free to open an issue if you need one, I may have a look on it as the requirement pops up.

Only stable versions will be presented, versions like "-rc1" will be removed from the list.

# asdf plugin

This one is special:

- It holds the python module these plugins are based on: `asdf/python3/asdfplugin`.
- If you use `asdf` from its shim, `asdf/bin/exec-env` makes all plugins find this module seamlessly.
- Otherwise install/symlink it into a python path directory.
- The created shim causes `asdf` to endless-loop, to solve this use the following hook in your `~/.asdfrc`:

```
post_asdf_reshim_asdf = sed -i "s|^exec asdf|exec ~/.asdf/installs/asdf/${1}/bin/asdf|" ~/.asdf/shims/asdf
```

- A custom shim would be better to fix this, but at the moment this functionality seems broken: https://github.com/asdf-vm/asdf/issues/2025
