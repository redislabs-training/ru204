# redisuniversity/redisconf-2020-gears
FROM redislabs/redisgears:latest

RUN set -ex && \
    apt-get install -y supervisor

# Course files
#ADD .logo /home/student/.logo

# Set permissions
#RUN chown -R student:student /src/redisu
#RUN chown    student:student /home/student/.logo

# Supervisord config
ADD supervisord.conf /etc/

CMD ["supervisord"]

#ENTRYPOINT ["redis-server"]
#CMD ["--loadmodule", "/var/opt/redislabs/lib/modules/redisgears.so", \
#    "PythonHomeDir", "/opt/redislabs/lib/modules/python3"]