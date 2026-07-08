#!/usr/bin/env bash
set -euo pipefail

APP_NAME="xui-manager-panel-frontend"
APP_DIR="${APP_DIR:-/var/www/xui-manager-panel-frontend}"
NGINX_CONF="${NGINX_CONF:-/etc/nginx/sites-available/${APP_NAME}.conf}"
NGINX_LINK="${NGINX_LINK:-/etc/nginx/sites-enabled/${APP_NAME}.conf}"
PURGE_APP="${PURGE_APP:-0}"

if [ "$(id -u)" -ne 0 ]; then
  echo "Please run this uninstaller as root."
  exit 1
fi

rm -f "$NGINX_LINK" "$NGINX_CONF"

if command -v nginx >/dev/null 2>&1; then
  nginx -t && systemctl reload nginx || true
fi

if [ "$PURGE_APP" = "1" ]; then
  case "$APP_DIR" in
    /var/www/xui-manager-panel-frontend|/opt/xui-manager-panel-frontend)
      rm -rf "$APP_DIR"
      echo "Removed ${APP_DIR}."
      ;;
    *)
      echo "Refusing to remove unsafe APP_DIR: ${APP_DIR}"
      exit 1
      ;;
  esac
fi

echo "Uninstalled ${APP_NAME}."
