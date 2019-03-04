PS1="\W$ "

if [ ! -f ~/.redw ]; then
   node ~/.config/init-container.js  --processid $HOSTNAME > ~/.redwrc
fi

if [ -f ~/.redwrc ]; then
   set -a
   source ~/.redwrc
   set +a
fi

if [ -f ~/.logo ]; then
   cat ~/.logo
fi


