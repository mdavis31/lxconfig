# .bashrc

# Source global definitions
if [ -f /etc/bashrc ]; then
	. /etc/bashrc
fi

# User specific environment
if ! [[ "$PATH" =~ "$HOME/.local/bin:$HOME/bin:" ]]
then
    PATH="$HOME/.local/bin:$HOME/bin:$PATH"
fi
export PATH

# Uncomment the following line if you don't like systemctl's auto-paging feature:
# export SYSTEMD_PAGER=

# User specific aliases and functions
alias l='exa --group-directories-first'
alias ll='exa -lg --group-directories-first'
alias ls='exa -lag --group-directories-first'
alias lm='exa -lgs modified --group-directories-first'
alias lmr='exa -lgs modified --group-directories-first --reverse'
alias konsave='python -m konsave'
alias xcopy='xclip -sel clip'

if [ -d ~/.bashrc.d ]; then
	for rc in ~/.bashrc.d/*; do
		if [ -f "$rc" ]; then
			. "$rc"
		fi
	done
fi

unset rc
