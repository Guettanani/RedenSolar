FROM nginx:latest

COPY ./default.conf /etc/nginx/conf.d/default.conf

# Copier le script d'entrée
COPY entrypoint.sh /usr/local/bin/entrypoint.sh

# Donner les permissions d'exécution au script
#RUN chmod +x /usr/local/bin/entrypoint.sh

# Définir l'entrée CMD pour utiliser le script
#ENTRYPOINT ["sh","/usr/local/bin/entrypoint.sh"]
