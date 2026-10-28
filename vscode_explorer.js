/**
 * ChronoChef - VS Code Style Complete Codebase Explorer & Global Search Engine
 * College Project PBCST304 (Object Oriented Programming)
 * 
 * Features:
 * - 100% complete project codebase: All 20 Java source files + Python tools + Batch scripts + Web code + Docs (32 files, 10,295 lines)
 * - Exact directory structure matching the developer's laptop
 * - Real-time full-text search across all files, classes, methods, and code lines
 * - Multi-language syntax highlighting (Java, Python, JS, HTML, CSS, Batch, Markdown)
 * - Direct interactive jump to all 15 OOP concepts implemented in the codebase
 */

(function () {
  // State
  let openTabs = [];
  let activeFileKey = "project code/src/model/FoodItem.java";
  let currentActiveTabSidebar = "explorer";
  let currentSearchQuery = "";
  let setSidebarVisibility = null;
  let toggleSidebar = null;

  function normalizePath(p) {
    return p ? p.replace(/\\/g, "/") : "";
  }

  function escapeHtml(str) {
    if (!str) return "";
    return str
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;")
      .replace(/'/g, "&#039;");
  }

  // Syntax Highlighting supporting Java, Python, JS, HTML, CSS, Batch, Markdown
  function highlightCode(code, fileName, queryToHighlight = null) {
    const lines = code.split("\n");
    const ext = fileName.includes(".") ? fileName.split(".").pop().toLowerCase() : "";

    // Keywords
    const javaKw = [
      "abstract", "assert", "boolean", "break", "byte", "case", "catch", "char",
      "class", "const", "continue", "default", "do", "double", "else", "enum",
      "extends", "final", "finally", "float", "for", "if", "implements", "import",
      "instanceof", "int", "interface", "long", "new", "package", "private",
      "protected", "public", "return", "short", "static", "super", "switch",
      "synchronized", "this", "throw", "throws", "try", "void", "volatile",
      "while", "true", "false", "null", "record"
    ];
    const pyKw = [
      "def", "class", "import", "from", "as", "return", "if", "elif", "else",
      "for", "while", "in", "not", "and", "or", "is", "with", "try", "except",
      "finally", "raise", "pass", "lambda", "global", "True", "False", "None"
    ];
    const jsKw = [
      "const", "let", "var", "function", "return", "if", "else", "for", "while",
      "switch", "case", "break", "continue", "new", "class", "extends", "import",
      "export", "default", "try", "catch", "finally", "throw", "async", "await",
      "this", "null", "undefined", "true", "false"
    ];

    let kwList = javaKw;
    if (ext === "py") kwList = pyKw;
    else if (ext === "js") kwList = jsKw;
    const kwRegex = new RegExp(`\\b(${kwList.join("|")})\\b`, "g");

    return lines.map((line, idx) => {
      let escaped = escapeHtml(line);

      // Comments
      if (ext === "py" && escaped.trim().startsWith("#")) {
        escaped = `<span class="vsc-token-comment">${escaped}</span>`;
      } else if (ext === "bat" && (escaped.trim().startsWith("@REM") || escaped.trim().startsWith("REM") || escaped.trim().startsWith("::"))) {
        escaped = `<span class="vsc-token-comment">${escaped}</span>`;
      } else if (escaped.trim().startsWith("//") || escaped.trim().startsWith("/*") || escaped.trim().startsWith("*")) {
        escaped = `<span class="vsc-token-comment">${escaped}</span>`;
      } else {
        // Strings
        escaped = escaped.replace(/(["'])(?:(?=(\\?))\2.)*?\1/g, '<span class="vsc-token-string">$&</span>');

        // Annotations
        escaped = escaped.replace(/@\w+/g, '<span class="vsc-token-annotation">$&</span>');

        // Keywords
        escaped = escaped.replace(kwRegex, '<span class="vsc-token-keyword">$1</span>');

        // Numbers
        escaped = escaped.replace(/\b(\d+(\.\d+)?)\b/g, '<span class="vsc-token-number">$1</span>');
      }

      // Search Query Highlight
      if (queryToHighlight && queryToHighlight.trim().length > 1) {
        const qEsc = escapeHtml(queryToHighlight.trim());
        const qRegex = new RegExp(`(${qEsc})`, "gi");
        escaped = escaped.replace(qRegex, '<mark class="vsc-search-match">$1</mark>');
      }

      return `<div class="vsc-code-line" id="line-${idx + 1}"><span class="vsc-line-num">${idx + 1}</span><span class="vsc-line-content">${escaped || " "}</span></div>`;
    }).join("");
  }

  // File Icon Mapper
  function getFileIcon(fileName, classType) {
    const ext = fileName.includes(".") ? fileName.split(".").pop().toLowerCase() : "";
    if (ext === "java") {
      if (classType === "Interface") return "⚡";
      if (classType === "Abstract Class") return "🔷";
      if (classType === "Custom Exception") return "⚠️";
      if (classType === "Swing JFrame") return "🖥️";
      if (classType === "Swing JPanel") return "📑";
      return "☕";
    }
    if (ext === "py") return "🐍";
    if (ext === "js") return "🟨";
    if (ext === "html") return "🌐";
    if (ext === "css") return "🎨";
    if (ext === "bat") return "⚙️";
    if (ext === "md") return "📝";
    if (ext === "json") return "🔧";
    return "📄";
  }

  // Initialize
  function initVSCodeExplorer() {
    if (typeof CHRONOCHEF_CODEBASE === "undefined") {
      console.warn("CHRONOCHEF_CODEBASE data not found.");
      return;
    }

    // Default open tabs
    openTabs = [
      "project code/src/Main.java",
      "project code/src/model/FoodItem.java",
      "project code/src/service/PriorityPricingService.java",
      "project code/src/database/DatabaseManager.java",
      "generate_project_report.py"
    ];
    activeFileKey = "project code/src/model/FoodItem.java";

    renderExplorerTree();
    renderTabs();
    renderActiveFile();
    setupEventListeners();
  }

  // Render Full Laptop Directory Tree
  function renderExplorerTree() {
    const treeContainer = document.getElementById("vsc-file-tree");
    if (!treeContainer) return;

    // Categorize all files into exact folder structures
    const javaFolders = {
      root: [],
      database: [],
      exception: [],
      model: [],
      service: [],
      test: [],
      ui: []
    };
    const scripts = [];
    const webFiles = [];
    const docs = [];
    const batchFiles = [];

    Object.keys(CHRONOCHEF_CODEBASE).forEach(rawKey => {
      const key = normalizePath(rawKey);
      const file = CHRONOCHEF_CODEBASE[rawKey];
      file.normalizedKey = key;

      if (key.startsWith("project code/src/")) {
        const sub = key.replace("project code/src/", "");
        if (sub.includes("/")) {
          const folder = sub.split("/")[0];
          if (javaFolders[folder]) {
            javaFolders[folder].push(file);
          }
        } else {
          javaFolders.root.push(file);
        }
      } else if (key.endsWith(".bat")) {
        batchFiles.push(file);
      } else if (key.endsWith(".py")) {
        scripts.push(file);
      } else if (["index.html", "index.css", "app.js", "vercel.json"].includes(key)) {
        webFiles.push(file);
      } else if (key.endsWith(".md")) {
        docs.push(file);
      }
    });

    function renderFileItem(f) {
      const isActive = f.normalizedKey === activeFileKey ? "active" : "";
      return `
        <div class="vsc-tree-file ${isActive}" data-file="${f.normalizedKey}">
          <span class="vsc-file-indent"></span>
          <span class="vsc-file-icon">${getFileIcon(f.fileName, f.classType)}</span>
          <span class="vsc-file-title">${f.fileName}</span>
          <span class="vsc-file-badge">${f.linesCount}L</span>
        </div>
      `;
    }

    let html = `
      <div class="vsc-tree-root">
        
        <!-- Folder 1: project code (Core Java Desktop Application) -->
        <div class="vsc-tree-folder open" data-folder="project-code">
          <div class="vsc-folder-header">
            <span class="vsc-chevron">▼</span>
            <span class="vsc-folder-icon">📁</span>
            <span class="vsc-folder-name">project code</span>
            <span class="vsc-folder-count">23 files</span>
          </div>
          <div class="vsc-folder-children">
            
            <!-- src/ Folder -->
            <div class="vsc-tree-folder open" data-folder="src">
              <div class="vsc-folder-header">
                <span class="vsc-chevron">▼</span>
                <span class="vsc-folder-icon">📁</span>
                <span class="vsc-folder-name">src</span>
                <span class="vsc-folder-count">20 Java classes</span>
              </div>
              <div class="vsc-folder-children">
    `;

    // Root Java files (Main.java)
    javaFolders.root.forEach(f => {
      html += renderFileItem(f);
    });

    // Java Packages
    const pkgDisplay = [
      { id: "model", name: "model", list: javaFolders.model, badge: "Entities & Base OOP" },
      { id: "service", name: "service", list: javaFolders.service, badge: "PDI Formula & Bubble Sort" },
      { id: "database", name: "database", list: javaFolders.database, badge: "SQLite DAO & Singleton" },
      { id: "exception", name: "exception", list: javaFolders.exception, badge: "Safety Guardrails" },
      { id: "ui", name: "ui", list: javaFolders.ui, badge: "Swing CardLayout Panels" },
      { id: "test", name: "test", list: javaFolders.test, badge: "35-Point Verification" }
    ];

    pkgDisplay.forEach(pkg => {
      html += `
        <div class="vsc-tree-folder open" data-folder="${pkg.id}">
          <div class="vsc-folder-header">
            <span class="vsc-chevron">▼</span>
            <span class="vsc-folder-icon">📁</span>
            <span class="vsc-folder-name">${pkg.name}</span>
            <span class="vsc-folder-count">${pkg.list.length}</span>
          </div>
          <div class="vsc-folder-children">
      `;
      pkg.list.forEach(f => {
        html += renderFileItem(f);
      });
      html += `
          </div>
        </div>
      `;
    });

    // Close src
    html += `
              </div>
            </div>
    `;

    // Batch scripts inside project code
    batchFiles.forEach(f => {
      html += renderFileItem(f);
    });

    // Close project code
    html += `
          </div>
        </div>

        <!-- Folder 2: Academic Report & PDF Generators (Python) -->
        <div class="vsc-tree-folder open" data-folder="scripts">
          <div class="vsc-folder-header">
            <span class="vsc-chevron">▼</span>
            <span class="vsc-folder-icon">📁</span>
            <span class="vsc-folder-name">academic report generators</span>
            <span class="vsc-folder-count">${scripts.length}</span>
          </div>
          <div class="vsc-folder-children">
    `;
    scripts.forEach(f => {
      html += renderFileItem(f);
    });
    html += `
          </div>
        </div>

        <!-- Folder 3: Web Application & Vercel Emulator Runtime -->
        <div class="vsc-tree-folder open" data-folder="web">
          <div class="vsc-folder-header">
            <span class="vsc-chevron">▼</span>
            <span class="vsc-folder-icon">📁</span>
            <span class="vsc-folder-name">web application runtime</span>
            <span class="vsc-folder-count">${webFiles.length}</span>
          </div>
          <div class="vsc-folder-children">
    `;
    webFiles.forEach(f => {
      html += renderFileItem(f);
    });
    html += `
          </div>
        </div>

        <!-- Documentation Files at Root -->
    `;
    docs.forEach(f => {
      html += renderFileItem(f);
    });

    html += `
      </div>
    `;

    treeContainer.innerHTML = html;

    // Attach tree event handlers
    treeContainer.querySelectorAll(".vsc-folder-header").forEach(header => {
      header.addEventListener("click", (e) => {
        e.stopPropagation();
        const folder = header.parentElement;
        folder.classList.toggle("open");
        const chevron = header.querySelector(".vsc-chevron");
        if (chevron) {
          chevron.textContent = folder.classList.contains("open") ? "▼" : "▶";
        }
      });
    });

    treeContainer.querySelectorAll(".vsc-tree-file").forEach(fileItem => {
      fileItem.addEventListener("click", () => {
        const fileKey = fileItem.dataset.file;
        openFile(fileKey);
      });
    });
  }

  // Open file in tabs & editor
  function openFile(fileKey, targetLine = null) {
    const normKey = normalizePath(fileKey);
    let matchedKey = null;

    Object.keys(CHRONOCHEF_CODEBASE).forEach(k => {
      if (normalizePath(k) === normKey) {
        matchedKey = k;
      }
    });

    if (!matchedKey) return;

    if (!openTabs.includes(normKey)) {
      openTabs.push(normKey);
    }
    activeFileKey = normKey;

    renderExplorerTree();
    renderTabs();
    renderActiveFile();

    // On mobile devices, auto-collapse sidebar drawer when selecting a file
    if (window.innerWidth <= 768 && typeof setSidebarVisibility === "function") {
      setSidebarVisibility(false);
    }

    if (targetLine) {
      setTimeout(() => {
        scrollToLine(targetLine);
      }, 50);
    }
  }

  // Scroll to line & highlight
  function scrollToLine(lineNum) {
    const lineEl = document.getElementById(`line-${lineNum}`);
    if (lineEl) {
      lineEl.scrollIntoView({ behavior: "smooth", block: "center" });
      lineEl.classList.add("vsc-line-targeted");
      setTimeout(() => {
        lineEl.classList.remove("vsc-line-targeted");
      }, 3000);
    }
  }

  // Render Tabs bar
  function renderTabs() {
    const tabsContainer = document.getElementById("vsc-tabs-bar");
    if (!tabsContainer) return;

    let html = "";
    openTabs.forEach(normKey => {
      let file = null;
      Object.keys(CHRONOCHEF_CODEBASE).forEach(k => {
        if (normalizePath(k) === normKey) file = CHRONOCHEF_CODEBASE[k];
      });
      if (!file) return;

      const isActive = normKey === activeFileKey ? "active" : "";
      html += `
        <div class="vsc-tab ${isActive}" data-file="${normKey}">
          <span class="vsc-tab-icon">${getFileIcon(file.fileName, file.classType)}</span>
          <span class="vsc-tab-title">${file.fileName}</span>
          <button class="vsc-tab-close" data-close="${normKey}" title="Close tab">✕</button>
        </div>
      `;
    });

    tabsContainer.innerHTML = html;

    tabsContainer.querySelectorAll(".vsc-tab").forEach(tab => {
      tab.addEventListener("click", (e) => {
        if (e.target.classList.contains("vsc-tab-close")) return;
        const fileKey = tab.dataset.file;
        openFile(fileKey);
      });
    });

    tabsContainer.querySelectorAll(".vsc-tab-close").forEach(closeBtn => {
      closeBtn.addEventListener("click", (e) => {
        e.stopPropagation();
        const toClose = closeBtn.dataset.close;
        openTabs = openTabs.filter(k => k !== toClose);
        if (activeFileKey === toClose) {
          activeFileKey = openTabs.length > 0 ? openTabs[openTabs.length - 1] : "project code/src/model/FoodItem.java";
        }
        renderTabs();
        renderActiveFile();
        renderExplorerTree();
      });
    });
  }

  // Render Active File into Editor
  function renderActiveFile(queryToHighlight = null) {
    let file = null;
    Object.keys(CHRONOCHEF_CODEBASE).forEach(k => {
      if (normalizePath(k) === activeFileKey) file = CHRONOCHEF_CODEBASE[k];
    });
    if (!file) return;

    // Breadcrumbs
    const breadcrumbs = document.getElementById("vsc-breadcrumbs");
    if (breadcrumbs) {
      const parts = activeFileKey.split("/");
      breadcrumbs.innerHTML = parts.map((p, idx) => {
        const isLast = idx === parts.length - 1;
        return `<span class="vsc-bc-item ${isLast ? 'active' : ''}">${p}</span>`;
      }).join('<span class="vsc-bc-sep">/</span>');
    }

    // Meta Badges
    const metaContainer = document.getElementById("vsc-file-meta");
    if (metaContainer) {
      let badgesHtml = `
        <span class="vsc-meta-tag class-type">${file.classType}</span>
        <span class="vsc-meta-tag package-name">${file.category || file.package}</span>
      `;
      if (file.oopTags && file.oopTags.length > 0) {
        file.oopTags.forEach(tag => {
          badgesHtml += `<span class="vsc-meta-tag oop-tag">⚡ ${tag}</span>`;
        });
      }
      metaContainer.innerHTML = badgesHtml;
    }

    // Code Editor Pane
    const codeArea = document.getElementById("vsc-code-editor-content");
    if (codeArea) {
      codeArea.innerHTML = highlightCode(file.content, file.fileName, queryToHighlight);
    }

    // Re-apply active zoom scale to newly rendered code lines
    applyCurrentZoom();

    // Status bar stats
    const statsEl = document.getElementById("vsc-status-stats");
    if (statsEl) {
      statsEl.textContent = `Lines: ${file.linesCount} | ${file.size.toLocaleString()} bytes | UTF-8`;
    }
  }

  // Real-time Global Search Engine
  function performSearch(query) {
    currentSearchQuery = query.trim();
    const resultsContainer = document.getElementById("vsc-search-results");
    if (!resultsContainer) return;

    if (!currentSearchQuery) {
      resultsContainer.innerHTML = `
        <div class="vsc-search-placeholder">
          <div class="vsc-placeholder-icon">🔍</div>
          <div>Type to search across all 32 project files, classes, methods, and 10,295 lines of code.</div>
        </div>
      `;
      renderActiveFile();
      return;
    }

    const qLower = currentSearchQuery.toLowerCase();
    const results = [];
    let totalMatches = 0;

    Object.keys(CHRONOCHEF_CODEBASE).forEach(rawKey => {
      const file = CHRONOCHEF_CODEBASE[rawKey];
      const normKey = normalizePath(rawKey);
      const fileMatches = [];

      const nameMatch = file.fileName.toLowerCase().includes(qLower) || file.className.toLowerCase().includes(qLower);
      const pkgMatch = (file.package || "").toLowerCase().includes(qLower) || (file.category || "").toLowerCase().includes(qLower);
      const tagMatch = file.oopTags && file.oopTags.some(t => t.toLowerCase().includes(qLower));

      const lines = file.content.split("\n");
      lines.forEach((lineText, idx) => {
        if (lineText.toLowerCase().includes(qLower)) {
          fileMatches.push({
            lineNum: idx + 1,
            lineText: lineText.trim()
          });
        }
      });

      if (nameMatch || pkgMatch || tagMatch || fileMatches.length > 0) {
        results.push({
          fileKey: normKey,
          fileName: file.fileName,
          path: file.path,
          classType: file.classType,
          nameMatch,
          tagMatch,
          matches: fileMatches
        });
        totalMatches += fileMatches.length + (nameMatch ? 1 : 0);
      }
    });

    if (results.length === 0) {
      resultsContainer.innerHTML = `
        <div class="vsc-search-empty">
          <div>No results found for "<strong>${escapeHtml(currentSearchQuery)}</strong>"</div>
          <div class="vsc-search-tip">Try searching for keywords like <code>FoodItem</code>, <code>PDI</code>, <code>SQLException</code>, <code>BubbleSort</code>, <code>Singleton</code>, or <code>extends</code>.</div>
        </div>
      `;
      renderActiveFile();
      return;
    }

    let html = `
      <div class="vsc-search-summary">
        Found <strong>${totalMatches}</strong> match${totalMatches === 1 ? '' : 'es'} in <strong>${results.length}</strong> file${results.length === 1 ? '' : 's'}
      </div>
      <div class="vsc-search-list">
    `;

    results.forEach(res => {
      html += `
        <div class="vsc-search-file-group">
          <div class="vsc-search-file-header" data-file="${res.fileKey}">
            <span class="vsc-search-file-icon">${getFileIcon(res.fileName, res.classType)}</span>
            <span class="vsc-search-file-name">${res.fileName}</span>
            <span class="vsc-search-badge">${res.matches.length} matches</span>
          </div>
          <div class="vsc-search-line-matches">
      `;

      res.matches.slice(0, 8).forEach(m => {
        const highlightedSnippet = escapeHtml(m.lineText).replace(
          new RegExp(`(${escapeHtml(currentSearchQuery)})`, "gi"),
          '<mark>$1</mark>'
        );
        html += `
          <div class="vsc-search-line-item" data-file="${res.fileKey}" data-line="${m.lineNum}">
            <span class="vsc-search-ln">${m.lineNum}:</span>
            <span class="vsc-search-text">${highlightedSnippet}</span>
          </div>
        `;
      });

      if (res.matches.length > 8) {
        html += `<div class="vsc-search-more">+ ${res.matches.length - 8} more matches in this file...</div>`;
      }

      html += `
          </div>
        </div>
      `;
    });

    html += `</div>`;
    resultsContainer.innerHTML = html;

    resultsContainer.querySelectorAll(".vsc-search-file-header").forEach(hdr => {
      hdr.addEventListener("click", () => {
        openFile(hdr.dataset.file);
      });
    });

    resultsContainer.querySelectorAll(".vsc-search-line-item").forEach(item => {
      item.addEventListener("click", () => {
        openFile(item.dataset.file, parseInt(item.dataset.line, 10));
      });
    });

    renderActiveFile(currentSearchQuery);
  }

  // Interactive OOP Concepts Directory
  const OOP_CATALOG = [
    {
      concept: "Classes & Objects",
      fileKey: "project code/src/model/FoodItem.java",
      line: 11,
      badge: "Module 1",
      desc: "Base entity representing food donation with encapsulated state and behaviors."
    },
    {
      concept: "Encapsulation & Data Hiding",
      fileKey: "project code/src/model/FoodItem.java",
      line: 13,
      badge: "Module 1",
      desc: "Private fields with defensive setters validating quantity and non-negative valuation."
    },
    {
      concept: "Abstract Classes & Methods",
      fileKey: "project code/src/model/FoodItem.java",
      line: 139,
      badge: "Module 2",
      desc: "abstract class FoodItem declaring public abstract String getStorageInstructions()."
    },
    {
      concept: "Hierarchical Inheritance",
      fileKey: "project code/src/model/PerishableItem.java",
      line: 7,
      badge: "Module 2",
      desc: "public class PerishableItem extends FoodItem adding requiredTempCelsius."
    },
    {
      concept: "Dynamic Polymorphism (Dispatch)",
      fileKey: "project code/src/model/PerishableItem.java",
      line: 29,
      badge: "Module 2",
      desc: "@Override getStorageInstructions() dynamically resolves cold-chain directives at runtime."
    },
    {
      concept: "Method Overloading (Compile-Time)",
      fileKey: "project code/src/model/InventoryOperations.java",
      line: 18,
      badge: "Module 2",
      desc: "Overloaded searchItems(keyword), searchItems(category, onlyActive), getItemById(id)."
    },
    {
      concept: "Interfaces & Contract Realization",
      fileKey: "project code/src/database/FoodBankDAO.java",
      line: 15,
      badge: "Module 3",
      desc: "FoodBankDAO implements InventoryOperations enforcing loose coupling between UI and DB."
    },
    {
      concept: "Custom Exception (Food Safety)",
      fileKey: "project code/src/exception/ExpiredItemDistributionException.java",
      line: 7,
      badge: "Module 3",
      desc: "Checked exception strictly preventing checkout of items past expiry date."
    },
    {
      concept: "Custom Exception (Inventory Invariant)",
      fileKey: "project code/src/exception/InvalidQuantityException.java",
      line: 7,
      badge: "Module 3",
      desc: "Checked exception preventing non-positive checkout volumes and stock overdrafts."
    },
    {
      concept: "Singleton Design Pattern",
      fileKey: "project code/src/database/DatabaseManager.java",
      line: 14,
      badge: "Module 3",
      desc: "Thread-safe synchronized getInstance() providing single global SQLite connection."
    },
    {
      concept: "JDBC Persistence & Parameterization",
      fileKey: "project code/src/database/FoodBankDAO.java",
      line: 30,
      badge: "Module 4",
      desc: "PreparedStatements defending against SQL Injection and executing atomic transactions."
    },
    {
      concept: "Java Swing CardLayout Coordinator",
      fileKey: "project code/src/ui/MainFrame.java",
      line: 24,
      badge: "Module 4",
      desc: "Master JFrame managing CardLayout navigation across five modular business panels."
    },
    {
      concept: "Event-Driven Delegation Model",
      fileKey: "project code/src/ui/DistributionPanel.java",
      line: 150,
      badge: "Module 4",
      desc: "ActionListeners on checkout buttons triggering exception interception and bill calculation."
    },
    {
      concept: "In-Memory Bubble Sort (FEFO)",
      fileKey: "project code/src/service/PriorityPricingService.java",
      line: 110,
      badge: "Algorithm",
      desc: "Custom Bubble Sort ordering food inventory descending by Priority Distribution Index."
    },
    {
      concept: "Automated 35-Point Test Suite",
      fileKey: "project code/src/test/ProjectTestRunner.java",
      line: 31,
      badge: "Testing",
      desc: "Automated assertion harness executing 35 rigorous domain verification tests."
    }
  ];

  function renderOOPConceptsList() {
    const container = document.getElementById("vsc-oop-catalog");
    if (!container) return;

    let html = `
      <div class="vsc-oop-header">
        <div><strong>KTU PBCST304 OOP Implementation Map</strong></div>
        <div class="vsc-oop-sub">Click any concept to jump directly to the code implementation:</div>
      </div>
      <div class="vsc-oop-list">
    `;

    OOP_CATALOG.forEach(item => {
      html += `
        <div class="vsc-oop-card" data-file="${item.fileKey}" data-line="${item.line}">
          <div class="vsc-oop-card-top">
            <span class="vsc-oop-title">${item.concept}</span>
            <span class="vsc-oop-badge">${item.badge}</span>
          </div>
          <div class="vsc-oop-loc"><code>${item.fileKey}:${item.line}</code></div>
          <div class="vsc-oop-desc">${item.desc}</div>
        </div>
      `;
    });

    html += `</div>`;
    container.innerHTML = html;

    container.querySelectorAll(".vsc-oop-card").forEach(card => {
      card.addEventListener("click", () => {
        openFile(card.dataset.file, parseInt(card.dataset.line, 10));
      });
    });
  }

  // Setup UI Listeners
  function setupEventListeners() {
    const btnModeSwing = document.getElementById("btn-mode-swing");
    const btnModeVSCode = document.getElementById("btn-mode-vscode");
    const btnModeSplit = document.getElementById("btn-mode-split");
    const workspace = document.querySelector(".desktop-workspace");
    const vscContainer = document.getElementById("vscode-explorer-container");
    const jframeWindow = document.getElementById("main-jframe");

    function setViewMode(mode) {
      if (mode === "swing") {
        workspace.classList.remove("mode-vscode", "mode-split");
        workspace.classList.add("mode-swing");
        vscContainer.style.display = "none";
        jframeWindow.style.display = "flex";
        btnModeSwing.classList.add("active");
        btnModeVSCode.classList.remove("active");
        if (btnModeSplit) btnModeSplit.classList.remove("active");
      } else if (mode === "vscode") {
        workspace.classList.remove("mode-swing", "mode-split");
        workspace.classList.add("mode-vscode");
        vscContainer.style.display = "flex";
        jframeWindow.style.display = "none";
        btnModeVSCode.classList.add("active");
        btnModeSwing.classList.remove("active");
        if (btnModeSplit) btnModeSplit.classList.remove("active");
      } else if (mode === "split") {
        workspace.classList.remove("mode-swing", "mode-vscode");
        workspace.classList.add("mode-split");
        vscContainer.style.display = "flex";
        jframeWindow.style.display = "flex";
        if (btnModeSplit) btnModeSplit.classList.add("active");
        btnModeSwing.classList.remove("active");
        btnModeVSCode.classList.remove("active");
      }
    }

    if (btnModeSwing) btnModeSwing.addEventListener("click", () => setViewMode("swing"));
    if (btnModeVSCode) btnModeVSCode.addEventListener("click", () => setViewMode("vscode"));
    if (btnModeSplit) btnModeSplit.addEventListener("click", () => setViewMode("split"));

    // Sidebar Toggle Functionality (Maximize codespace view)
    const workspaceBody = document.getElementById("vsc-workspace-body");
    const toggleSidebarBtn = document.getElementById("vsc-btn-toggle-sidebar");
    const collapseSidebarBtn = document.getElementById("vsc-btn-collapse-sidebar");
    const toggleSidebarText = document.getElementById("vsc-sidebar-toggle-text");
    const toggleSidebarIcon = document.getElementById("vsc-sidebar-toggle-icon");

    setSidebarVisibility = function(visible) {
      if (!workspaceBody) return;
      const backdrop = document.getElementById("vsc-sidebar-backdrop");
      if (visible) {
        workspaceBody.classList.remove("sidebar-hidden");
        if (toggleSidebarBtn) toggleSidebarBtn.classList.add("active-state");
        if (toggleSidebarText) toggleSidebarText.textContent = "Hide Sidebar";
        if (toggleSidebarIcon) toggleSidebarIcon.textContent = "◨";
        if (backdrop) backdrop.classList.add("active");
      } else {
        workspaceBody.classList.add("sidebar-hidden");
        if (toggleSidebarBtn) toggleSidebarBtn.classList.remove("active-state");
        if (toggleSidebarText) toggleSidebarText.textContent = "Show Sidebar";
        if (toggleSidebarIcon) toggleSidebarIcon.textContent = "◧";
        if (backdrop) backdrop.classList.remove("active");
      }
    };

    toggleSidebar = function() {
      if (!workspaceBody) return;
      const isCurrentlyHidden = workspaceBody.classList.contains("sidebar-hidden");
      setSidebarVisibility(isCurrentlyHidden);
    };

    if (toggleSidebarBtn) toggleSidebarBtn.addEventListener("click", toggleSidebar);
    if (collapseSidebarBtn) collapseSidebarBtn.addEventListener("click", () => setSidebarVisibility(false));

    // Backdrop click on mobile closes sidebar drawer
    const backdropEl = document.getElementById("vsc-sidebar-backdrop");
    if (backdropEl) backdropEl.addEventListener("click", () => setSidebarVisibility(false));

    // Mobile Panel Close buttons (✕ in header)
    ["vsc-m-close-explorer", "vsc-m-close-search", "vsc-m-close-oop"].forEach(id => {
      const btn = document.getElementById(id);
      if (btn) btn.addEventListener("click", () => setSidebarVisibility(false));
    });

    // Keyboard Shortcut (Ctrl+B / Cmd+B) like authentic VS Code
    document.addEventListener("keydown", (e) => {
      if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === "b") {
        const vscContainer = document.getElementById("vscode-explorer-container");
        if (vscContainer && vscContainer.style.display !== "none") {
          e.preventDefault();
          toggleSidebar();
        }
      }
    });

    // Activity Bar Navigation with Click-to-Toggle behavior
    const actBtns = document.querySelectorAll(".vsc-activity-btn");
    actBtns.forEach(btn => {
      btn.addEventListener("click", () => {
        const targetView = btn.dataset.view;
        const isAlreadyActive = btn.classList.contains("active");
        const isSidebarHidden = workspaceBody && workspaceBody.classList.contains("sidebar-hidden");

        // If clicking active button while visible, collapse sidebar
        if (isAlreadyActive && !isSidebarHidden) {
          setSidebarVisibility(false);
          return;
        }

        // If sidebar is hidden, open it
        if (isSidebarHidden) {
          setSidebarVisibility(true);
        }

        actBtns.forEach(b => b.classList.remove("active"));
        btn.classList.add("active");
        currentActiveTabSidebar = targetView;

        document.querySelectorAll(".vsc-sidebar-panel").forEach(p => p.classList.remove("active"));
        const panel = document.getElementById(`vsc-panel-${targetView}`);
        if (panel) panel.classList.add("active");

        if (targetView === "oop") {
          renderOOPConceptsList();
        }
      });
    });

    // Global Search Input
    const searchInput = document.getElementById("vsc-search-input");
    if (searchInput) {
      searchInput.addEventListener("input", (e) => {
        performSearch(e.target.value);
      });
    }

    const clearSearchBtn = document.getElementById("vsc-clear-search");
    if (clearSearchBtn) {
      clearSearchBtn.addEventListener("click", () => {
        if (searchInput) searchInput.value = "";
        performSearch("");
      });
    }

    // Copy Code Button
    const btnCopyCode = document.getElementById("vsc-btn-copy-code");
    if (btnCopyCode) {
      btnCopyCode.addEventListener("click", () => {
        let file = null;
        Object.keys(CHRONOCHEF_CODEBASE).forEach(k => {
          if (normalizePath(k) === activeFileKey) file = CHRONOCHEF_CODEBASE[k];
        });
        if (!file) return;
        navigator.clipboard.writeText(file.content).then(() => {
          btnCopyCode.innerHTML = "<span>✓</span><span>Copied!</span>";
          setTimeout(() => {
            btnCopyCode.innerHTML = "<span>📋</span><span>Copy Code</span>";
          }, 2000);
        });
      });
    }

    // Download File Button
    const btnDownload = document.getElementById("vsc-btn-download-file");
    if (btnDownload) {
      btnDownload.addEventListener("click", () => {
        let file = null;
        Object.keys(CHRONOCHEF_CODEBASE).forEach(k => {
          if (normalizePath(k) === activeFileKey) file = CHRONOCHEF_CODEBASE[k];
        });
        if (!file) return;
        const blob = new Blob([file.content], { type: "text/plain;charset=utf-8" });
        const url = URL.createObjectURL(blob);
        const a = document.createElement("a");
        a.href = url;
        a.download = file.fileName;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
      });
    }

    // Code Zoom & Mobile Sizing Engine
    const btnZoomOut = document.getElementById("vsc-btn-zoom-out");
    const btnZoomIn = document.getElementById("vsc-btn-zoom-in");
    const btnZoomReset = document.getElementById("vsc-btn-zoom-reset");
    const headZoomOut = document.getElementById("vsc-head-zoom-out");
    const headZoomIn = document.getElementById("vsc-head-zoom-in");
    const mzbZoomOut = document.getElementById("vsc-mzb-zoom-out");
    const mzbZoomIn = document.getElementById("vsc-mzb-zoom-in");
    const mzbToggleSidebar = document.getElementById("vsc-mzb-toggle-sidebar");
    const mzbWrap = document.getElementById("vsc-mzb-wrap");

    if (btnZoomOut) btnZoomOut.addEventListener("click", () => applyZoom(currentZoomIdx - 1));
    if (btnZoomIn) btnZoomIn.addEventListener("click", () => applyZoom(currentZoomIdx + 1));
    if (btnZoomReset) btnZoomReset.addEventListener("click", () => applyZoomByScale(100));

    if (headZoomOut) headZoomOut.addEventListener("click", () => applyZoom(currentZoomIdx - 1));
    if (headZoomIn) headZoomIn.addEventListener("click", () => applyZoom(currentZoomIdx + 1));

    if (mzbZoomOut) mzbZoomOut.addEventListener("click", () => applyZoom(currentZoomIdx - 1));
    if (mzbZoomIn) mzbZoomIn.addEventListener("click", () => applyZoom(currentZoomIdx + 1));
    if (mzbToggleSidebar) mzbToggleSidebar.addEventListener("click", toggleSidebar);

    // Mobile Zoom Presets (35%, 50%, 70%, 100%)
    document.querySelectorAll(".vsc-mzb-preset").forEach(pBtn => {
      pBtn.addEventListener("click", () => {
        const targetZoom = parseInt(pBtn.dataset.zoom, 10);
        applyZoomByScale(targetZoom);
      });
    });

    // Word Wrap Toggle (Synchronized across desktop and mobile bars)
    const btnWrap = document.getElementById("vsc-btn-wrap-lines");
    function toggleWordWrap() {
      const codeContent = document.getElementById("vsc-code-editor-content");
      if (codeContent) {
        const isWrapped = codeContent.classList.toggle("word-wrap-enabled");
        if (btnWrap) btnWrap.classList.toggle("active", isWrapped);
        if (mzbWrap) mzbWrap.classList.toggle("active", isWrapped);
      }
    }

    if (btnWrap) btnWrap.addEventListener("click", toggleWordWrap);
    if (mzbWrap) mzbWrap.addEventListener("click", toggleWordWrap);

    // Touch pinch-to-zoom on code pane for smartphones
    const scrollPane = document.querySelector(".vsc-code-scroll-pane");
    if (scrollPane) {
      let initialDist = 0;
      let startIdx = currentZoomIdx;

      scrollPane.addEventListener("touchstart", (e) => {
        if (e.touches.length === 2) {
          initialDist = Math.hypot(
            e.touches[0].clientX - e.touches[1].clientX,
            e.touches[0].clientY - e.touches[1].clientY
          );
          startIdx = currentZoomIdx;
        }
      }, { passive: true });

      scrollPane.addEventListener("touchmove", (e) => {
        if (e.touches.length === 2 && initialDist > 0) {
          const currentDist = Math.hypot(
            e.touches[0].clientX - e.touches[1].clientX,
            e.touches[0].clientY - e.touches[1].clientY
          );
          const ratio = currentDist / initialDist;
          if (ratio < 0.72) {
            applyZoom(startIdx - 2);
          } else if (ratio < 0.86) {
            applyZoom(startIdx - 1);
          } else if (ratio > 1.35) {
            applyZoom(startIdx + 2);
          } else if (ratio > 1.15) {
            applyZoom(startIdx + 1);
          }
        }
      }, { passive: true });

      scrollPane.addEventListener("touchend", () => {
        initialDist = 0;
      });
    }

    // Mobile Auto-Configuration on Startup
    if (window.innerWidth <= 768) {
      // Auto-collapse sidebar on phone so full screen is dedicated to code
      setSidebarVisibility(false);
      // Auto-enable word wrap on mobile
      const codeContent = document.getElementById("vsc-code-editor-content");
      if (codeContent) codeContent.classList.add("word-wrap-enabled");
      if (btnWrap) btnWrap.classList.add("active");
      if (mzbWrap) mzbWrap.classList.add("active");
    }

    // Initial Zoom Application
    applyCurrentZoom();
  }

  // Global Code Zoom Scale State
  // Allows zooming out all the way to 30% so full lines fit cleanly on phone screens
  const zoomLevels = [30, 35, 40, 50, 60, 70, 80, 90, 100, 115, 130, 150];
  let currentZoomIdx = window.innerWidth <= 768 ? 3 : 8; // Index 3 is 50% on mobile, index 8 is 100% on desktop

  function applyZoom(idx) {
    if (idx < 0) idx = 0;
    if (idx >= zoomLevels.length) idx = zoomLevels.length - 1;
    currentZoomIdx = idx;
    applyCurrentZoom();
  }

  function applyZoomByScale(targetScale) {
    let closestIdx = 0;
    let minDiff = 9999;
    zoomLevels.forEach((scale, i) => {
      const diff = Math.abs(scale - targetScale);
      if (diff < minDiff) {
        minDiff = diff;
        closestIdx = i;
      }
    });
    applyZoom(closestIdx);
  }

  function applyCurrentZoom() {
    const scale = zoomLevels[currentZoomIdx];
    const codeContent = document.getElementById("vsc-code-editor-content");
    if (codeContent) {
      codeContent.style.fontSize = `${12.5 * (scale / 100)}px`;
      codeContent.style.lineHeight = `${20 * (scale / 100)}px`;
    }

    // Update line number gutter: compact for small scales on mobile
    document.querySelectorAll(".vsc-line-num").forEach(numEl => {
      const numWidth = Math.max(22, Math.round(48 * (scale / 100)));
      numEl.style.width = `${numWidth}px`;
      numEl.style.fontSize = `${Math.max(8, 11 * (scale / 100))}px`;
    });

    // Update display labels
    const label1 = document.getElementById("vsc-zoom-display");
    const label2 = document.getElementById("vsc-head-zoom-display");
    if (label1) label1.textContent = `${scale}%`;
    if (label2) label2.textContent = `${scale}%`;

    // Highlight active preset button on mobile zoom bar
    document.querySelectorAll(".vsc-mzb-preset").forEach(pBtn => {
      const pScale = parseInt(pBtn.dataset.zoom, 10);
      pBtn.classList.toggle("active", Math.abs(pScale - scale) <= 5);
    });
  }

  // Auto-init on DOMContentLoaded
  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", initVSCodeExplorer);
  } else {
    initVSCodeExplorer();
  }
})();
