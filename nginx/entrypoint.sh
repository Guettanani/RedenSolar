

# Créer le répertoire /var/www/react/ s'il n'existe pas
mkdir -p /var/www/react/

# Appliquer les permissions au répertoire racine
chmod -R o+r /var/www/react/

# Lancer la commande d'origine de l'entrypoint
exec "$@"