from pathlib import Path
import unittest


class FrontendTests(unittest.TestCase):
    def test_page_declares_favicon_asset(self):
        root = Path(__file__).resolve().parents[0]
        index_html = (root / "index.html").read_text(encoding="utf-8")
        favicon = root / "favicon.svg"

        self.assertIn('<link rel="icon" type="image/svg+xml" href="./favicon.svg">', index_html)
        self.assertTrue(favicon.exists())
        self.assertIn("<svg", favicon.read_text(encoding="utf-8"))

    def test_mobile_login_dialog_has_non_dialog_browser_fallback(self):
        root = Path(__file__).resolve().parents[0]
        app_js = (root / "app.js").read_text(encoding="utf-8")
        app_css = (root / "app.css").read_text(encoding="utf-8")
        index_html = (root / "index.html").read_text(encoding="utf-8")

        self.assertIn('id="mobileAccountBtn" type="button" class="avatar-button"', index_html)
        self.assertNotIn('id="mobileAccountBtn" type="button" class="avatar-button" data-open-auth', index_html)
        self.assertIn("function openModalDialog", app_js)
        self.assertIn('typeof dialog.showModal === "function"', app_js)
        self.assertIn('dialog.setAttribute("open", "")', app_js)
        self.assertIn('dialog.classList.add("dialog-fallback-open")', app_js)
        self.assertIn(".dialog-fallback-open", app_css)

    def test_public_storefront_header_navigation_is_fixed_for_guests(self):
        root = Path(__file__).resolve().parents[0]
        app_css = (root / "app.css").read_text(encoding="utf-8")

        self.assertIn("Final override: keep the public header fixed", app_css)
        self.assertIn("--guest-topbar-height: 72px", app_css)
        self.assertIn("body.is-guest #storefrontView.storefront", app_css)
        self.assertIn("position: fixed !important", app_css)
        self.assertIn("inset: 0 0 auto 0 !important", app_css)
        self.assertIn("body.is-guest .guest-topbar::before", app_css)
        self.assertIn("scroll-margin-top: calc(var(--guest-topbar-height) + 18px)", app_css)

    def test_theme_and_language_controls_are_available_globally(self):
        root = Path(__file__).resolve().parents[0]
        index_html = (root / "index.html").read_text(encoding="utf-8")
        app_js = (root / "app.js").read_text(encoding="utf-8")
        app_css = (root / "app.css").read_text(encoding="utf-8")

        self.assertIn('id="languageToggleBtn"', index_html)
        self.assertIn('id="themeToggleBtn"', index_html)
        self.assertIn("data-toggle-language", index_html)
        self.assertIn("data-toggle-theme", index_html)
        self.assertIn('localStorage.getItem("xui-theme")', app_js)
        self.assertIn('localStorage.getItem("xui-language")', app_js)
        self.assertIn('localStorage.setItem("xui-theme", theme)', app_js)
        self.assertIn('localStorage.setItem("xui-language", language)', app_js)
        self.assertIn("function applyTheme", app_js)
        self.assertIn("function applyLanguage", app_js)
        self.assertIn("function toggleTheme", app_js)
        self.assertIn("function toggleLanguage", app_js)
        self.assertIn('html[data-theme="dark"]', app_css)
        self.assertIn(".app-toolbar", app_css)
        self.assertIn(".toolbar-chip", app_css)
        self.assertIn("body.is-guest .app-toolbar", app_css)
        self.assertIn("right: max(196px", app_css)
        self.assertIn('html[data-theme="dark"] body.is-guest .guest-plans', app_css)
        self.assertIn('html[data-theme="dark"] body.is-guest .compact-plan-card', app_css)
        self.assertIn('html[data-theme="dark"] body.is-guest .guest-section-heading h2', app_css)

    def test_mobile_guest_flow_arrows_point_down(self):
        app_css = (Path(__file__).resolve().parents[0] / "app.css").read_text(encoding="utf-8")

        self.assertIn("Mobile flow arrows", app_css)
        self.assertIn("body.is-guest .flow-step-arrow::before", app_css)
        self.assertIn('content: "↓" !important', app_css)
        self.assertIn("font-size: 0 !important", app_css)
        self.assertIn('html[data-theme="dark"] body.is-guest .flow-step-arrow::before', app_css)

    def test_mobile_guest_header_auth_button_stays_compact(self):
        app_css = (Path(__file__).resolve().parents[0] / "app.css").read_text(encoding="utf-8")

        self.assertIn("Mobile guest header: keep login action compact", app_css)
        self.assertIn("body.is-guest .guest-topbar > .guest-auth-actions button", app_css)
        self.assertIn("max-width: 94px !important", app_css)
        self.assertIn("height: 34px !important", app_css)
        self.assertIn("font-size: 12px !important", app_css)

    def test_mobile_guest_header_and_flow_shadows_are_removed(self):
        app_css = (Path(__file__).resolve().parents[0] / "app.css").read_text(encoding="utf-8")

        self.assertIn("Mobile guest polish: remove extra header and flow shadows", app_css)
        self.assertIn("body.is-guest .guest-brand .brand-mark", app_css)
        self.assertIn("body.is-guest .flow-step-arrow::before", app_css)
        self.assertIn("box-shadow: none !important", app_css)
        self.assertIn("filter: none !important", app_css)
        self.assertIn("text-shadow: none !important", app_css)
        self.assertIn("background: transparent !important", app_css)

    def test_public_storefront_and_authentication_are_separate(self):
        root = Path(__file__).resolve().parents[0]
        app_js = (root / "app.js").read_text(encoding="utf-8")
        index_html = (root / "index.html").read_text(encoding="utf-8")

        self.assertIn('id="storefrontView"', index_html)
        self.assertIn('id="planCatalog"', index_html)
        self.assertIn('id="authDialog"', index_html)
        self.assertIn('data-auth-tab="login"', index_html)
        self.assertIn('data-auth-tab="register"', index_html)
        self.assertNotIn('id="registerPlan"', index_html)
        self.assertIn("pendingPlanId", app_js)
        self.assertIn("data-apply-plan", app_js)
        self.assertIn('/api/purchases', app_js)
        self.assertIn("submitPurchase", app_js)
        self.assertIn('DEFAULT_STORE_PLANS', app_js)
        self.assertIn('入门套餐', app_js)
        self.assertIn('日常套餐', app_js)
        self.assertIn('畅享套餐', app_js)
        self.assertNotIn('暂无可购买套餐，请联系管理员。', app_js)
        self.assertIn('id="plansSubtitle"', index_html)
        self.assertIn('购买套餐', app_js)
        self.assertIn('三款套餐均可购买，余额充足后可直接开通。', app_js)

    def test_home_and_storefront_are_separate_views(self):
        root = Path(__file__).resolve().parents[0]
        app_js = (root / "app.js").read_text(encoding="utf-8")
        index_html = (root / "index.html").read_text(encoding="utf-8")

        self.assertIn('id="homeView"', index_html)
        self.assertIn('id="storefrontView"', index_html)

        desktop_nav_start = index_html.index('<nav class="nav">')
        desktop_nav = index_html[desktop_nav_start:index_html.index('</nav>', desktop_nav_start)]
        self.assertNotIn('data-view="home"><span>首页</span>', desktop_nav)
        self.assertIn('data-view="storefront"><span>套餐中心</span>', desktop_nav)
        for label in ['套餐中心', '我的订阅', '我的余额', '可用节点', '导入教程', '工单帮助', '用户管理', '卡密管理', '配置模块']:
            self.assertIn(label, desktop_nav)
            self.assertEqual(len(label), 4)
        self.assertIn('class="brand brand-button" type="button" data-view="home"', index_html)

        mobile_nav_start = index_html.index('id="mobileNav"')
        mobile_nav = index_html[mobile_nav_start:index_html.index('</nav>', mobile_nav_start)]
        self.assertNotIn('data-view="home"><span>首页</span>', mobile_nav)
        self.assertIn('data-view="storefront"><span>套餐中心</span>', mobile_nav)
        for label in ['套餐中心', '我的订阅', '我的余额', '可用节点', '导入教程', '工单帮助', '用户管理', '卡密管理', '配置模块']:
            self.assertIn(label, mobile_nav)
            self.assertEqual(len(label), 4)

        self.assertIn('view: "home"', app_js)
        self.assertIn('view = "home"', app_js)
        self.assertIn('setView("storefront")', app_js)

    def test_frontend_has_deliberate_desktop_mobile_and_slow_loading_states(self):
        root = Path(__file__).resolve().parents[0]
        app_js = (root / "app.js").read_text(encoding="utf-8")
        app_css = (root / "app.css").read_text(encoding="utf-8")
        index_html = (root / "index.html").read_text(encoding="utf-8")

        self.assertIn('id="mobileNav"', index_html)
        self.assertIn('id="slowLoader"', index_html)
        self.assertIn('id="userCardList"', index_html)
        self.assertIn(".storefront", app_css)
        self.assertIn(".plan-catalog", app_css)
        self.assertIn(".mobile-nav", app_css)
        self.assertIn(".user-card-list", app_css)
        self.assertIn("position: fixed", app_css)
        self.assertIn("@media (max-width: 920px)", app_css)
        self.assertIn("Authenticated storefront: only show purchasable plans", app_css)
        self.assertIn("body.is-authed #guestHero", app_css)
        self.assertIn("prefers-reduced-motion: reduce", app_css)
        self.assertIn("loadingCount", app_js)
        self.assertIn("600", app_js)
        self.assertIn("elapsed", app_js)

    def test_disabled_user_delete_action_calls_admin_endpoint(self):
        app_js = (Path(__file__).resolve().parents[0] / "app.js").read_text(encoding="utf-8")

        self.assertIn("data-delete-user", app_js)
        self.assertIn('/api/admin/users/delete', app_js)
        self.assertIn('user.status === "disabled"', app_js)

    def test_async_form_errors_are_shown_to_user(self):
        app_js = Path(__file__).resolve().parents[0] / "app.js"
        text = app_js.read_text(encoding="utf-8")

        self.assertIn('window.addEventListener("unhandledrejection"', text)
        self.assertIn("showNotice(message)", text)
        self.assertIn("event.preventDefault()", text)

    def test_nginx_config_can_take_over_default_http_site(self):
        root = Path(__file__).resolve().parents[0]
        install_sh = (root / "deploy" / "install.sh").read_text(encoding="utf-8")
        upgrade_sh = (root / "deploy" / "upgrade.sh").read_text(encoding="utf-8")

        for script in (install_sh, upgrade_sh):
            self.assertIn('FRONTEND_DEFAULT_SERVER="${FRONTEND_DEFAULT_SERVER:-1}"', script)
            self.assertIn("DEFAULT_SERVER_SUFFIX", script)
            self.assertIn('listen ${FRONTEND_LISTEN_PORT}${DEFAULT_SERVER_SUFFIX};', script)
            self.assertIn("/etc/nginx/sites-enabled/default", script)
            self.assertIn("rm -f /etc/nginx/sites-enabled/default", script)
            self.assertNotIn("-L /etc/nginx/sites-enabled/default", script)
            self.assertIn("default_server", script)

    def test_auth_form_errors_render_inside_auth_dialog(self):
        root = Path(__file__).resolve().parents[0]
        app_js = (root / "app.js").read_text(encoding="utf-8")
        app_css = (root / "app.css").read_text(encoding="utf-8")
        index_html = (root / "index.html").read_text(encoding="utf-8")

        self.assertIn('id="authError"', index_html)
        self.assertIn('role="alert"', index_html)
        self.assertIn("function setAuthError", app_js)
        self.assertIn('const isAuthForm = form.closest("#authDialog")', app_js)
        self.assertIn('setAuthError(error?.message || "操作失败")', app_js)
        self.assertIn('setAuthError("")', app_js)
        self.assertIn(".auth-error", app_css)
        self.assertIn('html[data-theme="dark"] .auth-error', app_css)

    def test_save_feedback_stays_visible_and_forms_lock_while_submitting(self):
        root = Path(__file__).resolve().parents[0]
        app_js = (root / "app.js").read_text(encoding="utf-8")
        app_css = (root / "app.css").read_text(encoding="utf-8")

        self.assertIn("async function withSubmitState", app_js)
        self.assertIn('form.dataset.submitting === "true"', app_js)
        self.assertIn("button.disabled = true", app_js)
        self.assertIn("button.disabled = false", app_js)
        self.assertIn('form.querySelector("button[type=submit]")', app_js)
        self.assertIn("position: fixed", app_css)
        self.assertIn("z-index: 100", app_css)

    def test_plan_and_panel_lists_offer_delete_actions(self):
        app_js = (Path(__file__).resolve().parents[0] / "app.js").read_text(encoding="utf-8")

        self.assertIn("data-delete-plan", app_js)
        self.assertIn("data-delete-panel", app_js)
        self.assertIn("/api/admin/plans/delete", app_js)
        self.assertIn("/api/admin/panels/delete", app_js)

    def test_node_list_offers_delete_action(self):
        app_js = (Path(__file__).resolve().parents[0] / "app.js").read_text(encoding="utf-8")

        self.assertIn("data-delete-node", app_js)
        self.assertIn("/api/admin/nodes/delete", app_js)
        self.assertIn("节点已删除", app_js)

    def test_plan_and_panel_forms_have_explicit_create_modes(self):
        root = Path(__file__).resolve().parents[0]
        app_js = (root / "app.js").read_text(encoding="utf-8")
        index_html = (root / "index.html").read_text(encoding="utf-8")

        self.assertIn('id="newPlanBtn"', index_html)
        self.assertIn('id="newPanelBtn"', index_html)
        self.assertIn('id="planFormTitle"', index_html)
        self.assertIn('id="panelFormTitle"', index_html)
        self.assertIn("function resetPlanForm", app_js)
        self.assertIn("function resetPanelForm", app_js)
        self.assertIn('form.elements.id.value = ""', app_js)
        self.assertIn('title.textContent = `编辑${label}', app_js)

    def test_frontend_offers_logout_and_clears_local_session_state(self):
        root = Path(__file__).resolve().parents[0]
        app_js = (root / "app.js").read_text(encoding="utf-8")
        index_html = (root / "index.html").read_text(encoding="utf-8")

        self.assertIn('id="logoutBtn"', index_html)
        self.assertNotIn('<div class="session">', index_html)
        profile_start = index_html.index('id="profileView"')
        profile_block = index_html[profile_start:index_html.index('id="adminView"', profile_start)]
        self.assertIn('id="logoutBtn"', profile_block)
        self.assertIn('api("/api/logout"', app_js)
        self.assertIn("state.me = null", app_js)
        self.assertIn('$("#loginForm").reset()', app_js)
        self.assertIn('setView("home")', app_js)
        self.assertIn('showNotice("已退出登录")', app_js)

    def test_subscription_copy_falls_back_without_clipboard_api(self):
        app_js = (Path(__file__).resolve().parents[0] / "app.js").read_text(encoding="utf-8")

        self.assertIn("async function copyTextFromInput", app_js)
        self.assertIn("navigator.clipboard", app_js)
        self.assertIn("document.execCommand", app_js)
        self.assertIn("input.select()", app_js)

    def test_frontend_exposes_managed_provisioning_actions(self):
        root = Path(__file__).resolve().parents[0]
        app_js = (root / "app.js").read_text(encoding="utf-8")

        self.assertIn("data-retry-provision", app_js)
        self.assertIn("data-reconcile-user", app_js)
        self.assertIn("/api/admin/users/provision/retry", app_js)
        self.assertIn("/api/admin/users/reconcile", app_js)
        self.assertIn("provisioningSummary", app_js)
        self.assertIn("provisioningErrorSummary", app_js)
        self.assertIn("provisioning_errors", app_js)

    def test_frontend_exposes_panel_testing_and_inbound_picker(self):
        root = Path(__file__).resolve().parents[0]
        app_js = (root / "app.js").read_text(encoding="utf-8")
        index_html = (root / "index.html").read_text(encoding="utf-8")

        self.assertIn("data-test-panel", app_js)
        self.assertIn("data-fetch-inbounds", app_js)
        self.assertIn("/api/admin/panels/test", app_js)
        self.assertIn("/api/admin/panels/inbounds", app_js)
        self.assertIn('id="inboundOptions"', index_html)

    def test_frontend_exposes_sync_settings_form(self):
        root = Path(__file__).resolve().parents[0]
        app_js = (root / "app.js").read_text(encoding="utf-8")
        index_html = (root / "index.html").read_text(encoding="utf-8")

        self.assertIn('id="settingsForm"', index_html)
        self.assertIn('name="sync_interval_seconds"', index_html)
        self.assertIn('name="subscription_title"', index_html)
        self.assertIn("/api/admin/settings", app_js)
        self.assertIn("renderSettings", app_js)

    def test_panel_password_field_explains_blank_edit_behavior(self):
        root = Path(__file__).resolve().parents[0]
        app_js = (root / "app.js").read_text(encoding="utf-8")
        index_html = (root / "index.html").read_text(encoding="utf-8")

        self.assertIn('id="panelPasswordHelp"', index_html)
        self.assertIn("留空保留已保存密码", index_html)
        self.assertIn("panelPasswordHelp", app_js)

    def test_plan_and_panel_create_actions_open_list_level_dialogs(self):
        root = Path(__file__).resolve().parents[0]
        app_js = (root / "app.js").read_text(encoding="utf-8")
        index_html = (root / "index.html").read_text(encoding="utf-8")

        self.assertIn('id="planDialog"', index_html)
        self.assertIn('id="panelDialog"', index_html)
        self.assertIn('id="newPlanBtn"', index_html)
        self.assertIn('id="newPanelBtn"', index_html)
        self.assertIn('name="price_yuan"', index_html)
        self.assertIn('$("#planDialog").showModal()', app_js)
        self.assertIn('$("#panelDialog").showModal()', app_js)

    def test_balance_purchase_recharge_and_multi_client_subscription_controls_exist(self):
        root = Path(__file__).resolve().parents[0]
        app_js = (root / "app.js").read_text(encoding="utf-8")
        index_html = (root / "index.html").read_text(encoding="utf-8")

        self.assertIn('id="balanceText"', index_html)
        self.assertIn('id="rechargeForm"', index_html)
        self.assertIn('Clash Verge / Mihomo（支持 VLESS；旧版 Clash 可能不兼容）', index_html)
        self.assertIn('data-sub-format="clash"', index_html)
        self.assertIn('data-sub-format="base64"', index_html)
        self.assertIn('data-sub-format="singbox"', index_html)
        self.assertIn('/api/recharge', app_js)
        self.assertIn('/api/purchases', app_js)
        self.assertIn("subscription_urls", app_js)
        self.assertNotIn("state.me.email ||", app_js)

    def test_subscription_one_click_import_controls_exist(self):
        root = Path(__file__).resolve().parents[0]
        app_js = (root / "app.js").read_text(encoding="utf-8")
        app_css = (root / "app.css").read_text(encoding="utf-8")
        index_html = (root / "index.html").read_text(encoding="utf-8")

        for client in (
            "clash-verge",
            "mihomo",
            "clash",
            "shadowrocket",
            "singbox",
            "v2rayng",
            "hiddify",
        ):
            self.assertIn(f'data-import-client="{client}"', index_html)

        self.assertIn("function subscriptionUrlForFormat", app_js)
        self.assertIn("function importUrlForClient", app_js)
        self.assertIn("function renderImportButtons", app_js)
        self.assertIn("async function launchImport", app_js)
        self.assertIn("encodeURIComponent", app_js)
        self.assertIn("clash://install-config?url=", app_js)
        self.assertIn('return "clash://install-config?url=" + encodeURIComponent(url);', app_js)
        self.assertNotIn('"&name=" +', app_js)
        self.assertIn("shadowrocket://", app_js)
        self.assertIn("data-import-client", app_js)
        self.assertIn("window.location.href", app_js)
        self.assertIn(".client-import-grid", app_css)
        self.assertIn(".client-import-button", app_css)

    def test_personal_center_avatar_profile_and_settings_exist(self):
        root = Path(__file__).resolve().parents[0]
        app_js = (root / "app.js").read_text(encoding="utf-8")
        app_css = (root / "app.css").read_text(encoding="utf-8")
        index_html = (root / "index.html").read_text(encoding="utf-8")

        for marker in (
            'id="profileEntryBtn"',
            'id="profileView"',
            'id="profileAvatarInput"',
            'id="expireReminderToggle"',
            'id="trafficReminderToggle"',
            'id="profileGiftCardForm"',
            'id="profileGiftCardBalance"',
            'id="profilePasswordForm"',
            'class="profile-list"',
            "礼品卡兑换",
        ):
            self.assertIn(marker, index_html)
        profile_start = index_html.index('id="profileView"')
        profile_block = index_html[profile_start:index_html.index('id="adminView"', profile_start)]
        self.assertNotIn('id="checkinPanel"', profile_block)
        self.assertNotIn('自动续费', profile_block)
        self.assertNotIn('订阅信息', profile_block)
        self.assertNotIn('id="profileSubscriptionInfo"', profile_block)
        self.assertNotIn('id="profileSubscriptionUrl"', profile_block)
        self.assertNotIn('data-copy-profile-sub', profile_block)
        self.assertIn("renderProfile", app_js)
        self.assertNotIn("data-copy-profile-sub", app_js)
        self.assertNotIn("#profileSubscriptionUrl", app_js)
        self.assertNotIn("profileSubStatus", app_js)
        self.assertIn("/api/me/password", app_js)
        self.assertIn("礼品卡兑换成功，余额已到账", app_js)
        self.assertIn("profileEntryLabel", app_js)
        self.assertNotIn('$("#sessionEmail")', app_js)
        self.assertIn(".profile-entry", app_css)
        self.assertIn(".profile-list", app_css)
        self.assertIn(".gift-card-panel", app_css)

    def test_user_list_has_search_filters_collapse_notes_and_balance_tools(self):
        root = Path(__file__).resolve().parents[0]
        app_js = (root / "app.js").read_text(encoding="utf-8")
        index_html = (root / "index.html").read_text(encoding="utf-8")

        for marker in ('id="userSearch"', 'id="userStatusFilter"', 'id="userRoleFilter"', 'id="priorityFilter"', 'id="toggleUserListBtn"'):
            self.assertIn(marker, index_html)
        self.assertIn("data-user-note-form", app_js)
        self.assertIn("data-user-balance-form", app_js)
        self.assertIn('/api/admin/users/note', app_js)
        self.assertIn('/api/admin/users/balance', app_js)
        self.assertIn("filteredUsers", app_js)

    def test_admin_recharge_card_generator_is_available(self):
        root = Path(__file__).resolve().parents[0]
        app_js = (root / "app.js").read_text(encoding="utf-8")
        app_css = (root / "app.css").read_text(encoding="utf-8")
        index_html = (root / "index.html").read_text(encoding="utf-8")

        self.assertIn('id="rechargeCardsView"', index_html)
        self.assertIn('id="rechargeCardForm"', index_html)
        self.assertIn('id="rechargeCardList"', index_html)
        recharge_start = index_html.index('id="rechargeCardsView"')
        recharge_block = index_html[recharge_start:index_html.index('id="configView"', recharge_start)]
        admin_start = index_html.index('id="adminView"')
        admin_block = index_html[admin_start:index_html.index('id="rechargeCardsView"', admin_start)]
        self.assertIn('id="rechargeCardForm"', recharge_block)
        self.assertNotIn('返回用户管理', recharge_block)
        self.assertNotIn('id="rechargeCardForm"', admin_block)
        self.assertIn('/api/admin/recharge-cards', app_js)
        self.assertIn('/api/admin/recharge-cards/reveal', app_js)
        self.assertIn('/api/admin/recharge-cards/delete', app_js)
        self.assertIn("data-reveal-card", app_js)
        self.assertIn("data-copy-card", app_js)
        self.assertIn("data-delete-card", app_js)
        self.assertIn("充值卡已删除", app_js)
        self.assertIn("generatedCardCodes", app_js)
        self.assertIn('.recharge-admin-panel .inline-form', app_css)
        self.assertIn('margin-top: 0 !important', app_css)
        self.assertIn('min-height: clamp(460px, 58vh, 640px)', app_css)
        self.assertIn('grid-column: 1 / -1', app_css)

    def test_recharge_card_delete_not_found_removes_local_card(self):
        app_js = (Path(__file__).resolve().parents[0] / "app.js").read_text(encoding="utf-8")

        self.assertIn("function isNotFoundError", app_js)
        self.assertIn("function removeRechargeCardLocally", app_js)
        self.assertIn("isNotFoundError(error)", app_js)
        self.assertIn("接口返回 Not found，已从当前列表移除这张充值卡", app_js)

    def test_admin_configuration_sections_are_split_into_module_pages(self):
        root = Path(__file__).resolve().parents[0]
        app_js = (root / "app.js").read_text(encoding="utf-8")
        index_html = (root / "index.html").read_text(encoding="utf-8")
        app_css = (root / "app.css").read_text(encoding="utf-8")

        self.assertIn('data-view="config"><span>配置模块</span>', index_html)
        self.assertNotIn('data-view="nodes"><span>节点配置</span>', index_html)
        self.assertNotIn('data-view="settings"><span>配置</span>', index_html)
        for view_id in [
            "configView",
            "configNodesView",
            "configSystemView",
            "configCheckinView",
            "configTutorialsView",
            "configPlansView",
            "configPanelsView",
        ]:
            self.assertIn(f'id="{view_id}"', index_html)
        for view in ["configNodes", "configSystem", "configCheckin", "configTutorials", "configPlans", "configPanels"]:
            self.assertIn(f'data-view="{view}"', index_html)
        self.assertIn("CONFIG_VIEWS", app_js)
        self.assertIn("LEGACY_ADMIN_VIEW_ALIASES", app_js)
        self.assertIn('setView("configNodes")', app_js)
        self.assertIn('setView("configTutorials")', app_js)
        self.assertIn(".config-module-grid", app_css)

    def test_checkin_uses_lightweight_button_state_without_global_loader(self):
        root = Path(__file__).resolve().parents[0]
        app_js = (root / "app.js").read_text(encoding="utf-8")
        app_css = (root / "app.css").read_text(encoding="utf-8")

        self.assertIn("silent = false", app_js)
        self.assertIn("if (!silent) beginLoading(loadingLabel)", app_js)
        self.assertIn('api("/api/checkin", { method: "POST", body: "{}", silent: true })', app_js)
        self.assertIn("item.classList.add(\"is-loading\")", app_js)
        self.assertIn("item.classList.remove(\"is-loading\")", app_js)
        self.assertIn("refreshUserBackgroundData", app_js)
        self.assertIn("function scheduleUserBackgroundDataRefresh", app_js)
        self.assertIn("void refreshUserBackgroundData().catch", app_js)
        self.assertIn('const buttons = $$("[data-checkin]")', app_js)
        self.assertIn("buttons.forEach", app_js)
        self.assertIn("Promise.allSettled", app_js)
        self.assertIn(".checkin-icon-action.is-loading::after", app_css)
        self.assertIn(".checkin-panel [data-checkin].is-loading::after", app_css)

    def test_admin_requested_ui_refinements_are_present(self):
        root = Path(__file__).resolve().parents[0]
        app_js = (root / "app.js").read_text(encoding="utf-8")
        app_css = (root / "app.css").read_text(encoding="utf-8")

        self.assertIn("activeAdminTicketId", app_js)
        self.assertIn("data-select-admin-ticket", app_js)
        self.assertIn("admin-ticket-chat", app_js)
        self.assertIn("admin-ticket-thread", app_js)
        self.assertIn("admin-ticket-conversation", app_js)
        self.assertIn("admin-ticket-messages", app_js)
        self.assertIn("admin-ticket-composer", app_js)

        self.assertIn("body.is-authed #rechargeCardsView .recharge-card-layout", app_css)
        self.assertIn("body.is-authed #rechargeCardsView .recharge-admin-panel", app_css)
        self.assertIn("body.is-authed #rechargeCardsView .recharge-card-list-panel", app_css)
        self.assertIn("min-height: clamp(460px, 58vh, 640px)", app_css)
        self.assertIn("rgba(239, 246, 255", app_css)
        self.assertIn(".admin-ticket-chat", app_css)
        self.assertIn(".admin-ticket-thread", app_css)
        self.assertIn(".admin-ticket-conversation", app_css)
        self.assertIn(".admin-ticket-bubble", app_css)

    def test_ticket_help_page_keeps_scroll_inside_panels(self):
        root = Path(__file__).resolve().parents[0]
        index_html = (root / "index.html").read_text(encoding="utf-8")
        app_js = (root / "app.js").read_text(encoding="utf-8")
        app_css = (root / "app.css").read_text(encoding="utf-8")

        self.assertIn('class="ticket-workbench"', index_html)
        self.assertIn('class="ticket-chat-shell"', index_html)
        self.assertIn('class="ticket-sidebar"', index_html)
        self.assertIn('id="ticketConversationPane"', index_html)
        self.assertIn("admin-conversation-list", index_html)
        self.assertIn("renderTicketConversationPane", app_js)
        self.assertIn("ticket-conversation-pane", app_js)
        self.assertIn("Ticket help redesign: conversation workbench", app_css)
        self.assertIn("body.is-authed #ticketsView.tickets-workspace", app_css)
        self.assertIn("height: 100svh !important", app_css)
        self.assertIn("overflow: hidden !important", app_css)
        self.assertIn("grid-template-columns: minmax(280px, 340px) minmax(0, 1fr)", app_css)
        self.assertIn(".ticket-conversation-pane", app_css)
        self.assertIn(".ticket-empty-conversation", app_css)
        self.assertIn("overflow: auto !important", app_css)
        self.assertIn('html[data-theme="dark"] .ticket-workbench', app_css)

    def test_node_status_menu_switch_does_not_shift_page_sideways(self):
        root = Path(__file__).resolve().parents[0]
        app_css = (root / "app.css").read_text(encoding="utf-8")

        self.assertIn("scrollbar-gutter: stable", app_css)
        self.assertIn("overflow-y: scroll", app_css)
        self.assertIn("#nodeStatusView.view", app_css)
        self.assertIn("animation: node-status-view-fade", app_css)
        self.assertIn("transform: none !important", app_css)
        self.assertIn("will-change: opacity", app_css)

    def test_utility_pages_fill_available_main_width(self):
        app_css = (Path(__file__).resolve().parents[0] / "app.css").read_text(encoding="utf-8")

        self.assertIn("Authenticated utility pages: remove side gutters", app_css)
        for selector in [
            "body.is-authed #nodeStatusView.node-status-workspace",
            "body.is-authed #guideView.guide-workspace",
            "body.is-authed #ticketsView.tickets-workspace",
        ]:
            self.assertIn(selector, app_css)
        self.assertIn("margin-inline: 0 !important", app_css)
        self.assertIn("width: 100% !important", app_css)
        self.assertIn("max-width: none !important", app_css)
        self.assertIn("body.is-authed #ticketsView .ticket-workbench", app_css)
        self.assertIn("body.is-authed #guideView #publicTutorialList.tutorial-list", app_css)
        self.assertIn("body.is-authed #nodeStatusView #nodeStatusList", app_css)

    def test_menu_view_switches_use_no_position_animation(self):
        root = Path(__file__).resolve().parents[0]
        app_css = (root / "app.css").read_text(encoding="utf-8")

        view_block = app_css[app_css.index(".view {"):app_css.index("@keyframes view-enter")]
        keyframes_block = app_css[app_css.index("@keyframes view-enter"):app_css.index(".home {", app_css.index("@keyframes view-enter"))]

        self.assertIn("animation: view-enter 180ms ease-out both", view_block)
        self.assertIn("transform: none", view_block)
        self.assertIn("from { opacity: 0; }", keyframes_block)
        self.assertIn("to { opacity: 1; }", keyframes_block)
        self.assertNotIn("translateY(8px)", keyframes_block)
        self.assertNotIn("translateY(0)", keyframes_block)


if __name__ == "__main__":
    unittest.main()
class SplitFrontendConfigTests(unittest.TestCase):
    def test_frontend_supports_configurable_api_base_url(self):
        root = Path(__file__).resolve().parents[0]
        app_js = (root / "app.js").read_text(encoding="utf-8")
        index_html = (root / "index.html").read_text(encoding="utf-8")

        self.assertIn("XUI_MANAGER_API_BASE_URL", app_js)
        self.assertIn("function apiUrl", app_js)
        self.assertIn("fetch(apiUrl(path)", app_js)
        self.assertIn('credentials: API_BASE_URL ? "include" : "same-origin"', app_js)
        self.assertIn('href="./app.css"', index_html)
        self.assertIn('src="./app.js"', index_html)
