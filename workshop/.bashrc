PS1="\W$ "

if [ ! -f ~/.redw ]; then
   ~/.config/init-container.sh --processid $HOSTNAME > ~/.redw
fi

if [ -f ~/.redw ]; then
   set -a
   source ~/.redw
   set +a
fi

echo "To access your Redis Enterprise Cluster, enter the following:"
echo "redis-cli -h \$REDISHOST -p \$REDISPORT -a \$REDISPASSWORD"