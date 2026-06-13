(function() {
  'use strict';

  function initTocNav() {
    var content = document.querySelector('.main-content');
    if (!content) return;

    // 只收集 h2 和 h3 标题
    var headings = content.querySelectorAll('h2, h3');
    if (headings.length === 0) return;

    // 给每个 heading 加 id（如果还没有）
    headings.forEach(function(h, i) {
      if (!h.id) {
        h.id = 'toc-heading-' + i;
      }
    });

    // 构建 HTML
    var html = '<div class="toc-nav-title">目录</div>';
    headings.forEach(function(h) {
      var cls = h.tagName === 'H3' ? 'toc-h3' : '';
      var text = h.textContent.replace(/^#+\s*/, '').trim();
      html += '<a class="' + cls + '" href="#' + h.id + '">' + escapeHtml(text) + '</a>';
    });

    // 插入到面板
    var panel = document.querySelector('.toc-nav-panel');
    if (panel) {
      panel.innerHTML = html;
    }
  }

  function escapeHtml(str) {
    var div = document.createElement('div');
    div.appendChild(document.createTextNode(str));
    return div.innerHTML;
  }

  // DOM 加载完成后执行
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initTocNav);
  } else {
    initTocNav();
  }
})();