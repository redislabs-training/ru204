PS1="\W$ "

umask 002

if [ -f ~/.logo ]; then
   cat ~/.logo
fi

alias redis-cli6="/usr/local/bin/redis6-cli -p 6370"
