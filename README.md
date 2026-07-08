# xui-manager-panel-frontend

独立前端仓库，包含 xui-manager-panel 的静态 UI。

## 部署

把本仓库部署到任意静态站点服务即可，例如 Nginx、Cloudflare Pages、Vercel 或对象存储静态站点。

默认情况下，前端会请求同域的 /api/...。如果后端部署在另一个域名，需要在 index.html 加载 app.js 之前写入：

    <script>
      window.XUI_MANAGER_API_BASE_URL = "https://你的后端域名";
    </script>

也可以在浏览器控制台临时设置：

    localStorage.setItem("XUI_MANAGER_API_BASE_URL", "https://你的后端域名");

跨域部署时，后端需要配置允许的前端来源，并启用跨站 Cookie：

    FRONTEND_ORIGIN=https://你的前端域名
    SESSION_COOKIE_SAMESITE=None
    SESSION_COOKIE_SECURE=true
