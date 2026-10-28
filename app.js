/**
 * ChronoChef - Java Swing & AWT Runtime Emulator Controller
 * College Project PBCST304 (Object Oriented Programming)
 * 
 * Recreates the exact runtime behavior of:
 * - MainFrame.java (CardLayout Coordinator)
 * - InputPanel.java (Module A: Data Input)
 * - InventoryPanel.java (Module B: Expiry & PDI Tracker)
 * - ManagementPanel.java (Module C: Warehouse Maintenance & CRUD)
 * - DistributionPanel.java (Module D: Subsidy Billing & Receipt Slip)
 * - AnalyticsPanel.java (Module E: Social Impact Reporting)
 * - PriorityPricingService.java (PDI formula & Bubble Sort)
 */

// =========================================================================
// 1. DATA SEEDER & INITIAL MODEL (DataSeeder.java)
// =========================================================================

function getFormattedDate(offsetDays) {
  const d = new Date();
  d.setDate(d.getDate() + offsetDays);
  return d.toISOString().split("T")[0];
}

const DEFAULT_ITEMS = [
  {
    id: "FD-1001",
    name: "Pasteurized Whole Milk 1L",
    category: "Dairy",
    type: "PERISHABLE",
    quantity: 35,
    unit: "Liters",
    receivedDate: getFormattedDate(-1),
    expiryDate: getFormattedDate(1), // Urgent: 1 day left
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
    receivedDate: getFormattedDate(-2),
    expiryDate: getFormattedDate(2), // Urgent: 2 days left
    basePrice: 25.0,
    optimumTemp: 20.0,
    batchNumber: null
  },
  {
    id: "FD-1003",
    name: "Organic Ripe Bananas",
    category: "Produce",
    type: "PERISHABLE",
    quantity: 50,
    unit: "kg",
    receivedDate: getFormattedDate(-3),
    expiryDate: getFormattedDate(0), // Urgent: Expires today
    basePrice: 35.0,
    optimumTemp: 13.0,
    batchNumber: null
  },
  {
    id: "FD-1004",
    name: "Fresh Strawberry Yogurt 200g",
    category: "Dairy",
    type: "PERISHABLE",
    quantity: 15,
    unit: "Tubs",
    receivedDate: getFormattedDate(-8),
    expiryDate: getFormattedDate(-1), // Quarantined: Expired yesterday
    basePrice: 18.0,
    optimumTemp: 3.5,
    batchNumber: null
  },
  {
    id: "FD-1005",
    name: "Fresh Spinach Bunches",
    category: "Produce",
    type: "PERISHABLE",
    quantity: 20,
    unit: "Bags",
    receivedDate: getFormattedDate(-1),
    expiryDate: getFormattedDate(4), // High: 4 days left
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
    expiryDate: getFormattedDate(6), // High: 6 days left
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
    expiryDate: getFormattedDate(12), // Safe: 12 days left
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
    expiryDate: getFormattedDate(20), // Safe: 20 days left
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
    expiryDate: getFormattedDate(60), // Safe: 60 days left
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
    expiryDate: getFormattedDate(180), // Safe: 180 days left
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
// 2. STATE MANAGER (SINGLE SOURCE OF TRUTH - FoodBankDAO Simulation)
// =========================================================================

class FoodBankStore {
  constructor() {
    this.STORAGE_KEY_ITEMS = "chronochef_swing_items_v2";
    this.STORAGE_KEY_TXNS = "chronochef_swing_txns_v2";
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

  updateItem(updated) {
    const idx = this.items.findIndex(i => i.id === updated.id);
    if (idx !== -1) {
      this.items[idx] = { ...this.items[idx], ...updated };
      this.saveItems();
      return true;
    }
    return false;
  }

  deleteItem(itemId) {
    this.items = this.items.filter(i => i.id !== itemId);
    this.saveItems();
    return true;
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

  setStockToZero(itemId) {
    const item = this.items.find(i => i.id === itemId);
    if (item) {
      item.quantity = 0.0;
      this.saveItems();
      return true;
    }
    return false;
  }

  addDistribution(record) {
    this.distributions.unshift(record);
    this.saveDistributions();
  }
}

const store = new FoodBankStore();

// =========================================================================
// 3. PRIORITY PRICING SERVICE (PriorityPricingService.java)
// =========================================================================

const PriorityPricingService = {
  calculateDaysRemaining(expiryDateStr) {
    const today = new Date();
    today.setHours(0, 0, 0, 0);

    const parts = expiryDateStr.split("-");
    const expDate = new Date(parts[0], parts[1] - 1, parts[2]);
    expDate.setHours(0, 0, 0, 0);

    const diffMs = expDate.getTime() - today.getTime();
    return Math.round(diffMs / (1000 * 60 * 60 * 24));
  },

  calculatePdiScore(daysRemaining) {
    if (daysRemaining < 0) return 0;
    const rawPdi = 100 - (daysRemaining * 2);
    return Math.max(1, Math.min(100, rawPdi));
  },

  getUrgencyLevel(daysRemaining) {
    if (daysRemaining < 0) return "EXPIRED";
    if (daysRemaining <= 5) return "URGENT";
    if (daysRemaining <= 15) return "HIGH";
    if (daysRemaining <= 30) return "MEDIUM";
    return "LOW";
  },

  calculateSubsidyPercentage(daysRemaining) {
    if (daysRemaining < 0) return 0.0;
    if (daysRemaining <= 2) return 100.0; // 100% Free emergency relief
    if (daysRemaining <= 5) return 50.0;  // 50% Community relief
    return 0.0;                          // Standard base price
  },

  getStorageInstructions(item) {
    if (item.type === "PERISHABLE") {
      const temp = item.optimumTemp !== null ? item.optimumTemp : 4.0;
      return `Refrigerate continuously at ${temp}°C. Inspect packaging for cold chain integrity.`;
    } else {
      const batch = item.batchNumber || "UNTRACKED";
      return `Store in dry room temperature conditions (Lot #${batch}).`;
    }
  },

  bubbleSortByUrgency(itemsList) {
    const arr = [...itemsList];
    const n = arr.length;
    for (let i = 0; i < n - 1; i++) {
      for (let j = 0; j < n - i - 1; j++) {
        const d1 = this.calculateDaysRemaining(arr[j].expiryDate);
        const pdi1 = this.calculatePdiScore(d1);

        const d2 = this.calculateDaysRemaining(arr[j + 1].expiryDate);
        const pdi2 = this.calculatePdiScore(d2);

        if (pdi1 < pdi2) {
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
// 4. AUTHENTIC SWING JOPTIONPANE DIALOG HELPER
// =========================================================================

function showJOptionPane(options) {
  const overlay = document.getElementById("joptionpane-overlay");
  const titleElem = document.getElementById("joptionpane-title");
  const msgElem = document.getElementById("joptionpane-message");
  const iconElem = document.getElementById("joptionpane-icon");
  const actionsElem = document.getElementById("joptionpane-actions");

  titleElem.innerText = options.title || "Message";
  msgElem.innerText = options.message || "";

  // Icon styles
  const iconMap = {
    info: { icon: "ℹ️", cls: "info" },
    warning: { icon: "⚠️", cls: "warning" },
    danger: { icon: "🛑", cls: "danger" },
    question: { icon: "❓", cls: "question" }
  };
  const iconMeta = iconMap[options.type || "info"] || iconMap.info;
  iconElem.innerText = iconMeta.icon;
  iconElem.className = `joptionpane-icon ${iconMeta.cls}`;

  // Generate buttons
  actionsElem.innerHTML = "";
  const buttons = options.buttons || ["OK"];
  buttons.forEach(btnText => {
    const btn = document.createElement("button");
    btn.className = "swing-btn";
    btn.innerText = btnText;
    btn.style.minWidth = "70px";
    btn.addEventListener("click", () => {
      overlay.classList.remove("active");
      if (options.onSelect) options.onSelect(btnText);
    });
    actionsElem.appendChild(btn);
  });

  // Focus primary button
  overlay.classList.add("active");
  const primaryBtn = actionsElem.querySelector("button");
  if (primaryBtn) primaryBtn.focus();
}

document.getElementById("btn-joptionpane-close").addEventListener("click", () => {
  document.getElementById("joptionpane-overlay").classList.remove("active");
});

// =========================================================================
// 5. SWING CARDLAYOUT COORDINATION (MainFrame.java)
// =========================================================================

const CARD_MAP = {
  CARD_INPUT: "card-input",
  CARD_INVENTORY: "card-inventory",
  CARD_MANAGE: "card-manage",
  CARD_DISTRIBUTE: "card-distribute",
  CARD_ANALYTICS: "card-analytics"
};

let currentCard = "CARD_INVENTORY";

function switchCard(cardKey) {
  currentCard = cardKey;

  // Update button highlights
  document.querySelectorAll(".swing-nav-btn").forEach(btn => {
    btn.classList.toggle("active", btn.dataset.card === cardKey);
  });

  // Update visible card panel
  document.querySelectorAll(".swing-card-view").forEach(panel => {
    panel.classList.toggle("active", panel.id === CARD_MAP[cardKey]);
  });

  // Refresh data on card activation (exact MainFrame.java behavior)
  if (cardKey === "CARD_INVENTORY") renderInventoryTable();
  if (cardKey === "CARD_MANAGE") populateManagementItemSelector();
  if (cardKey === "CARD_DISTRIBUTE") populateDistributionDropdown();
  if (cardKey === "CARD_ANALYTICS") renderAnalyticsData();
}

// =========================================================================
// 6. VIEW 1: DATA INPUT PANEL (InputPanel.java)
// =========================================================================

function setupInputPanel() {
  const form = document.getElementById("form-input-panel");
  const inType = document.getElementById("in-type");
  const lblExtra = document.getElementById("lbl-in-extra");
  const inExtra = document.getElementById("in-extra");
  const btnClear = document.getElementById("btn-input-clear");

  // Dynamic label based on Perishable / Packaged type
  inType.addEventListener("change", (e) => {
    if (e.target.value === "PERISHABLE") {
      lblExtra.innerText = "Storage Temperature (°C):";
      inExtra.value = "4.0";
    } else {
      lblExtra.innerText = "Manufacturer Lot / Batch #:";
      inExtra.value = "BATCH-LOT-101";
    }
  });

  // Default dates
  document.getElementById("in-received-date").value = getFormattedDate(0);
  document.getElementById("in-expiry-date").value = getFormattedDate(5);

  btnClear.addEventListener("click", () => {
    form.reset();
    document.getElementById("in-received-date").value = getFormattedDate(0);
    document.getElementById("in-expiry-date").value = getFormattedDate(5);
  });

  form.addEventListener("submit", (e) => {
    e.preventDefault();

    const id = document.getElementById("in-id").value.trim();
    const name = document.getElementById("in-name").value.trim();
    const category = document.getElementById("in-category").value;
    const type = document.getElementById("in-type").value;
    const qty = parseFloat(document.getElementById("in-qty").value);
    const unit = document.getElementById("in-unit").value;
    const receivedDate = document.getElementById("in-received-date").value;
    const expiryDate = document.getElementById("in-expiry-date").value;
    const price = parseFloat(document.getElementById("in-price").value);
    const extraVal = inExtra.value.trim();

    if (!id || !name || isNaN(qty) || qty <= 0) {
      showJOptionPane({
        title: "Validation Error",
        message: "Please enter a valid Item ID, Name, and positive quantity.",
        type: "warning",
        buttons: ["OK"]
      });
      return;
    }

    // Check duplicate ID
    if (store.items.some(i => i.id.toUpperCase() === id.toUpperCase())) {
      showJOptionPane({
        title: "Duplicate Key Error",
        message: `Item with ID [${id}] already exists in database.`,
        type: "danger",
        buttons: ["OK"]
      });
      return;
    }

    const newItem = {
      id: id.toUpperCase(),
      name,
      category,
      type,
      quantity: qty,
      unit,
      receivedDate,
      expiryDate,
      basePrice: price,
      optimumTemp: type === "PERISHABLE" ? parseFloat(extraVal) || 4.0 : null,
      batchNumber: type === "PACKAGED" ? extraVal : null
    };

    store.addItem(newItem);
    form.reset();
    document.getElementById("in-received-date").value = getFormattedDate(0);
    document.getElementById("in-expiry-date").value = getFormattedDate(5);

    showJOptionPane({
      title: "Success",
      message: `Food item [${newItem.id} - ${newItem.name}] saved to database successfully!`,
      type: "info",
      buttons: ["OK"],
      onSelect: () => {
        switchCard("CARD_INVENTORY");
      }
    });
  });
}

// =========================================================================
// 7. VIEW 2: INVENTORY & EXPIRY TRACKER (InventoryPanel.java)
// =========================================================================

function renderInventoryTable() {
  const tbody = document.getElementById("inventory-tbody");
  if (!tbody) return;

  const searchQuery = (document.getElementById("inv-search-input").value || "").toLowerCase().trim();
  const filterVal = document.getElementById("inv-filter-select").value || "ALL";

  let items = [...store.items];

  // Apply search query
  if (searchQuery) {
    items = items.filter(i => 
      i.id.toLowerCase().includes(searchQuery) ||
      i.name.toLowerCase().includes(searchQuery) ||
      i.category.toLowerCase().includes(searchQuery)
    );
  }

  // Apply priority filter
  if (filterVal !== "ALL") {
    items = items.filter(item => {
      const days = PriorityPricingService.calculateDaysRemaining(item.expiryDate);
      if (filterVal === "SAFE") return days > 5;
      if (filterVal === "URGENT") return days >= 0 && days <= 5;
      if (filterVal === "HIGH") return days >= 6 && days <= 15;
      if (filterVal === "EXPIRED") return days < 0;
      return true;
    });
  }

  if (items.length === 0) {
    tbody.innerHTML = `<tr><td colspan="12" style="text-align: center; padding: 16px; color: #64748B;">No inventory items match filter.</td></tr>`;
    return;
  }

  tbody.innerHTML = items.map(item => {
    const days = PriorityPricingService.calculateDaysRemaining(item.expiryDate);
    const pdi = PriorityPricingService.calculatePdiScore(days);
    const priority = PriorityPricingService.getUrgencyLevel(days);
    const instructions = PriorityPricingService.getStorageInstructions(item);

    let rowClass = "";
    if (priority === "EXPIRED") rowClass = "swing-row-expired";
    else if (priority === "URGENT") rowClass = "swing-row-urgent";
    else if (priority === "HIGH") rowClass = "swing-row-high";

    const daysText = days < 0 ? `${Math.abs(days)}d Overdue` : `${days} Days`;
    const statusText = days < 0 ? "QUARANTINED" : (days <= 2 ? "100% SUBSIDY" : (days <= 5 ? "50% SUBSIDY" : "SAFE"));

    return `
      <tr class="${rowClass}">
        <td><strong>${item.id}</strong></td>
        <td>${item.name}</td>
        <td>${item.category}</td>
        <td>${item.type}</td>
        <td><strong>${item.quantity}</strong></td>
        <td>${item.unit}</td>
        <td>${item.expiryDate}</td>
        <td>${daysText}</td>
        <td><strong>${pdi}</strong></td>
        <td><strong>${priority}</strong></td>
        <td>${statusText}</td>
        <td style="max-width: 200px; overflow: hidden; text-overflow: ellipsis;">${instructions}</td>
      </tr>
    `;
  }).join("");
}

function setupInventoryPanel() {
  document.getElementById("btn-inv-search").addEventListener("click", renderInventoryTable);
  document.getElementById("inv-search-input").addEventListener("input", renderInventoryTable);
  document.getElementById("inv-filter-select").addEventListener("change", renderInventoryTable);
  document.getElementById("btn-inv-refresh").addEventListener("click", () => {
    document.getElementById("inv-search-input").value = "";
    document.getElementById("inv-filter-select").value = "ALL";
    renderInventoryTable();
  });

  // Run in-memory Bubble Sort by Urgency
  document.getElementById("btn-inv-bubblesort").addEventListener("click", () => {
    store.items = PriorityPricingService.bubbleSortByUrgency(store.items);
    store.saveItems();
    renderInventoryTable();
    showJOptionPane({
      title: "Sort Complete",
      message: "Bubble Sort executed successfully!\nItems arranged in descending order of urgency (highest PDI first).",
      type: "info",
      buttons: ["OK"]
    });
  });
}

// =========================================================================
// 8. VIEW 3: MANAGEMENT PANEL (ManagementPanel.java)
// =========================================================================

function populateManagementItemSelector() {
  const select = document.getElementById("mgmt-item-select");
  if (!select) return;

  const currentSelection = select.value;
  select.innerHTML = "";

  if (store.items.length === 0) {
    select.innerHTML = `<option value="">-- No items in catalog --</option>`;
    clearManagementFields();
    return;
  }

  store.items.forEach(item => {
    const opt = document.createElement("option");
    opt.value = item.id;
    opt.innerText = `${item.id} - ${item.name} (${item.quantity} ${item.unit})`;
    select.appendChild(opt);
  });

  if (currentSelection && store.items.some(i => i.id === currentSelection)) {
    select.value = currentSelection;
  }

  loadManagementFields(select.value);
}

function loadManagementFields(itemId) {
  const item = store.items.find(i => i.id === itemId);
  if (!item) {
    clearManagementFields();
    return;
  }

  document.getElementById("mgmt-id").value = item.id;
  document.getElementById("mgmt-name").value = item.name;
  document.getElementById("mgmt-category").value = item.category;
  document.getElementById("mgmt-qty").value = item.quantity;
  document.getElementById("mgmt-unit").value = item.unit;
  document.getElementById("mgmt-expiry").value = item.expiryDate;
  document.getElementById("mgmt-price").value = item.basePrice;
}

function clearManagementFields() {
  document.getElementById("mgmt-id").value = "";
  document.getElementById("mgmt-name").value = "";
  document.getElementById("mgmt-qty").value = "";
  document.getElementById("mgmt-unit").value = "";
  document.getElementById("mgmt-expiry").value = "";
  document.getElementById("mgmt-price").value = "";
  document.getElementById("mgmt-restock-qty").value = "";
}

function setupManagementPanel() {
  const select = document.getElementById("mgmt-item-select");
  select.addEventListener("change", () => loadManagementFields(select.value));

  document.getElementById("btn-mgmt-refresh-list").addEventListener("click", () => {
    populateManagementItemSelector();
  });

  // Restock Item
  document.getElementById("btn-mgmt-restock").addEventListener("click", () => {
    const id = document.getElementById("mgmt-id").value;
    if (!id) {
      showJOptionPane({ title: "Warning", message: "Please select an item first.", type: "warning", buttons: ["OK"] });
      return;
    }

    const addQty = parseFloat(document.getElementById("mgmt-restock-qty").value);
    if (isNaN(addQty) || addQty <= 0) {
      showJOptionPane({ title: "Validation Error", message: "Restock quantity must be positive.", type: "danger", buttons: ["OK"] });
      return;
    }

    store.updateStock(id, addQty);
    document.getElementById("mgmt-restock-qty").value = "";
    populateManagementItemSelector();
    renderInventoryTable();

    showJOptionPane({
      title: "Success",
      message: `Successfully restocked ${addQty} units!`,
      type: "info",
      buttons: ["OK"]
    });
  });

  // Update Item Details
  document.getElementById("btn-mgmt-update").addEventListener("click", () => {
    const id = document.getElementById("mgmt-id").value;
    if (!id) {
      showJOptionPane({ title: "Warning", message: "Please select an item first.", type: "warning", buttons: ["OK"] });
      return;
    }

    const name = document.getElementById("mgmt-name").value.trim();
    const category = document.getElementById("mgmt-category").value;
    const unit = document.getElementById("mgmt-unit").value.trim();
    const expiry = document.getElementById("mgmt-expiry").value;
    const price = parseFloat(document.getElementById("mgmt-price").value);

    if (!name || !expiry || isNaN(price)) {
      showJOptionPane({ title: "Error", message: "Name, Expiry Date, and Price cannot be empty.", type: "danger", buttons: ["OK"] });
      return;
    }

    store.updateItem({
      id,
      name,
      category,
      unit,
      expiryDate: expiry,
      basePrice: price
    });

    populateManagementItemSelector();
    renderInventoryTable();

    showJOptionPane({
      title: "Success",
      message: "Item details updated successfully!",
      type: "info",
      buttons: ["OK"]
    });
  });

  // Write-Off Stock (Set to 0)
  document.getElementById("btn-mgmt-writeoff").addEventListener("click", () => {
    const id = document.getElementById("mgmt-id").value;
    const name = document.getElementById("mgmt-name").value;
    if (!id) {
      showJOptionPane({ title: "Warning", message: "Please select an item first.", type: "warning", buttons: ["OK"] });
      return;
    }

    showJOptionPane({
      title: "Confirm Stock Write-Off",
      message: `Write-off all physical stock for [${id} - ${name}]?\nQuantity will be set to 0, but the item record will remain in the catalog.`,
      type: "warning",
      buttons: ["Yes", "No"],
      onSelect: (btn) => {
        if (btn === "Yes") {
          store.setStockToZero(id);
          document.getElementById("mgmt-qty").value = "0";
          populateManagementItemSelector();
          renderInventoryTable();

          showJOptionPane({
            title: "Stock Written Off",
            message: "Physical stock written off (Quantity set to 0).\nItem record remains preserved in catalog.",
            type: "info",
            buttons: ["OK"]
          });
        }
      }
    });
  });

  // Permanently Delete Item Info
  document.getElementById("btn-mgmt-delete").addEventListener("click", () => {
    const id = document.getElementById("mgmt-id").value;
    const name = document.getElementById("mgmt-name").value;
    if (!id) {
      showJOptionPane({ title: "Warning", message: "Please select an item to delete.", type: "warning", buttons: ["OK"] });
      return;
    }

    showJOptionPane({
      title: "Confirm Complete Deletion",
      message: `PERMANENTLY DELETE item info for [${id} - ${name}]?\n\nThis will completely purge this item and all its information from the database and catalog.`,
      type: "danger",
      buttons: ["Yes", "No"],
      onSelect: (btn) => {
        if (btn === "Yes") {
          store.deleteItem(id);
          clearManagementFields();
          populateManagementItemSelector();
          renderInventoryTable();

          showJOptionPane({
            title: "Item Removed",
            message: "Item info permanently deleted from the database.\nRecord completely removed from catalog.",
            type: "info",
            buttons: ["OK"]
          });
        }
      }
    });
  });
}

// =========================================================================
// 9. VIEW 4: DISTRIBUTION & BILLING PANEL (DistributionPanel.java)
// =========================================================================

function populateDistributionDropdown() {
  const select = document.getElementById("dist-item-select");
  if (!select) return;

  const currentVal = select.value;
  select.innerHTML = "";

  if (store.items.length === 0) {
    select.innerHTML = `<option value="">-- No items available --</option>`;
    updateDistributionStatus();
    return;
  }

  store.items.forEach(item => {
    const opt = document.createElement("option");
    opt.value = item.id;
    const days = PriorityPricingService.calculateDaysRemaining(item.expiryDate);
    const tag = days < 0 ? " [EXPIRED]" : (days <= 2 ? " [100% SUBSIDY]" : "");
    opt.innerText = `${item.id} - ${item.name} (${item.quantity} ${item.unit})${tag}`;
    select.appendChild(opt);
  });

  if (currentVal && store.items.some(i => i.id === currentVal)) {
    select.value = currentVal;
  }

  updateDistributionStatus();
}

function updateDistributionStatus() {
  const select = document.getElementById("dist-item-select");
  const statusElem = document.getElementById("dist-status-text");
  const subsidyElem = document.getElementById("dist-subsidy-text");

  const itemId = select ? select.value : null;
  const item = store.items.find(i => i.id === itemId);

  if (!item) {
    statusElem.innerText = "Stock: - | Days Left: -";
    statusElem.style.color = "#1E293B";
    subsidyElem.innerText = "Subsidy: - | Net Price: -";
    subsidyElem.style.color = "#007832";
    return;
  }

  const days = PriorityPricingService.calculateDaysRemaining(item.expiryDate);
  statusElem.innerText = `Stock: ${item.quantity} ${item.unit} | Days Left: ${days}`;

  if (days < 0) {
    statusElem.style.color = "#DC2626";
    subsidyElem.innerText = "BLOCKED: Item is Expired";
    subsidyElem.style.color = "#DC2626";
  } else {
    statusElem.style.color = "#1E293B";
    const subsidy = PriorityPricingService.calculateSubsidyPercentage(days);
    const effPrice = item.basePrice * (1 - subsidy / 100);
    subsidyElem.innerText = `${subsidy.toFixed(0)}% Subsidy | Net: Rs. ${effPrice.toFixed(2)}/${item.unit}`;
    subsidyElem.style.color = "#007832";
  }
}

function setupDistributionPanel() {
  const select = document.getElementById("dist-item-select");
  select.addEventListener("change", updateDistributionStatus);

  // Generate Preview
  document.getElementById("btn-dist-preview").addEventListener("click", () => {
    const itemId = select.value;
    const item = store.items.find(i => i.id === itemId);
    if (!item) {
      showJOptionPane({ title: "Warning", message: "Please select a food item.", type: "warning", buttons: ["OK"] });
      return;
    }

    const qty = parseFloat(document.getElementById("dist-qty").value);
    const recipient = document.getElementById("dist-recipient").value.trim() || "Community Beneficiary";

    if (isNaN(qty) || qty <= 0) {
      showJOptionPane({ title: "Validation Error", message: "Please enter a valid numeric quantity.", type: "danger", buttons: ["OK"] });
      return;
    }

    const days = PriorityPricingService.calculateDaysRemaining(item.expiryDate);
    if (days < 0) {
      showJOptionPane({
        title: "Food Safety Violation",
        message: `Food Safety Violation: Item [${item.name}] expired ${Math.abs(days)} days ago.\nDistribution and pricing calculations are strictly prohibited.`,
        type: "danger",
        buttons: ["OK"]
      });
      return;
    }

    const subsidy = PriorityPricingService.calculateSubsidyPercentage(days);
    const gross = item.basePrice * qty;
    const discount = gross * (subsidy / 100);
    const netPaid = Math.max(0, gross - discount);

    const receipt = `
============================================================
              CHRONOCHEF FOOD BANK DISTRIBUTION SYSTEM
============================================================
Transaction ID : TXN-PREVIEW
Date & Time    : ${getFormattedDate(0)} ${new Date().toTimeString().split(' ')[0]}
Recipient      : ${recipient}
Operator       : Volunteer Desk 01
------------------------------------------------------------
Item Dispatched: ${item.name}
Item Code      : ${item.id} (${item.type})
Quantity Issued: ${qty} ${item.unit}
Shelf Life Left: ${days} Day(s) remaining
Storage Advice : ${PriorityPricingService.getStorageInstructions(item)}
------------------------------------------------------------
Original Value : Rs. ${gross.toFixed(2)} (Base: Rs. ${item.basePrice.toFixed(2)}/${item.unit})
Dynamic Subsidy: ${subsidy.toFixed(0)}% Relief Tier
Subsidy Granted: -Rs. ${discount.toFixed(2)}
------------------------------------------------------------
TOTAL CHARGE   : Rs. ${netPaid.toFixed(2)} ${netPaid === 0 ? "(100% FREE RELIEF)" : ""}
============================================================
       FOOD SAFETY VERIFIED • ZERO SPOILAGE CLEARANCE
============================================================
    `.trim();

    document.getElementById("dist-receipt-area").value = receipt;
  });

  // Confirm Distribution
  document.getElementById("btn-dist-confirm").addEventListener("click", () => {
    const itemId = select.value;
    const item = store.items.find(i => i.id === itemId);
    if (!item) {
      showJOptionPane({ title: "Warning", message: "Please select a food item.", type: "warning", buttons: ["OK"] });
      return;
    }

    const qty = parseFloat(document.getElementById("dist-qty").value);
    const recipient = document.getElementById("dist-recipient").value.trim() || "Community Beneficiary";

    if (isNaN(qty) || qty <= 0) {
      showJOptionPane({ title: "Validation Error", message: "Please enter a valid numeric quantity.", type: "danger", buttons: ["OK"] });
      return;
    }

    const days = PriorityPricingService.calculateDaysRemaining(item.expiryDate);

    // SAFETY CHECK 1: ExpiredItemDistributionException
    if (days < 0) {
      showJOptionPane({
        title: "Food Safety Violation (ExpiredItemDistributionException)",
        message: `Food Safety Violation: Item [${item.name}] expired ${Math.abs(days)} days ago.\nDistribution and subsidy calculations are strictly prohibited under public health laws.`,
        type: "danger",
        buttons: ["OK"]
      });
      return;
    }

    // SAFETY CHECK 2: InvalidQuantityException (Stock bound)
    if (qty > item.quantity) {
      showJOptionPane({
        title: "Invalid Quantity Exception",
        message: `Insufficient stock! Only ${item.quantity} ${item.unit} available in warehouse.`,
        type: "danger",
        buttons: ["OK"]
      });
      return;
    }

    // Deduct stock
    store.updateStock(itemId, -qty);

    const subsidy = PriorityPricingService.calculateSubsidyPercentage(days);
    const gross = item.basePrice * qty;
    const discount = gross * (subsidy / 100);
    const netPaid = Math.max(0, gross - discount);
    const txnId = `TXN-${Date.now().toString().slice(-6)}`;
    const timestamp = `${getFormattedDate(0)} ${new Date().toTimeString().split(' ')[0]}`;

    const record = {
      txnId,
      itemId: item.id,
      itemName: item.name,
      recipient,
      qty,
      unit: item.unit,
      gross,
      subsidyPercent: subsidy,
      netPaid,
      timestamp
    };
    store.addDistribution(record);

    // Final receipt
    const receipt = `
============================================================
              CHRONOCHEF FOOD BANK DISTRIBUTION SYSTEM
============================================================
Transaction ID : ${txnId}
Date & Time    : ${timestamp}
Recipient      : ${recipient}
Operator       : Volunteer Desk 01
------------------------------------------------------------
Item Dispatched: ${item.name}
Item Code      : ${item.id} (${item.type})
Quantity Issued: ${qty} ${item.unit}
Shelf Life Left: ${days} Day(s) remaining
Storage Advice : ${PriorityPricingService.getStorageInstructions(item)}
------------------------------------------------------------
Original Value : Rs. ${gross.toFixed(2)} (Base: Rs. ${item.basePrice.toFixed(2)}/${item.unit})
Dynamic Subsidy: ${subsidy.toFixed(0)}% Relief Tier
Subsidy Granted: -Rs. ${discount.toFixed(2)}
------------------------------------------------------------
TOTAL PAID     : Rs. ${netPaid.toFixed(2)} ${netPaid === 0 ? "(100% FREE RELIEF)" : ""}
============================================================
       FOOD SAFETY VERIFIED • ZERO SPOILAGE CLEARANCE
============================================================
    `.trim();

    document.getElementById("dist-receipt-area").value = receipt;
    document.getElementById("dist-qty").value = "";

    populateDistributionDropdown();
    renderInventoryTable();

    showJOptionPane({
      title: "Transaction Confirmed",
      message: `Successfully issued ${qty} ${item.unit} of [${item.name}] to ${recipient}!\nReceipt generated.`,
      type: "info",
      buttons: ["OK"]
    });
  });

  document.getElementById("btn-dist-clear").addEventListener("click", () => {
    document.getElementById("dist-qty").value = "";
    document.getElementById("dist-receipt-area").value = "Receipt preview will appear here upon entering distribution details.";
  });

  document.getElementById("btn-dist-copy").addEventListener("click", () => {
    const text = document.getElementById("dist-receipt-area").value;
    navigator.clipboard.writeText(text).then(() => {
      showJOptionPane({ title: "Copied", message: "Receipt copied to system clipboard!", type: "info", buttons: ["OK"] });
    });
  });
}

// =========================================================================
// 10. VIEW 5: ANALYTICS PANEL (AnalyticsPanel.java)
// =========================================================================

function renderAnalyticsData() {
  const totalItems = store.items.length;
  const totalQuantity = store.items.reduce((sum, i) => sum + i.quantity, 0);

  let urgentCount = 0;
  let expiredCount = 0;

  store.items.forEach(item => {
    const days = PriorityPricingService.calculateDaysRemaining(item.expiryDate);
    if (days < 0) expiredCount++;
    else if (days <= 5) urgentCount++;
  });

  const totalDistributed = store.distributions.length;
  const totalSubsidized = store.distributions.reduce((sum, d) => sum + (d.gross - d.netPaid), 0);

  document.getElementById("stat-total-items").innerText = totalItems;
  document.getElementById("stat-total-quantity").innerText = totalQuantity.toFixed(1);
  document.getElementById("stat-urgent-count").innerText = urgentCount;
  document.getElementById("stat-expired-count").innerText = expiredCount;
  document.getElementById("stat-total-distributed").innerText = totalDistributed;
  document.getElementById("stat-total-subsidized").innerText = `Rs. ${totalSubsidized.toLocaleString('en-IN', { minimumFractionDigits: 2 })}`;

  // Populate Transaction History Table
  const tbody = document.getElementById("analytics-tbody");
  if (!tbody) return;

  if (store.distributions.length === 0) {
    tbody.innerHTML = `<tr><td colspan="9" style="text-align: center; padding: 12px; color: #64748B;">No distribution transactions recorded yet.</td></tr>`;
    return;
  }

  tbody.innerHTML = store.distributions.map(d => `
    <tr>
      <td><strong>${d.txnId}</strong></td>
      <td>${d.timestamp}</td>
      <td>${d.itemName}</td>
      <td>${d.recipient}</td>
      <td>${d.qty}</td>
      <td>${d.unit}</td>
      <td>Rs. ${d.gross.toFixed(2)}</td>
      <td><strong>${d.subsidyPercent.toFixed(0)}%</strong></td>
      <td style="color: #007832; font-weight: bold;">Rs. ${d.netPaid.toFixed(2)}</td>
    </tr>
  `).join("");
}

// =========================================================================
// 11. DESKTOP WINDOW & HOST CONTROLS
// =========================================================================

function setupDesktopHostControls() {
  const windowElem = document.getElementById("main-jframe");
  const btnToggleWinMode = document.getElementById("btn-toggle-window-mode");
  const winModeIcon = document.getElementById("window-mode-icon");
  const winModeLabel = document.getElementById("window-mode-label");
  const btnWinMaximize = document.getElementById("btn-win-maximize");
  const btnWinMinimize = document.getElementById("btn-win-minimize");
  const btnWinClose = document.getElementById("btn-win-close");

  function toggleMaximize() {
    const isMax = windowElem.classList.toggle("maximized");
    if (isMax) {
      winModeIcon.innerText = "🗗";
      winModeLabel.innerText = "Windowed Mode";
      btnWinMaximize.innerText = "🗗";
    } else {
      winModeIcon.innerText = "⛶";
      winModeLabel.innerText = "Maximize Window";
      btnWinMaximize.innerText = "□";
    }
  }

  btnToggleWinMode.addEventListener("click", toggleMaximize);
  btnWinMaximize.addEventListener("click", toggleMaximize);

  btnWinMinimize.addEventListener("click", () => {
    showJOptionPane({
      title: "Java Swing Desktop",
      message: "ChronoChef JFrame minimized to desktop taskbar.\nClick Maximize to restore.",
      type: "info",
      buttons: ["OK"]
    });
  });

  btnWinClose.addEventListener("click", () => {
    showJOptionPane({
      title: "Exit ChronoChef Application",
      message: "Are you sure you want to close ChronoChef?\nActive session data remains saved in local SQLite storage.",
      type: "question",
      buttons: ["Yes", "No"]
    });
  });

  // Reset Demo DB
  document.getElementById("btn-host-reset-db").addEventListener("click", () => {
    showJOptionPane({
      title: "Confirm Database Reset",
      message: "Reset SQLite database to the original 10 college demo items and initial transactions?",
      type: "warning",
      buttons: ["Yes", "No"],
      onSelect: (btn) => {
        if (btn === "Yes") {
          store.resetToDefault();
          renderInventoryTable();
          populateManagementItemSelector();
          populateDistributionDropdown();
          renderAnalyticsData();
          showJOptionPane({
            title: "Database Restored",
            message: "Database tables refreshed to default test state.",
            type: "info",
            buttons: ["OK"]
          });
        }
      }
    });
  });

  // Viva / Architecture JDialog
  const vivaOverlay = document.getElementById("viva-jdialog-overlay");
  document.getElementById("btn-open-viva-dialog").addEventListener("click", () => {
    vivaOverlay.classList.add("active");
  });

  document.getElementById("btn-close-viva-dialog").addEventListener("click", () => {
    vivaOverlay.classList.remove("active");
  });

  document.getElementById("btn-dismiss-viva-dialog").addEventListener("click", () => {
    vivaOverlay.classList.remove("active");
  });
}

// =========================================================================
// 12. INITIALIZATION
// =========================================================================

document.addEventListener("DOMContentLoaded", () => {
  // Navigation buttons
  document.querySelectorAll(".swing-nav-btn").forEach(btn => {
    btn.addEventListener("click", () => switchCard(btn.dataset.card));
  });

  // Setup panels
  setupInputPanel();
  setupInventoryPanel();
  setupManagementPanel();
  setupDistributionPanel();
  document.getElementById("btn-analytics-refresh").addEventListener("click", renderAnalyticsData);

  // Setup desktop controls
  setupDesktopHostControls();

  // Initial render
  renderInventoryTable();
  populateManagementItemSelector();
  populateDistributionDropdown();
  renderAnalyticsData();
});
