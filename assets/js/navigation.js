(function() {
  'use strict';

  function init() {
    var content = document.querySelector('.main-content');
    if (!content) return;

    var headings = content.querySelectorAll('h2, h3');
    if (headings.length === 0) return;

    headings.forEach(function(h, i) {
      if (!h.id) {
        h.id = 'toc-heading-' + i;
      }
    });

    // 构建目录
    var html = '<div class="toc-title">📖 目录</div>';
    headings.forEach(function(h) {
      var cls = h.tagName === 'H3' ? 'toc-h3' : '';
      var text = h.textContent.replace(/^#+\s*/, '').trim();
      html += '<a class="' + cls + '" href="#' + h.id + '">' + escapeHtml(text) + '</a>';
    });

    var panel = document.querySelector('.toc-nav-panel');
    if (panel) {
      panel.innerHTML = html;
    }

    // 点击切换
    var btn = document.querySelector('.toc-nav-btn');
    var overlay = document.querySelector('.toc-overlay');

    function open() {
      panel.classList.add('open');
      overlay.classList.add('open');
      document.body.style.overflow = 'hidden';
    }

    function close() {
      panel.classList.remove('open');
      overlay.classList.remove('open');
      document.body.style.overflow = '';
    }

    if (btn) {
      btn.addEventListener('click', function(e) {
        e.stopPropagation();
        if (panel.classList.contains('open')) {
          close();
        } else {
          open();
        }
      });
    }

    // 点击遮罩关闭
    if (overlay) {
      overlay.addEventListener('click', close);
    }

    // 点击链接后关闭
    panel.addEventListener('click', function(e) {
      if (e.target.tagName === 'A') {
        // 让浏览器先执行默认跳转，再关闭面板
        setTimeout(close, 150);
      }
    });

    // ESC 关闭
    document.addEventListener('keydown', function(e) {
      if (e.key === 'Escape' && panel.classList.contains('open')) {
        close();
      }
    });
  }

  function escapeHtml(str) {
    var div = document.createElement('div');
    div.appendChild(document.createTextNode(str));
    return div.innerHTML;
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();