# xui-manager-panel-frontend

xui-manager-panel 的独立前端仓库，提供静态页面、运行时 API 地址配置和 Nginx 部署脚本。

后端仓库：<https://github.com/HaydenSmith1121/xui-manager-panel-backend>

## 适用场景

- 推荐部署：前端由 Nginx 对外服务，`/api/` 和 `/sub/` 反向代理到后端。浏览器只访问一个域名，Cookie 和跨域配置最简单。
- 分离域名部署：前端和后端使用不同域名，前端 `config.js` 指向后端 API，后端开启 CORS 与跨站 Cookie。
- 纯静态托管：可部署到任意静态站点服务，但需要自行配置 API 地址和后端跨域。

## 一键部署 - 推荐同域模式

先部署后端，并建议只监听本机：

~~~bash
export ADMIN_EMAIL=admin@admin.com
export ADMIN_PASSWORD=请改成强密码
export LISTEN_HOST=127.0.0.1
export LISTEN_PORT=25889
bash <(curl -fsSL https://raw.githubusercontent.com/HaydenSmith1121/xui-manager-panel-backend/main/deploy/install.sh)
~~~

再部署前端，由 Nginx 对外暴露站点并代理后端：

~~~bash
export FRONTEND_SERVER_NAME=_
export FRONTEND_LISTEN_PORT=80
export BACKEND_UPSTREAM=http://127.0.0.1:25889
export ENABLE_BACKEND_PROXY=1
export API_BASE_URL=
bash <(curl -fsSL https://raw.githubusercontent.com/HaydenSmith1121/xui-manager-panel-frontend/main/deploy/install.sh)
~~~

部署完成后访问：

- 前端页面：`http://服务器IP/`
- API 代理：`http://服务器IP/api/...`
- 订阅代理：`http://服务器IP/sub/...`

## 一键部署 - 前后端不同域名

后端需要允许前端来源，并在 HTTPS 下启用跨站 Cookie：

~~~bash
export ADMIN_EMAIL=admin@admin.com
export ADMIN_PASSWORD=请改成强密码
export LISTEN_HOST=0.0.0.0
export LISTEN_PORT=25889
export FRONTEND_ORIGIN=https://front.example.com
export SESSION_COOKIE_SAMESITE=None
export SESSION_COOKIE_SECURE=true
bash <(curl -fsSL https://raw.githubusercontent.com/HaydenSmith1121/xui-manager-panel-backend/main/deploy/install.sh)
~~~

前端关闭后端代理，并把 API 地址写入运行时配置：

~~~bash
export FRONTEND_SERVER_NAME=front.example.com
export FRONTEND_LISTEN_PORT=80
export ENABLE_BACKEND_PROXY=0
export API_BASE_URL=https://api.example.com
bash <(curl -fsSL https://raw.githubusercontent.com/HaydenSmith1121/xui-manager-panel-frontend/main/deploy/install.sh)
~~~

跨域模式建议全站使用 HTTPS；如果 `SESSION_COOKIE_SECURE=true`，浏览器不会在 HTTP 页面发送登录 Cookie。

## 手动静态部署

上传以下文件到静态站点根目录：

- `index.html`
- `app.js`
- `app.css`
- `config.js`
- `favicon.svg`
- `assets/`

然后编辑 `config.js`：

~~~js
window.XUI_MANAGER_API_BASE_URL = "https://api.example.com";
~~~

如果前端和后端同域并由反向代理转发 `/api/` 和 `/sub/`，可保持为空字符串：

~~~js
window.XUI_MANAGER_API_BASE_URL = "";
~~~

## 环境变量

| 变量 | 默认值 | 说明 |
| --- | --- | --- |
| `APP_DIR` | `/var/www/xui-manager-panel-frontend` | 前端部署目录 |
| `REPO_URL` | 本仓库地址 | 前端 Git 仓库地址 |
| `BRANCH` | `main` | 部署分支 |
| `FRONTEND_SERVER_NAME` | `_` | Nginx `server_name` |
| `FRONTEND_LISTEN_PORT` | `80` | Nginx 监听端口 |
| `API_BASE_URL` | 空 | 写入 `config.js` 的后端地址；空表示同源请求 |
| `ENABLE_BACKEND_PROXY` | `1` | 是否由 Nginx 代理 `/api/` 和 `/sub/` |
| `BACKEND_UPSTREAM` | `http://127.0.0.1:25889` | 后端上游地址 |
| `FRONTEND_DEFAULT_SERVER` | `1` | 是否让本前端站点成为 Nginx 默认站点，并移除系统默认站点链接 |
| `NGINX_CONF` | `/etc/nginx/sites-available/xui-manager-panel-frontend.conf` | Nginx 配置文件路径 |
| `NGINX_LINK` | `/etc/nginx/sites-enabled/xui-manager-panel-frontend.conf` | Nginx enabled 链接路径 |

## 升级

~~~bash
export API_BASE_URL=
export ENABLE_BACKEND_PROXY=1
export BACKEND_UPSTREAM=http://127.0.0.1:25889
bash <(curl -fsSL https://raw.githubusercontent.com/HaydenSmith1121/xui-manager-panel-frontend/main/deploy/upgrade.sh)
~~~

升级脚本会拉取最新代码、重写 `config.js`、校验并重载 Nginx。重新安装或升级已有站点时，如果没有显式传入 `FRONTEND_LISTEN_PORT`、`FRONTEND_SERVER_NAME`、`BACKEND_UPSTREAM` 或 `ENABLE_BACKEND_PROXY`，脚本会优先复用现有 Nginx 配置里的 `listen`、`server_name` 和 `proxy_pass`，避免把线上非 80 端口误改回默认值。

### 现有服务器推荐升级命令

如果后端服务监听 `127.0.0.1:25889`，前端 Nginx 对外监听 `25888`，升级脚本现在会尽量自动复用现有端口；生产环境仍建议显式传入端口和 upstream，让操作记录更清楚，也避免首次部署或配置文件缺失时回退到默认 `80`。

~~~bash
export FRONTEND_LISTEN_PORT=25888
export BACKEND_UPSTREAM=http://127.0.0.1:25889
export ENABLE_BACKEND_PROXY=1
export API_BASE_URL=

bash <(curl -fsSL https://raw.githubusercontent.com/HaydenSmith1121/xui-manager-panel-frontend/main/deploy/upgrade.sh)

nginx -t
systemctl reload nginx
ss -lntp | grep -E '25888|25889'
curl -I http://127.0.0.1:25888/
curl -i http://127.0.0.1:25888/api/plans
~~~

正常情况下，`25888` 应由 Nginx 监听，`25889` 应由后端服务监听；`/api/plans` 不应返回 502。

如果部署到 80 端口后 `curl -I http://127.0.0.1/` 返回 Ubuntu 默认欢迎页，说明请求仍落到了系统默认站点。升级脚本默认会使用 `default_server` 并移除 `/etc/nginx/sites-enabled/default` 链接；如需保留系统默认站点，可设置 `FRONTEND_DEFAULT_SERVER=0`。

## 卸载

仅移除 Nginx 站点配置，保留前端文件：

~~~bash
bash <(curl -fsSL https://raw.githubusercontent.com/HaydenSmith1121/xui-manager-panel-frontend/main/deploy/uninstall.sh)
~~~

同时删除前端目录：

~~~bash
export PURGE_APP=1
bash <(curl -fsSL https://raw.githubusercontent.com/HaydenSmith1121/xui-manager-panel-frontend/main/deploy/uninstall.sh)
~~~

## 常用检查

~~~bash
nginx -t
systemctl status nginx --no-pager
curl -I http://127.0.0.1/
curl -I http://127.0.0.1/api/health || true
~~~

## 本地验证

~~~bash
python -m unittest test_frontend
~~~

本仓库是纯静态前端，不需要构建步骤。
