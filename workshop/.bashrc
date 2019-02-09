PS1="\W$ "

~/.config/init-container.sh --processid $HOSTNAME > ~/.redw

if [ -f ~/.redw ]; then
   set -a
   source ~/.redw
   set +a
fi
