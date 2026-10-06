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
chezmoi add ~/.file  # add or refresh a shared file
chezmoi edit ~/.file # edit source and apply it
chezmoi cd           # open the source repository
```

Run `chezmoi apply --dry-run --verbose` before applying a large change.

## Machine-local configuration

| Local entry point | Managed shared configuration | Local contents |
| --- | --- | --- |
| `~/.zshrc` | `~/.zshrc.remote` | Tool initialization, installer additions, interactive overrides |
| `~/.zprofile` | `~/.zprofile.remote` | PATH entries, tool environment, secrets |
| `~/.gitconfig` | `~/.gitconfig.remote` | Identity, signing, credential helpers, local overrides |

Chezmoi creates the entry points only when absent. Each loads its shared file
first; local settings follow. Edit `.remote` files with `chezmoi edit`. Edit
local entry points directly. Do not import local entry points with
`chezmoi add` or `chezmoi re-add`.

Tool installation and initialization, including nvm, Cargo, pnpm, Snap, and
ROS environment settings, remain local. Fresh shell entry points do not
initialize these tools. The local `.zprofile` starter sources `~/.secrets`.
Git identity is seeded from the initialization answers; subsequent identity
changes belong in `~/.gitconfig`, including changes through `git config --global`.

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

## Existing-machine migration

The one-time entry-point migration runs during `chezmoi apply`. It recognizes
the layouts at `00ee7cd` and `1ef8c4e`, preserves appended installer additions,
and folds each former `.local` file into its entry point. Existing tool setup
and Git identity move into the local files. The former `.local` files are
removed after backup. The migration requires Git history containing those
commits, chezmoi, and zsh.

Backups are stored in `~/.local/state/chezmoi/local-entrypoints-backup/`.
Unrecognized layouts stop the migration before any entry-point contents are
changed. For those layouts, manually retain machine-specific settings after
the corresponding `.remote` include and rerun `chezmoi apply`.

> [!NOTE]
> Dry runs show the shared files and migration script, not the script's resulting
> entry-point edits. Existing local entry points are not updated when starter
> templates change.

To roll back, check out the previous repository revision and restore the
entry points and former `.local` files from the backup directory before applying
that revision. Keep backups until all machines have migrated successfully.

Run the isolated migration checks from the repository:

```sh
python3 -m unittest discover -s tests -v
```
