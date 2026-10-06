# Dotfiles

Portable configuration managed by [chezmoi](https://www.chezmoi.io/).

## New machine

Install chezmoi, clone this repository, answer the prompts, and apply:

```sh
sh -c "$(curl -fsLS get.chezmoi.io)" -- init --apply git@github.com:alxfox/dotfiles.git
```

If SSH is not configured yet, use the HTTPS repository URL instead.

The initialization prompt stores machine-local values in
`~/.config/chezmoi/chezmoi.toml`. That file is not committed. Choose the Git
identity for each machine. You can also let chezmoi install zsh when it is
missing, opt into Oh My Zsh with Powerlevel10k, and install Caveman for Claude
Code, Codex, both, or neither. Caveman installation requires Node.js and `npx`.

Oh My Zsh and Powerlevel10k are managed as Git repository externals. Oh My Zsh
checks for updates weekly, while Powerlevel10k is pinned to `v1.20.0`. Generate
the machine-local prompt config with `p10k configure`. Force an external refresh
with `chezmoi -R apply`. Caveman is pinned to `v3.1.0`.

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

The managed zsh configuration loads nvm from `$NVM_DIR` (default `~/.nvm`),
or `/usr/share/nvm/init-nvm.sh` when the user installation is absent. It disables
`extendedglob` because it conflicts with nvm alias parsing. On Linux, login
shells load Snap's `/etc/profile.d/apps-bin-path.sh` when present to initialize
command and desktop application paths. These tools are not installed by this
configuration.

Use `~/.zprofile.local` for machine-specific login-shell environment variables
and PATH entries, and `~/.zshrc.local` for interactive aliases and tool
initialization. Chezmoi creates starter versions once, then deliberately leaves
them alone. Managed `.zprofile` sources the private `~/.secrets` file directly.

Use `~/.ssh/config.local` for machine-local SSH hosts and overrides. Chezmoi
creates it with owner-only permissions and does not update it afterwards.

The tmux configuration keeps the default prefix and keybindings, adding mouse
support, a larger history, and `Prefix-R` to reload the file. TPM manages
tmux-resurrect and tmux-continuum; sessions are saved every 15 minutes and
restored when tmux next starts. Use `Prefix-Ctrl-s` and `Prefix-Ctrl-r` for a
manual save and restore, or `Prefix-U` to update plugins. Saved session data is
machine-local and is not committed.

Claude Code and Codex share the same global working conventions. Codex reads a
symlink at `~/.codex/AGENTS.md` pointing to `~/.claude/CLAUDE.md`.

Keep secrets out of this repository. `~/.secrets` is sourced when present and
chezmoi enforces owner-only permissions without managing its contents. A
password manager integration is preferable for values that need to be shared.

To change a machine's answers later, run `chezmoi init --prompt`, inspect with
`chezmoi diff`, then run `chezmoi apply`.
