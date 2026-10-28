/**
 * ChronoChef Web Application — Client-Side Logic & Business Rules
 * Faithfully mirrors the Java SE desktop codebase:
 * - DataSeeder.java (Initial 10 items)
 * - PriorityPricingService.java (PDI formula & Bubble Sort)
 * - ExpiredItemDistributionException.java (Food safety enforcer)
 * - FoodBankDAO.java (Data persistence with localStorage)
 */

// =========================================================================
// 1. DATE HELPERS & SEED DATA DEFINITIONS
// =========================================================================

function getFormattedDate(offsetDays = 0) {
  const d = new Date();
  d.setDate(d.getDate() + offsetDays);
  const year = d.getFullYear();
  const month = String(d.getMonth() + 1).padStart(2, '0');
  const day = String(d.getDate()).padStart(2, '0');
  return `${year}-${month}-${day}`;
}

const DEFAULT_ITEMS = [
  {
    id: "FD-1001",
    name: "Greek Yogurt (Pack of 4)",
    category: "Dairy",
    type: "PERISHABLE",
    quantity: 15,
    unit: "Packs",
    receivedDate: getFormattedDate(-10),
    expiryDate: getFormattedDate(-2), // Expired 2 days ago
    basePrice: 40.0,
    optimumTemp: 4.0,
    batchNumber: null
  },
  {
    id: "FD-1002",
    name: "Artisan Sandwich Bread",
    category: "Bakery",
    type: "PERISHABLE",
    quantity: 25,
    unit: "Loaves",
    receivedDate: getFormattedDate(-1),
    expiryDate: getFormattedDate(0), // Expires today
    basePrice: 25.0,
    optimumTemp: 20.0,
    batchNumber: null
  },
  {
    id: "FD-1003",
    name: "Fresh Whole Milk 1L",
    category: "Dairy",
    type: "PERISHABLE",
    quantity: 30,
    unit: "Liters",
    receivedDate: getFormattedDate(-2),
    expiryDate: getFormattedDate(1), // Expires tomorrow
    basePrice: 35.0,
    optimumTemp: 4.0,
    batchNumber: null
  },
  {
    id: "FD-1004",
    name: "Organic Ripe Strawberries",
    category: "Produce",
    type: "PERISHABLE",
    quantity: 18,
    unit: "kg",
    receivedDate: getFormattedDate(-1),
    expiryDate: getFormattedDate(2), // Expires in 2 days
    basePrice: 50.0,
    optimumTemp: 3.0,
    batchNumber: null
  },
  {
    id: "FD-1005",
    name: "Baby Spinach & Mixed Greens",
    category: "Produce",
    type: "PERISHABLE",
    quantity: 20,
    unit: "Bags",
    receivedDate: getFormattedDate(-1),
    expiryDate: getFormattedDate(4), // Expires in 4 days
    basePrice: 20.0,
    optimumTemp: 5.0,
    batchNumber: null
  },
  {
    id: "FD-1006",
    name: "Cottage Cheese 500g",
    category: "Dairy",
    type: "PERISHABLE",
    quantity: 22,
    unit: "Tubs",
    receivedDate: getFormattedDate(-2),
    expiryDate: getFormattedDate(6), // Expires in 6 days
    basePrice: 45.0,
    optimumTemp: 4.0,
    batchNumber: null
  },
  {
    id: "FD-1007",
    name: "Farm Fresh Crisp Apples",
    category: "Produce",
    type: "PERISHABLE",
    quantity: 60,
    unit: "kg",
    receivedDate: getFormattedDate(-3),
    expiryDate: getFormattedDate(12), // Expires in 12 days
    basePrice: 30.0,
    optimumTemp: 10.0,
    batchNumber: null
  },
  {
    id: "FD-1008",
    name: "Whole Wheat Pasta 500g",
    category: "Grains",
    type: "PACKAGED",
    quantity: 45,
    unit: "Packets",
    receivedDate: getFormattedDate(-5),
    expiryDate: getFormattedDate(20), // Expires in 20 days
    basePrice: 25.0,
    optimumTemp: null,
    batchNumber: "BATCH-PASTA-902"
  },
  {
    id: "FD-1009",
    name: "Canned Red Kidney Beans",
    category: "Canned Goods",
    type: "PACKAGED",
    quantity: 80,
    unit: "Cans",
    receivedDate: getFormattedDate(-15),
    expiryDate: getFormattedDate(60), // Expires in 60 days
    basePrice: 28.0,
    optimumTemp: null,
    batchNumber: "BATCH-BEAN-110"
  },
  {
    id: "FD-1010",
    name: "Long Grain White Basmati Rice",
    category: "Grains",
    type: "PACKAGED",
    quantity: 100,
    unit: "kg",
    receivedDate: getFormattedDate(-20),
    expiryDate: getFormattedDate(180), // Expires in 180 days
    basePrice: 45.0,
    optimumTemp: null,
    batchNumber: "BATCH-RICE-2024"
  }
];

const DEFAULT_DISTRIBUTIONS = [
  {
    txnId: "TXN-SEED-01",
    itemId: "FD-1002",
    itemName: "Artisan Sandwich Bread",
    recipient: "St. Jude Community Shelter",
    qty: 5,
    unit: "Loaves",
    gross: 125.0,
    subsidyPercent: 100.0,
    netPaid: 0.0,
    timestamp: `${getFormattedDate(0)} 10:15:00`
  },
  {
    txnId: "TXN-SEED-02",
    itemId: "FD-1006",
    itemName: "Cottage Cheese 500g",
    recipient: "City Harvest Relief Kitchen",
    qty: 4,
    unit: "Tubs",
    gross: 180.0,
    subsidyPercent: 50.0,
    netPaid: 90.0,
    timestamp: `${getFormattedDate(0)} 11:30:00`
  }
];

// =========================================================================
// 2. STATE MANAGER (LOCAL STORAGE PERSISTENCE)
// =========================================================================

class FoodBankStore {
  constructor() {
    this.STORAGE_KEY_ITEMS = "chronochef_food_items_v1";
    this.STORAGE_KEY_TXNS = "chronochef_distributions_v1";
    this.items = [];
    this.distributions = [];
    this.loadState();
  }

  loadState() {
    const storedItems = localStorage.getItem(this.STORAGE_KEY_ITEMS);
    const storedTxns = localStorage.getItem(this.STORAGE_KEY_TXNS);

    if (storedItems) {
      try {
        this.items = JSON.parse(storedItems);
      } catch (e) {
        this.items = [...DEFAULT_ITEMS];
      }
    } else {
      this.items = [...DEFAULT_ITEMS];
      this.saveItems();
    }

    if (storedTxns) {
      try {
        this.distributions = JSON.parse(storedTxns);
      } catch (e) {
        this.distributions = [...DEFAULT_DISTRIBUTIONS];
      }
    } else {
      this.distributions = [...DEFAULT_DISTRIBUTIONS];
      this.saveDistributions();
    }
  }

  saveItems() {
    localStorage.setItem(this.STORAGE_KEY_ITEMS, JSON.stringify(this.items));
  }

  saveDistributions() {
    localStorage.setItem(this.STORAGE_KEY_TXNS, JSON.stringify(this.distributions));
  }

  resetToDefault() {
    this.items = [...DEFAULT_ITEMS];
    this.distributions = [...DEFAULT_DISTRIBUTIONS];
    this.saveItems();
    this.saveDistributions();
  }

  addItem(item) {
    this.items.unshift(item);
    this.saveItems();
  }

  updateStock(itemId, deltaQty) {
    const item = this.items.find(i => i.id === itemId);
    if (item) {
      item.quantity = Math.max(0, item.quantity + deltaQty);
      this.saveItems();
      return true;
    }
    return false;
  }

  deleteItem(itemId) {
    this.items = this.items.filter(i => i.id !== itemId);
    this.saveItems();
  }

  addDistribution(record) {
    this.distributions.unshift(record);
    this.saveDistributions();
  }
}

const store = new FoodBankStore();

// =========================================================================
// 3. CORE MATHEMATICAL ALGORITHMS & OOP LOGIC
// =========================================================================

/**
 * PriorityPricingService emulation
 */
const PriorityPricingService = {
  /**
   * Days Remaining (D) formula
   */
  calculateDaysRemaining(expiryDateStr) {
    const today = new Date();
    today.setHours(0, 0, 0, 0);

    const expiry = new Date(expiryDateStr);
    expiry.setHours(0, 0, 0, 0);

    const diffMs = expiry.getTime() - today.getTime();
    return Math.round(diffMs / (1000 * 60 * 60 * 24));
  },

  /**
   * PDI Score Formula:
   * If D < 0: 0
   * Else: max(1, min(100, 100 - (D * 2)))
   */
  calculatePdiScore(daysRemaining) {
    if (daysRemaining < 0) return 0;
    const score = 100 - (daysRemaining * 2);
    return Math.max(1, Math.min(100, score));
  },

  /**
   * Urgency Level Mapping
   */
  getUrgencyLevel(daysRemaining) {
    if (daysRemaining < 0) return "EXPIRED";
    if (daysRemaining <= 5) return "URGENT";
    if (daysRemaining <= 15) return "HIGH";
    if (daysRemaining <= 30) return "MEDIUM";
    return "LOW";
  },

  /**
   * Dynamic Subsidy Percentage Rule:
   * D <= 2 days: 100% Free
   * 3 <= D <= 7: 50% Off
   * D > 7: 0% (Standard)
   */
  calculateSubsidyPercentage(daysRemaining) {
    if (daysRemaining < 0) return 0;
    if (daysRemaining <= 2) return 100.0;
    if (daysRemaining <= 7) return 50.0;
    return 0.0;
  },

  /**
   * Polymorphic Storage Instructions (Dynamic Method Dispatch)
   */
  getStorageInstructions(item) {
    if (item.type === "PERISHABLE") {
      return `Chilled storage at ${item.optimumTemp ?? 4.0}°C in walk-in cold room`;
    } else {
      const lot = item.batchNumber ? ` (Lot: ${item.batchNumber})` : "";
      return `Dry pantry at room temperature, keep sealed${lot}`;
    }
  },

  /**
   * Classic Bubble Sort Algorithm on item list by descending PDI
   */
  bubbleSortByUrgency(itemsList) {
    const arr = [...itemsList];
    const n = arr.length;
    for (let i = 0; i < n - 1; i++) {
      for (let j = 0; j < n - i - 1; j++) {
        const pdiA = this.calculatePdiScore(this.calculateDaysRemaining(arr[j].expiryDate));
        const pdiB = this.calculatePdiScore(this.calculateDaysRemaining(arr[j + 1].expiryDate));
        if (pdiA < pdiB) {
          // Swap
          const temp = arr[j];
          arr[j] = arr[j + 1];
          arr[j + 1] = temp;
        }
      }
    }
    return arr;
  }
};

// =========================================================================
// 4. UI CONTROLLER & EVENT DELEGATION
// =========================================================================

document.addEventListener("DOMContentLoaded", () => {
  // Navigation Tabs Switching (CardLayout)
  const navButtons = document.querySelectorAll(".nav-btn");
  const tabPanels = document.querySelectorAll(".tab-panel");

  function switchTab(targetTabId) {
    navButtons.forEach(btn => {
      btn.classList.toggle("active", btn.dataset.tab === targetTabId);
    });
    tabPanels.forEach(panel => {
      panel.classList.toggle("active", panel.id === targetTabId);
    });

    // Refresh targeted views
    if (targetTabId === "tab-inventory") renderInventoryTable();
    if (targetTabId === "tab-distribution") populateDistributionDropdown();
    if (targetTabId === "tab-management") renderManagementTable();
    if (targetTabId === "tab-analytics") renderAnalytics();
  }

  navButtons.forEach(btn => {
    btn.addEventListener("click", () => switchTab(btn.dataset.tab));
  });

  // Dark / Light Theme Toggle
  const btnThemeToggle = document.getElementById("btn-theme-toggle");
  btnThemeToggle.addEventListener("click", () => {
    const currentTheme = document.body.getAttribute("data-theme");
    const nextTheme = currentTheme === "dark" ? "light" : "dark";
    document.body.setAttribute("data-theme", nextTheme);
    showToast(`Switched to ${nextTheme} mode`, "info");
  });

  // Reset Demo DB Button
  const btnResetDb = document.getElementById("btn-reset-db");
  btnResetDb.addEventListener("click", () => {
    if (confirm("Reset database back to the 10 college demo items and initial transactions?")) {
      store.resetToDefault();
      renderAllViews();
      showToast("Database restored to initial 10 items!", "success");
    }
  });

  // Toggle Subclass Fields on Intake Form
  const inTypeSelect = document.getElementById("in-type");
  const grpOptimumTemp = document.getElementById("grp-optimum-temp");
  const grpBatchNum = document.getElementById("grp-batch-num");

  inTypeSelect.addEventListener("change", (e) => {
    const isPerishable = e.target.value === "PERISHABLE";
    grpOptimumTemp.style.display = isPerishable ? "flex" : "none";
    grpBatchNum.style.display = isPerishable ? "none" : "flex";
  });

  // Default Intake Dates
  document.getElementById("in-received-date").value = getFormattedDate(0);
  document.getElementById("in-expiry-date").value = getFormattedDate(5);

  // Submit Intake Form
  const intakeForm = document.getElementById("intake-form");
  intakeForm.addEventListener("submit", (e) => {
    e.preventDefault();
    const id = document.getElementById("in-id").value.trim();
    const name = document.getElementById("in-name").value.trim();
    const category = document.getElementById("in-category").value;
    const type = document.getElementById("in-type").value;
    const qty = parseInt(document.getElementById("in-qty").value, 10);
    const unit = document.getElementById("in-unit").value.trim();
    const price = parseFloat(document.getElementById("in-price").value);
    const receivedDate = document.getElementById("in-received-date").value;
    const expiryDate = document.getElementById("in-expiry-date").value;

    if (!id || !name || isNaN(qty) || qty <= 0) {
      showToast("Invalid inputs! Ensure quantity is positive.", "danger");
      return;
    }

    const newItem = {
      id,
      name,
      category,
      type,
      quantity: qty,
      unit,
      receivedDate,
      expiryDate,
      basePrice: price,
      optimumTemp: type === "PERISHABLE" ? parseFloat(document.getElementById("in-temp").value) : null,
      batchNumber: type === "PACKAGED" ? document.getElementById("in-batch").value.trim() : null
    };

    store.addItem(newItem);
    intakeForm.reset();
    document.getElementById("in-received-date").value = getFormattedDate(0);
    document.getElementById("in-expiry-date").value = getFormattedDate(5);

    showToast(`Registered "${name}" into warehouse!`, "success");
    switchTab("tab-inventory");
  });

  // Run Bubble Sort on Inventory
  const btnBubbleSort = document.getElementById("btn-trigger-bubblesort");
  btnBubbleSort.addEventListener("click", () => {
    store.items = PriorityPricingService.bubbleSortByUrgency(store.items);
    store.saveItems();
    renderInventoryTable();
    showToast("Bubble Sort completed! Urgent items floated to top.", "success");
  });

  // Inventory Filters
  const searchInput = document.getElementById("inventory-search");
  const filterCat = document.getElementById("filter-category");
  const filterUrg = document.getElementById("filter-urgency");

  searchInput.addEventListener("input", renderInventoryTable);
  filterCat.addEventListener("change", renderInventoryTable);
  filterUrg.addEventListener("change", renderInventoryTable);

  // Distribution Form Live Calculation
  const distItemSelect = document.getElementById("dist-item-select");
  const distQtyInput = document.getElementById("dist-qty");
  const distItemPreview = document.getElementById("dist-item-preview");

  distItemSelect.addEventListener("change", updateDistributionPreview);
  distQtyInput.addEventListener("input", updateDistributionPreview);

  // Confirm Distribution
  const distForm = document.getElementById("distribution-form");
  distForm.addEventListener("submit", handleDistributionSubmit);

  // Safety Exception Modal Dismissal
  document.getElementById("btn-close-modal").addEventListener("click", () => {
    document.getElementById("safety-modal").classList.remove("active");
  });

  // Print Receipt Button
  document.getElementById("btn-print-receipt").addEventListener("click", () => {
    const text = document.getElementById("receipt-output").innerText;
    navigator.clipboard.writeText(text).then(() => {
      showToast("Receipt copied to clipboard!", "info");
    });
  });

  // Initial Render
  renderAllViews();
});

// =========================================================================
// 5. VIEW RENDERING MODULES
// =========================================================================

function renderAllViews() {
  renderInventoryTable();
  populateDistributionDropdown();
  renderManagementTable();
  renderAnalytics();
}

function renderInventoryTable() {
  const tbody = document.getElementById("inventory-tbody");
  if (!tbody) return;

  const search = document.getElementById("inventory-search").value.toLowerCase();
  const catFilter = document.getElementById("filter-category").value;
  const urgFilter = document.getElementById("filter-urgency").value;

  let urgentCount = 0;
  let highCount = 0;
  let safeCount = 0;
  let expiredCount = 0;

  const filtered = store.items.filter(item => {
    const days = PriorityPricingService.calculateDaysRemaining(item.expiryDate);
    const urgency = PriorityPricingService.getUrgencyLevel(days);

    if (urgency === "URGENT") urgentCount++;
    else if (urgency === "HIGH") highCount++;
    else if (urgency === "EXPIRED") expiredCount++;
    else safeCount++;

    const matchesSearch = item.name.toLowerCase().includes(search) || 
                          item.category.toLowerCase().includes(search) ||
                          item.id.toLowerCase().includes(search) ||
                          (item.batchNumber && item.batchNumber.toLowerCase().includes(search));
    const matchesCat = catFilter === "ALL" || item.category === catFilter;
    const matchesUrg = urgFilter === "ALL" || urgency === urgFilter;

    return matchesSearch && matchesCat && matchesUrg;
  });

  // Update Top KPI Counters
  document.getElementById("kpi-urgent-count").innerText = urgentCount;
  document.getElementById("kpi-high-count").innerText = highCount;
  document.getElementById("kpi-safe-count").innerText = safeCount;
  document.getElementById("kpi-expired-count").innerText = expiredCount;

  if (filtered.length === 0) {
    tbody.innerHTML = `<tr><td colspan="11" style="text-align:center; padding:2rem; color:var(--text-muted);">No inventory items match your search filters.</td></tr>`;
    return;
  }

  tbody.innerHTML = filtered.map(item => {
    const days = PriorityPricingService.calculateDaysRemaining(item.expiryDate);
    const pdi = PriorityPricingService.calculatePdiScore(days);
    const urgency = PriorityPricingService.getUrgencyLevel(days);
    const storage = PriorityPricingService.getStorageInstructions(item);

    const badgeClass = {
      "URGENT": "badge-urgent",
      "HIGH": "badge-high",
      "MEDIUM": "badge-medium",
      "LOW": "badge-low",
      "EXPIRED": "badge-expired"
    }[urgency] || "badge-low";

    const daysText = days < 0 ? `${Math.abs(days)}d Overdue` : `${days} Days`;
    const daysColor = days < 0 ? "#f87171" : (days <= 2 ? "#fbbf24" : "var(--text-primary)");

    return `
      <tr>
        <td><code>${item.id}</code></td>
        <td><strong>${item.name}</strong></td>
        <td>${item.category}</td>
        <td><span style="font-size:0.75rem; color:var(--text-muted);">${item.type}</span></td>
        <td><strong>${item.quantity}</strong> ${item.unit}</td>
        <td>${item.expiryDate}</td>
        <td style="color:${daysColor}; font-weight:600;">${daysText}</td>
        <td><span class="pdi-pill">${pdi}</span></td>
        <td><span class="badge ${badgeClass}">${urgency}</span></td>
        <td>₹${item.basePrice.toFixed(2)}</td>
        <td style="font-size:0.8rem; color:var(--text-secondary); max-width:240px;">${storage}</td>
      </tr>
    `;
  }).join('');
}

function populateDistributionDropdown() {
  const select = document.getElementById("dist-item-select");
  if (!select) return;

  const currentVal = select.value;
  select.innerHTML = `<option value="">-- Choose item to dispatch --</option>` + 
    store.items.map(item => {
      const days = PriorityPricingService.calculateDaysRemaining(item.expiryDate);
      const tag = days < 0 ? " [EXPIRED - QUARANTINED]" : (days <= 2 ? " [100% SUBSIDY]" : "");
      return `<option value="${item.id}">${item.id} — ${item.name} (${item.quantity} ${item.unit} in stock)${tag}</option>`;
    }).join('');

  if (currentVal) select.value = currentVal;
  updateDistributionPreview();
}

function updateDistributionPreview() {
  const itemId = document.getElementById("dist-item-select").value;
  const qtyInput = document.getElementById("dist-qty");
  const qty = parseInt(qtyInput.value, 10) || 0;
  const previewBox = document.getElementById("dist-item-preview");

  if (!itemId) {
    previewBox.style.display = "none";
    document.getElementById("calc-original-value").innerText = "₹0.00";
    document.getElementById("calc-subsidy-tier").innerText = "0% (Standard)";
    document.getElementById("calc-subsidy-saved").innerText = "-₹0.00";
    document.getElementById("calc-final-price").innerText = "₹0.00";
    return;
  }

  const item = store.items.find(i => i.id === itemId);
  if (!item) return;

  const days = PriorityPricingService.calculateDaysRemaining(item.expiryDate);
  const pdi = PriorityPricingService.calculatePdiScore(days);
  const subsidyPercent = PriorityPricingService.calculateSubsidyPercentage(days);

  previewBox.style.display = "grid";
  document.getElementById("prev-days-left").innerText = days < 0 ? `${Math.abs(days)} days ago (EXPIRED)` : `${days} days`;
  document.getElementById("prev-pdi").innerText = pdi;
  document.getElementById("prev-stock").innerText = `${item.quantity} ${item.unit}`;
  document.getElementById("prev-base-price").innerText = `₹${item.basePrice.toFixed(2)}`;

  if (days < 0) {
    document.getElementById("calc-original-value").innerText = "BLOCKED";
    document.getElementById("calc-subsidy-tier").innerText = "QUARANTINED (0%)";
    document.getElementById("calc-subsidy-saved").innerText = "₹0.00";
    document.getElementById("calc-final-price").innerText = "UNAVAILABLE";
    return;
  }

  const gross = item.basePrice * qty;
  const discount = gross * (subsidyPercent / 100);
  const finalPrice = Math.max(0, gross - discount);

  document.getElementById("calc-original-value").innerText = `₹${gross.toFixed(2)}`;
  document.getElementById("calc-subsidy-tier").innerText = `${subsidyPercent.toFixed(0)}% (${subsidyPercent === 100 ? 'FREE DISTRIBUTION' : (subsidyPercent === 50 ? 'HALF PRICE' : 'STANDARD')})`;
  document.getElementById("calc-subsidy-saved").innerText = `-₹${discount.toFixed(2)}`;
  document.getElementById("calc-final-price").innerText = `₹${finalPrice.toFixed(2)}`;
}

function handleDistributionSubmit(e) {
  e.preventDefault();
  const itemId = document.getElementById("dist-item-select").value;
  const qty = parseInt(document.getElementById("dist-qty").value, 10);
  const shelter = document.getElementById("dist-shelter").value.trim();

  if (!itemId || isNaN(qty) || qty <= 0 || !shelter) {
    showToast("Please fill in all distribution fields correctly.", "danger");
    return;
  }

  const item = store.items.find(i => i.id === itemId);
  if (!item) return;

  const days = PriorityPricingService.calculateDaysRemaining(item.expiryDate);

  // SAFETY CHECK 1: Expired Food Check (Simulating ExpiredItemDistributionException)
  if (days < 0) {
    document.getElementById("modal-exception-msg").innerHTML = `
      <b>Safety Violation:</b> Attempted to distribute <b>${item.name}</b> (Batch: ${item.id}), which expired <b>${Math.abs(days)} days ago</b> (${item.expiryDate}).<br/><br/>
      Under food bank safety laws, expired food items cannot be disbursed or subsidized.
    `;
    document.getElementById("safety-modal").classList.add("active");
    return;
  }

  // SAFETY CHECK 2: Stock bounds check (Simulating InvalidQuantityException)
  if (qty > item.quantity) {
    showToast(`Insufficient stock! Only ${item.quantity} ${item.unit} available in warehouse.`, "danger");
    return;
  }

  // Calculate pricing
  const subsidyPercent = PriorityPricingService.calculateSubsidyPercentage(days);
  const gross = item.basePrice * qty;
  const discount = gross * (subsidyPercent / 100);
  const netPaid = Math.max(0, gross - discount);
  const txnId = `TXN-${Date.now().toString().slice(-6)}`;
  const timestamp = `${getFormattedDate(0)} ${new Date().toTimeString().split(' ')[0]}`;

  // Deduct stock in store
  store.updateStock(itemId, -qty);

  // Record transaction in audit log
  const record = {
    txnId,
    itemId: item.id,
    itemName: item.name,
    recipient: shelter,
    qty,
    unit: item.unit,
    gross,
    subsidyPercent,
    netPaid,
    timestamp
  };
  store.addDistribution(record);

  // Generate ASCII Terminal Receipt
  const receipt = `
============================================================
              CHRONOCHEF FOOD BANK DISTRIBUTION SYSTEM
============================================================
Transaction ID : ${txnId}
Date & Time    : ${timestamp}
Recipient      : ${shelter}
Operator       : Volunteer Desk 01
------------------------------------------------------------
Item Dispatched: ${item.name}
Item Code      : ${item.id} (${item.type})
Quantity Issued: ${qty} ${item.unit}
Shelf Life Left: ${days} Day(s) remaining
Storage Advice : ${PriorityPricingService.getStorageInstructions(item)}
------------------------------------------------------------
Original Value : ₹${gross.toFixed(2)} (Base: ₹${item.basePrice.toFixed(2)}/${item.unit})
Dynamic Subsidy: ${subsidyPercent.toFixed(0)}% Relief Tier
Subsidy Granted: -₹${discount.toFixed(2)}
------------------------------------------------------------
FINAL CHARGE   : ₹${netPaid.toFixed(2)} ${netPaid === 0 ? "(100% FREE RELIEF)" : ""}
============================================================
       FOOD SAFETY VERIFIED • ZERO SPOILAGE CLEARANCE
============================================================
  `.trim();

  document.getElementById("receipt-output").innerText = receipt;

  // Clear input
  document.getElementById("dist-qty").value = "";
  populateDistributionDropdown();
  renderAllViews();

  showToast(`Successfully dispatched ${qty} ${item.unit} to ${shelter}!`, "success");
}

function renderManagementTable() {
  const tbody = document.getElementById("management-tbody");
  if (!tbody) return;

  tbody.innerHTML = store.items.map(item => `
    <tr>
      <td><code>${item.id}</code></td>
      <td><strong>${item.name}</strong></td>
      <td>${item.category}</td>
      <td><strong>${item.quantity}</strong> ${item.unit}</td>
      <td>₹${item.basePrice.toFixed(2)}</td>
      <td>${item.expiryDate}</td>
      <td>
        <button class="btn btn-outline-sm" onclick="quickRestock('${item.id}', 10)">+10</button>
        <button class="btn btn-outline-sm" onclick="quickRestock('${item.id}', 25)">+25</button>
      </td>
      <td>
        <button class="btn btn-danger btn-sm" onclick="deleteStockItem('${item.id}')">Write Off</button>
      </td>
    </tr>
  `).join('');
}

window.quickRestock = function(itemId, qty) {
  store.updateStock(itemId, qty);
  renderAllViews();
  showToast(`Restocked +${qty} units!`, "info");
};

window.deleteStockItem = function(itemId) {
  if (confirm(`Are you sure you want to write off / delete item ${itemId}?`)) {
    store.deleteItem(itemId);
    renderAllViews();
    showToast(`Item ${itemId} written off.`, "info");
  }
};

function renderAnalytics() {
  const totalItems = store.items.length;
  const totalUnits = store.items.reduce((sum, i) => sum + i.quantity, 0);

  let wastePreventedKg = 0;
  let subsidiesGranted = 0;
  const shelters = new Set();

  store.distributions.forEach(d => {
    // If food was subsidized (100% or 50%), it prevented waste
    if (d.subsidyPercent >= 50) {
      wastePreventedKg += (d.qty * 1.2); // approx 1.2kg per unit
    }
    subsidiesGranted += (d.gross - d.netPaid);
    shelters.add(d.recipient);
  });

  document.getElementById("stat-total-items").innerText = totalItems;
  document.getElementById("stat-total-units").innerText = totalUnits;
  document.getElementById("stat-waste-prevented").innerText = `${Math.round(wastePreventedKg)} kg`;
  document.getElementById("stat-subsidies-granted").innerText = `₹${subsidiesGranted.toLocaleString('en-IN', { minimumFractionDigits: 2 })}`;
  document.getElementById("stat-shelters-served").innerText = shelters.size;
  document.getElementById("stat-distributions-count").innerText = store.distributions.length;

  const tbody = document.getElementById("analytics-tbody");
  if (!tbody) return;

  if (store.distributions.length === 0) {
    tbody.innerHTML = `<tr><td colspan="8" style="text-align:center; padding:1.5rem; color:var(--text-muted);">No distribution transactions recorded yet.</td></tr>`;
    return;
  }

  tbody.innerHTML = store.distributions.map(d => `
    <tr>
      <td><code>${d.txnId}</code></td>
      <td><strong>${d.itemName}</strong></td>
      <td>${d.recipient}</td>
      <td>${d.qty} ${d.unit}</td>
      <td>₹${d.gross.toFixed(2)}</td>
      <td><span class="badge ${d.subsidyPercent === 100 ? 'badge-urgent' : (d.subsidyPercent === 50 ? 'badge-high' : 'badge-low')}">${d.subsidyPercent.toFixed(0)}%</span></td>
      <td><strong style="color:var(--emerald);">₹${d.netPaid.toFixed(2)}</strong></td>
      <td style="font-size:0.75rem; color:var(--text-muted);">${d.timestamp}</td>
    </tr>
  `).join('');
}

function showToast(message, type = "info") {
  const container = document.getElementById("toast-container");
  if (!container) return;

  const toast = document.createElement("div");
  toast.className = `toast ${type}`;
  toast.innerText = message;
  container.appendChild(toast);

  setTimeout(() => {
    toast.style.opacity = "0";
    toast.style.transform = "translateX(40px)";
    setTimeout(() => toast.remove(), 300);
  }, 3500);
}
