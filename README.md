# Dotfiles

Portable personal and work configuration managed by [chezmoi](https://www.chezmoi.io/).

## New machine

Install chezmoi, clone this repository, answer the profile prompts, and apply:

```sh
sh -c "$(curl -fsLS get.chezmoi.io)" -- init --apply git@github.com:alxfox/dotfiles.git
```

If SSH is not configured yet, use the HTTPS repository URL instead.

The initialization prompt stores machine-local values in
`~/.config/chezmoi/chezmoi.toml`. That file is not committed. Choose the
appropriate profile and Git email for each machine.

## Daily workflow

```sh
chezmoi update       # pull and apply changes
chezmoi diff         # preview local changes
chezmoi add ~/.file  # add or refresh a managed file
chezmoi edit ~/.file # edit source and apply it
chezmoi cd           # open the source repository
```

Run `chezmoi apply --dry-run --verbose` before applying a large change.

## Machine-local configuration

Use `~/.zprofile.local` for login-shell environment variables and PATH entries,
and `~/.zshrc.local` for interactive aliases and tool initialization. Chezmoi
creates starter versions once, then deliberately leaves them alone.

Keep secrets out of this repository. `~/.secrets` is sourced when present and
chezmoi enforces owner-only permissions without managing its contents. A
password manager integration is preferable for values that need to be shared.

To change a machine's answers later, run `chezmoi init --prompt`, inspect with
`chezmoi diff`, then run `chezmoi apply`.
