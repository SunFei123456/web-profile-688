
// 图片查看器功能
document.addEventListener('DOMContentLoaded', function() {
    // 获取所有图片元素
    const galleryImages = document.querySelectorAll('.detail-gallery img');

    // 创建图片查看器元素
    const viewer = document.createElement('div');
    viewer.className = 'image-viewer';
    viewer.innerHTML = `
        <div class="image-viewer-container">
            <button class="image-viewer-close">&times;</button>
            <img src="" alt="放大预览" class="image-viewer-img">
        </div>
    `;

    // 添加样式
    const style = document.createElement('style');
    style.textContent = `
        .image-viewer {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background-color: rgba(0, 0, 0, 0.9);
            z-index: 1000;
            display: none;
            justify-content: center;
            align-items: center;
            opacity: 0;
            transition: opacity 0.3s ease;
        }

        .image-viewer.active {
            display: flex;
            opacity: 1;
        }

        .image-viewer-container {
            position: relative;
            max-width: 90%;
            max-height: 90%;
            display: flex;
            flex-direction: column;
            align-items: center;
        }

        .image-viewer-close {
            position: absolute;
            top: -40px;
            right: 0;
            color: white;
            font-size: 30px;
            cursor: pointer;
            background: none;
            border: none;
            padding: 0;
            width: 30px;
            height: 30px;
            display: flex;
            justify-content: center;
            align-items: center;
        }

        .image-viewer-img {
            max-width: 100%;
            max-height: 80vh;
            object-fit: contain;
            border-radius: 4px;
            box-shadow: 0 5px 15px rgba(0, 0, 0, 0.3);
        }

        /* 添加加载动画 */
        .image-viewer-img.loading {
            opacity: 0.7;
        }

        /* 响应式调整 */
        @media (max-width: 768px) {
            .image-viewer-container {
                max-width: 95%;
                max-height: 95%;
            }

            .image-viewer-close {
                top: -35px;
                font-size: 24px;
            }
        }
    `;

    document.head.appendChild(style);
    document.body.appendChild(viewer);

    // 获取查看器元素
    const viewerImg = viewer.querySelector('.image-viewer-img');
    const closeBtn = viewer.querySelector('.image-viewer-close');

    // 为每个图片添加点击事件
    galleryImages.forEach(img => {
        // 添加鼠标悬停效果，提示可点击
        img.style.cursor = 'pointer';
        img.title = '点击查看大图';

        img.addEventListener('click', function() {
            // 显示加载状态
            viewerImg.classList.add('loading');

            // 设置图片源
            viewerImg.src = this.src;

            // 显示查看器
            viewer.classList.add('active');

            // 图片加载完成后移除加载状态
            viewerImg.onload = function() {
                viewerImg.classList.remove('loading');
            };
        });
    });

    // 关闭查看器
    function closeViewer() {
        viewer.classList.remove('active');
    }

    // 点击关闭按钮
    closeBtn.addEventListener('click', closeViewer);

    // 点击背景关闭
    viewer.addEventListener('click', function(e) {
        if (e.target === viewer) {
            closeViewer();
        }
    });

    // 按ESC键关闭
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape' && viewer.classList.contains('active')) {
            closeViewer();
        }
    });
});
