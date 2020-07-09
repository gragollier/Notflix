FROM nginx

RUN apt-get update;apt-get install openssh-server unzip -y

RUN echo "root:training" | chpasswd
RUN sed -i 's/prohibit-password/yes/' /etc/ssh/sshd_config
RUN sed -i 's/PermitRootLogin without-password/PermitRootLogin yes/' /etc/ssh/sshd_config
ADD id_rsa.pub /root/
RUN mkdir /root/.ssh
RUN touch /root/.ssh/authorized_keys
RUN chown -R root:root /root/.ssh;chmod -R 700 /root/.ssh
RUN cat /root/id_rsa.pub >> /root/.ssh/authorized_keys

RUN echo “StrictHostKeyChecking=no” >> /etc/ssh/ssh_config
RUN mkdir /var/run/sshd

ADD start.sh /start.sh
RUN chmod +x /start.sh

COPY nginx.conf /etc/nginx/nginx.conf

EXPOSE 22 80

ENTRYPOINT [ "/start.sh" ]

CMD ["nginx", "-g", "daemon off;"]