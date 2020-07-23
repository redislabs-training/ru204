PS1="\W$ "

if [ ! -f /src/redisu/project/README.md ]; then
   /home/student/get_project_source.sh
   clear
fi

if [ -f ~/.logo ]; then
   cat ~/.logo
fi

alias python="/usr/local/bin/python3.8"