// Theme Management with LocalStorage
const lightModeButton = document.querySelector(".theme-toggle-light");
const darkModeButton = document.querySelector(".theme-toggle-dark");

// Load saved theme from localStorage
function loadSavedTheme() {
    const savedTheme = localStorage.getItem('theme');

    if (savedTheme === 'dark') {
        document.body.classList.add('dark');
        lightModeButton.style.display = "none";
        darkModeButton.style.display = "block";
    } else {
        document.body.classList.remove('dark');
        lightModeButton.style.display = "block";
        darkModeButton.style.display = "none";
    }
}

// Save theme to localStorage
function saveTheme(theme) {
    localStorage.setItem('theme', theme);
}

// Theme Toggle Functionality
lightModeButton.addEventListener("click", () => {
    document.body.classList.add("dark");
    lightModeButton.style.display = "none";
    darkModeButton.style.display = "block";
    saveTheme('dark');
});

darkModeButton.addEventListener("click", () => {
    document.body.classList.remove("dark");
    darkModeButton.style.display = "none";
    lightModeButton.style.display = "block";
    saveTheme('light');
});

// Load theme on page load
loadSavedTheme();
// 预加载器已移除：不再在脚本中控制 `.pre-loader` 或在加载期间禁止滚动。

// Mobile Menu Toggle
const mobileMenuButton = document.querySelector(".mobile-menu-toggle");
const navigationMenu = document.querySelector(".navigation-menu");

mobileMenuButton.addEventListener("click", () => {
    navigationMenu.classList.toggle("dis");
    document.body.classList.toggle("overflow");
});

// Page Transition Handler
function setupPageTransitions() {
    // Check if browser supports View Transitions API
    const supportsViewTransitions = 'startViewTransition' in document;

    // Get all navigation links
    const links = document.querySelectorAll('a[href^="index.html"], a[href^="cv.html"], a[href^="research.html"], a[href^="design.html"], a[href^="contact.html"]');

    links.forEach(link => {
        link.addEventListener('click', function (e) {
            const targetUrl = this.href;
            const currentUrl = window.location.href;

            // Don't transition if clicking current page
            if (targetUrl === currentUrl) {
                e.preventDefault();
                return;
            }

            // Modern browsers: Use View Transitions API
            if (supportsViewTransitions) {
                e.preventDefault();

                document.startViewTransition(() => {
                    window.location.href = targetUrl;
                });
            }
            // Fallback: CSS animation
            else {
                e.preventDefault();

                // Add exit animation
                document.body.classList.add('page-exit');

                // Navigate after animation completes
                setTimeout(() => {
                    window.location.href = targetUrl;
                }, 300); // Match fadeOut duration
            }
        });
    });
}

// Initialize page transitions after DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', setupPageTransitions);
} else {
    setupPageTransitions();
}

// ==================== 访客埋点功能 ====================

// API 配置
const VISITOR_API_URL = 'http://122.51.104.18:18888/api/visit';

// 获取浏览器信息
function getBrowserInfo() {
    const userAgent = navigator.userAgent;
    let browser = 'Unknown';

    if (userAgent.indexOf('Firefox') > -1) {
        browser = 'Firefox';
    } else if (userAgent.indexOf('Chrome') > -1) {
        browser = 'Chrome';
    } else if (userAgent.indexOf('Safari') > -1) {
        browser = 'Safari';
    } else if (userAgent.indexOf('Edge') > -1) {
        browser = 'Edge';
    } else if (userAgent.indexOf('Opera') > -1 || userAgent.indexOf('OPR') > -1) {
        browser = 'Opera';
    } else if (userAgent.indexOf('Trident') > -1) {
        browser = 'Internet Explorer';
    }

    return browser;
}

// 获取操作系统信息
function getOSInfo() {
    const userAgent = navigator.userAgent;
    let os = 'Unknown';

    if (userAgent.indexOf('Win') > -1) {
        os = 'Windows';
    } else if (userAgent.indexOf('Mac') > -1) {
        os = 'macOS';
    } else if (userAgent.indexOf('Linux') > -1) {
        os = 'Linux';
    } else if (userAgent.indexOf('Android') > -1) {
        os = 'Android';
    } else if (userAgent.indexOf('iOS') > -1 || userAgent.indexOf('iPhone') > -1 || userAgent.indexOf('iPad') > -1) {
        os = 'iOS';
    }

    return os;
}

// 获取当前页面路径
function getCurrentPage() {
    const path = window.location.pathname;
    const page = path.split('/').pop() || 'index.html';
    return page;
}

// 获取访客IP地址（API）
async function getVisitorIP() {
    try {
        const response = await fetch('https://api.ipify.org?format=json');
        const data = await response.json();
        return data.ip;
    } catch (error) {
        console.error('获取IP失败:', error);
        return 'Unknown';
    }
}

// 记录访客访问
async function recordVisit() {
    try {
        // 获取访客IP
        const ip = await getVisitorIP();

        // 获取访客信息
        const visitorData = {
            ip: ip,
            page: getCurrentPage(),
            browser: getBrowserInfo(),
            os: getOSInfo(),
            user_agent: navigator.userAgent,
            referrer: document.referrer || '直接访问'
        };

        // 发送访客数据到后端
        const response = await fetch(VISITOR_API_URL, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(visitorData)
        });

        if (response.ok) {
            const result = await response.json();
            console.log('访客记录成功:', result);
        } else {
            console.error('访客记录失败:', response.status);
        }
    } catch (error) {
        console.error('访客埋点错误:', error);
        // 埋点失败不影响页面正常使用，静默处理
    }
}

// 页面加载完成后记录访客
window.addEventListener('load', () => {
    // 延迟执行，避免阻塞页面加载
    setTimeout(() => {
        recordVisit();
    }, 1000);
});
