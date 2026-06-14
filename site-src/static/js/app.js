/**
 * Git Kimchi LMS — Client-side JavaScript
 * Progress tracking, navigation, and UI interactions
 */

(function () {
  'use strict';

  const STORAGE_KEY = 'git-kimchi-progress';

  // ----------------------------------------
  // Progress Helpers
  // ----------------------------------------

  function loadProgress() {
    try {
      const raw = localStorage.getItem(STORAGE_KEY);
      return raw ? JSON.parse(raw) : { visited: {}, completed: {} };
    } catch (e) {
      return { visited: {}, completed: {} };
    }
  }

  function saveProgress(progress) {
    try {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(progress));
    } catch (e) {
      // Storage may be full or unavailable
    }
  }

  function markVisited(lessonId) {
    const progress = loadProgress();
    progress.visited[lessonId] = true;
    saveProgress(progress);
    updateUI();
  }

  function toggleCompleted(lessonId) {
    const progress = loadProgress();
    progress.completed[lessonId] = !progress.completed[lessonId];
    if (progress.completed[lessonId]) {
      progress.visited[lessonId] = true;
    }
    saveProgress(progress);
    updateUI();
    return progress.completed[lessonId];
  }

  function getCompletionRate() {
    const progress = loadProgress();
    const lessonIds = [];
    for (let i = 1; i <= 15; i++) {
      lessonIds.push(String(i));
    }
    const completedCount = lessonIds.filter(id => progress.completed[id]).length;
    return { completed: completedCount, total: 15, percent: Math.round((completedCount / 15) * 100) };
  }

  // ----------------------------------------
  // UI Updates
  // ----------------------------------------

  function updateUI() {
    const progress = loadProgress();
    const rate = getCompletionRate();

    // Update header progress bar on lesson pages
    const headerProgress = document.getElementById('header-progress');
    const progressBarFill = document.getElementById('progress-bar-fill');
    const progressText = document.getElementById('progress-text');
    if (headerProgress && progressBarFill && progressText) {
      headerProgress.style.display = 'flex';
      progressBarFill.style.width = rate.percent + '%';
      progressText.textContent = rate.completed + ' / ' + rate.total;
    }

    // Update homepage ring
    const ringFill = document.getElementById('progress-ring-fill');
    const ringPercent = document.getElementById('progress-percent');
    if (ringFill && ringPercent) {
      const circumference = 326.726;
      const offset = circumference - (rate.percent / 100) * circumference;
      ringFill.style.strokeDashoffset = offset;
      ringPercent.textContent = rate.percent + '%';
    }

    // Update nav status dots
    document.querySelectorAll('[data-status-lesson]').forEach(el => {
      const lessonId = el.getAttribute('data-status-lesson');
      el.classList.remove('visited', 'completed');
      if (progress.completed[lessonId]) {
        el.classList.add('completed');
      } else if (progress.visited[lessonId]) {
        el.classList.add('visited');
      }
    });

    // Update "Mark Complete" button state
    const btn = document.getElementById('btn-mark-complete');
    if (btn) {
      const lessonId = btn.getAttribute('data-lesson');
      const isCompleted = !!progress.completed[lessonId];
      btn.classList.toggle('completed', isCompleted);
      btn.querySelector('.btn-icon').textContent = isCompleted ? '✓' : '✓';
      btn.childNodes[btn.childNodes.length - 1].textContent = isCompleted ? ' Completed' : ' Mark Complete';
    }
  }

  // ----------------------------------------
  // Mobile Sidebar
  // ----------------------------------------

  function initSidebar() {
    const toggle = document.getElementById('menu-toggle');
    const sidebar = document.getElementById('sidebar');
    const closeBtn = document.getElementById('sidebar-close');
    if (!toggle || !sidebar) return;

    // Create overlay if missing
    let overlay = document.querySelector('.sidebar-overlay');
    if (!overlay) {
      overlay = document.createElement('div');
      overlay.className = 'sidebar-overlay';
      document.body.appendChild(overlay);
    }

    function open() {
      sidebar.classList.add('open');
      overlay.classList.add('open');
      document.body.style.overflow = 'hidden';
    }

    function close() {
      sidebar.classList.remove('open');
      overlay.classList.remove('open');
      document.body.style.overflow = '';
    }

    toggle.addEventListener('click', open);
    if (closeBtn) closeBtn.addEventListener('click', close);
    overlay.addEventListener('click', close);

    // Close on resize to desktop
    window.addEventListener('resize', () => {
      if (window.innerWidth > 768) close();
    });
  }

  // ----------------------------------------
  // Back to Top
  // ----------------------------------------

  function initBackToTop() {
    const btn = document.getElementById('back-to-top');
    if (!btn) return;

    const threshold = 300;

    function onScroll() {
      if (window.scrollY > threshold) {
        btn.classList.add('visible');
      } else {
        btn.classList.remove('visible');
      }
    }

    window.addEventListener('scroll', onScroll, { passive: true });
    onScroll();

    btn.addEventListener('click', () => {
      window.scrollTo({ top: 0, behavior: 'smooth' });
    });
  }

  // ----------------------------------------
  // Mark Complete
  // ----------------------------------------

  function initMarkComplete() {
    const btn = document.getElementById('btn-mark-complete');
    if (!btn) return;

    btn.addEventListener('click', () => {
      const lessonId = btn.getAttribute('data-lesson');
      const isCompleted = toggleCompleted(lessonId);
      btn.classList.toggle('completed', isCompleted);
      const labelSpan = document.createTextNode(isCompleted ? ' Completed' : ' Mark Complete');
      // Rebuild label
      const icon = btn.querySelector('.btn-icon');
      btn.innerHTML = '';
      btn.appendChild(icon);
      btn.appendChild(document.createTextNode(isCompleted ? ' Completed' : ' Mark Complete'));
    });
  }

  // ----------------------------------------
  // Smooth Scroll for Anchors
  // ----------------------------------------

  function initSmoothScroll() {
    document.addEventListener('click', (e) => {
      const a = e.target.closest('a[href^="#"]');
      if (!a) return;
      const targetId = a.getAttribute('href').slice(1);
      const target = document.getElementById(targetId);
      if (target) {
        e.preventDefault();
        const headerOffset = 80;
        const top = target.getBoundingClientRect().top + window.scrollY - headerOffset;
        window.scrollTo({ top, behavior: 'smooth' });
      }
    });
  }

  // ----------------------------------------
  // TOC Active Tracking
  // ----------------------------------------

  function initTOCTracking() {
    const toc = document.getElementById('lesson-toc');
    const content = document.querySelector('.lesson-body');
    if (!toc || !content) return;

    const headings = content.querySelectorAll('h2[id], h3[id]');
    const tocLinks = toc.querySelectorAll('a[href^="#"]');
    if (!headings.length || !tocLinks.length) return;

    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach(entry => {
          if (entry.isIntersecting) {
            tocLinks.forEach(link => link.classList.remove('active'));
            const link = toc.querySelector('a[href="#' + entry.target.id + '"]');
            if (link) link.classList.add('active');
          }
        });
      },
      { rootMargin: '-80px 0px -60% 0px', threshold: 0 }
    );

    headings.forEach(h => observer.observe(h));
  }

  // ----------------------------------------
  // Mark Current Page Active in Sidebar
  // ----------------------------------------

  function initActiveNav() {
    const currentPath = window.location.pathname;
    const filename = currentPath.split('/').pop() || 'index.html';
    document.querySelectorAll('.nav-link').forEach(link => {
      const href = link.getAttribute('href');
      if (href && href.endsWith(filename)) {
        link.classList.add('active');
      }
    });
  }

  // ----------------------------------------
  // Visit Tracking (lesson pages only)
  // ----------------------------------------

  function initVisitTracking() {
    const body = document.body;
    const pageType = body.getAttribute('data-page');
    if (pageType !== 'lesson') return;
    const btn = document.getElementById('btn-mark-complete');
    if (!btn) return;
    const lessonId = btn.getAttribute('data-lesson');
    if (lessonId) {
      markVisited(lessonId);
    }
  }

  // ----------------------------------------
  // Solutions page visit tracking
  // ----------------------------------------

  function initSolutionsTracking() {
    const body = document.body;
    const pageType = body.getAttribute('data-page');
    if (pageType === 'solutions') {
      markVisited('solutions');
    }
  }

  // ----------------------------------------
  // Boot
  // ----------------------------------------

  function init() {
    updateUI();
    initSidebar();
    initBackToTop();
    initMarkComplete();
    initSmoothScroll();
    initTOCTracking();
    initActiveNav();
    initVisitTracking();
    initSolutionsTracking();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
