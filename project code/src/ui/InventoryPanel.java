package ui;

import database.FoodBankDAO;
import model.FoodItem;
import service.PriorityPricingService;

import javax.swing.BorderFactory;
import javax.swing.JButton;
import javax.swing.JComboBox;
import javax.swing.JLabel;
import javax.swing.JOptionPane;
import javax.swing.JPanel;
import javax.swing.JScrollPane;
import javax.swing.JTable;
import javax.swing.JTextField;
import javax.swing.table.DefaultTableCellRenderer;
import javax.swing.table.DefaultTableModel;
import java.awt.BorderLayout;
import java.awt.Color;
import java.awt.Component;
import java.awt.Dimension;
import java.awt.FlowLayout;
import java.awt.Font;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.util.Vector;

/**
 * InventoryPanel - Module B: Inventory Reading & Expiry Tracker Interface
 * 
 * Displays all active food stock, calculates days remaining, evaluates PDI score,
 * classifies priorities, and sorts items by urgency using Bubble Sort.
 * 
 * College Syllabus Mapping:
 * - Module 4: Swing Components (JTable, JScrollPane, JPanel, JComboBox)
 * - Module 4: Event Handling (ActionListener on Search and Filter controls)
 * - Module 1: Vector class as backing data store
 */
public class InventoryPanel extends JPanel implements ActionListener {

    private JTextField txtSearch;
    private JComboBox<String> cbFilter;
    private JButton btnSearch;
    private JButton btnRefresh;
    private JButton btnSortPDI;

    private JTable inventoryTable;
    private DefaultTableModel tableModel;
    private JLabel lblStatusCount;

    private FoodBankDAO dao;
    private MainFrame mainFrame;

    public InventoryPanel(MainFrame mainFrame) {
        this.mainFrame = mainFrame;
        this.dao = new FoodBankDAO();

        setLayout(new BorderLayout(10, 10));
        setBorder(BorderFactory.createEmptyBorder(15, 20, 15, 20));

        // Top Control Panel: Search & Filters
        JPanel topPanel = new JPanel(new BorderLayout(10, 10));

        JLabel lblTitle = new JLabel("Inventory Reading & Expiry Tracker (PDI)", JLabel.LEFT);
        lblTitle.setFont(new Font("Arial", Font.BOLD, 18));
        lblTitle.setForeground(new Color(30, 60, 100));
        topPanel.add(lblTitle, BorderLayout.NORTH);

        JPanel searchBarPanel = new JPanel(new FlowLayout(FlowLayout.LEFT, 10, 5));
        searchBarPanel.add(new JLabel("Search Item:"));
        txtSearch = new JTextField(15);
        searchBarPanel.add(txtSearch);

        btnSearch = new JButton("Search");
        btnSearch.addActionListener(this);
        searchBarPanel.add(btnSearch);

        searchBarPanel.add(new JLabel("Filter View:"));
        String[] filters = {
            "All Items", 
            "Safe to Distribute", 
            "Urgent Only (0-5 days)", 
            "High Priority (6-15 days)", 
            "Expired Goods (Quarantined)"
        };
        cbFilter = new JComboBox<String>(filters);
        cbFilter.addActionListener(this);
        searchBarPanel.add(cbFilter);

        btnSortPDI = new JButton("Sort by Urgency (PDI)");
        btnSortPDI.setBackground(new Color(230, 240, 255));
        btnSortPDI.addActionListener(this);
        searchBarPanel.add(btnSortPDI);

        btnRefresh = new JButton("Refresh");
        btnRefresh.addActionListener(this);
        searchBarPanel.add(btnRefresh);

        topPanel.add(searchBarPanel, BorderLayout.CENTER);
        add(topPanel, BorderLayout.NORTH);

        // Center Table Setup
        String[] columns = {
            "Item ID", "Name", "Category", "Type", "Stock", "Unit", 
            "Expiry Date", "Days Left", "PDI Score", "Priority", "Status", "Instructions"
        };

        tableModel = new DefaultTableModel(columns, 0) {
            @Override
            public boolean isCellEditable(int row, int column) {
                return false; // read-only table
            }
        };

        inventoryTable = new JTable(tableModel);
        inventoryTable.setRowHeight(26);
        inventoryTable.getTableHeader().setFont(new Font("Arial", Font.BOLD, 12));
        inventoryTable.getTableHeader().setBackground(new Color(235, 240, 248));

        // Custom Cell Renderer to visually highlight priority with high contrast
        inventoryTable.setDefaultRenderer(Object.class, new DefaultTableCellRenderer() {
            @Override
            public Component getTableCellRendererComponent(JTable table, Object value, 
                    boolean isSelected, boolean hasFocus, int row, int column) {
                Component c = super.getTableCellRendererComponent(table, value, isSelected, hasFocus, row, column);
                String priority = (String) table.getValueAt(row, 9);

                if (isSelected) {
                    c.setBackground(table.getSelectionBackground());
                    c.setForeground(table.getSelectionForeground());
                } else {
                    if ("EXPIRED".equalsIgnoreCase(priority)) {
                        c.setBackground(new Color(255, 230, 230)); // Soft red background
                        c.setForeground(new Color(160, 0, 0));     // Deep red text (high contrast)
                    } else if ("URGENT".equalsIgnoreCase(priority)) {
                        c.setBackground(new Color(255, 240, 220)); // Soft orange background
                        c.setForeground(new Color(160, 50, 0));    // Deep orange-brown text
                    } else if ("HIGH".equalsIgnoreCase(priority)) {
                        c.setBackground(new Color(255, 250, 220)); // Soft yellow background
                        c.setForeground(new Color(120, 80, 0));     // Deep amber text
                    } else {
                        c.setBackground(Color.WHITE);
                        c.setForeground(new Color(30, 30, 30));     // Crisp dark charcoal text
                    }
                }
                return c;
            }
        });

        JScrollPane scrollPane = new JScrollPane(inventoryTable);
        add(scrollPane, BorderLayout.CENTER);

        // Bottom Summary Bar
        JPanel bottomBar = new JPanel(new FlowLayout(FlowLayout.LEFT, 15, 8));
        lblStatusCount = new JLabel("Total Items: 0 | Total Quantity: 0");
        lblStatusCount.setFont(new Font("Arial", Font.BOLD, 13));
        lblStatusCount.setForeground(new Color(30, 45, 65));
        bottomBar.add(lblStatusCount);
        add(bottomBar, BorderLayout.SOUTH);

        // Load initial data
        loadInventoryData();
    }

    /**
     * Load data from database into JTable, applying filters and PDI calculations
     */
    public void loadInventoryData() {
        try {
            Vector<FoodItem> items = dao.getAllItems();
            displayItemsInTable(items);
        } catch (Exception e) {
            JOptionPane.showMessageDialog(this, "Error loading inventory: " + e.getMessage(), "Error", JOptionPane.ERROR_MESSAGE);
        }
    }

    private void displayItemsInTable(Vector<FoodItem> items) {
        tableModel.setRowCount(0);

        String selectedFilter = (String) cbFilter.getSelectedItem();
        double totalQty = 0;
        int displayedCount = 0;

        for (int i = 0; i < items.size(); i++) {
            FoodItem item = items.get(i);
            int daysLeft = PriorityPricingService.calculateDaysRemaining(item.getExpiryDate());
            int pdi = PriorityPricingService.calculatePDI(daysLeft);
            String priority = PriorityPricingService.getPriorityLevel(daysLeft);
            String status = PriorityPricingService.getStatusString(daysLeft);

            // Apply view filters
            boolean matchesFilter = true;
            if ("Safe to Distribute".equals(selectedFilter)) {
                matchesFilter = (daysLeft >= 0);
            } else if ("Urgent Only (0-5 days)".equals(selectedFilter)) {
                matchesFilter = (daysLeft >= 0 && daysLeft <= 5);
            } else if ("High Priority (6-15 days)".equals(selectedFilter)) {
                matchesFilter = (daysLeft >= 6 && daysLeft <= 15);
            } else if ("Expired Goods (Quarantined)".equals(selectedFilter)) {
                matchesFilter = (daysLeft < 0);
            }

            if (!matchesFilter) continue;

            // Clean, user-friendly Days Left description (replaces raw negative numbers)
            String daysLeftDisplay;
            if (daysLeft < 0) {
                daysLeftDisplay = "Expired (" + Math.abs(daysLeft) + "d ago)";
            } else if (daysLeft == 0) {
                daysLeftDisplay = "Expires Today";
            } else if (daysLeft == 1) {
                daysLeftDisplay = "1 day left";
            } else {
                daysLeftDisplay = daysLeft + " days";
            }

            // Row vector with all values as Strings for uniform high-contrast rendering
            Vector<Object> row = new Vector<Object>();
            row.add(item.getItemId());
            row.add(item.getName());
            row.add(item.getCategory());
            row.add(item.getItemType());
            row.add(String.format("%.1f", item.getQuantity()));
            row.add(item.getUnit());
            row.add(item.getExpiryDate());
            row.add(daysLeftDisplay);
            row.add(String.valueOf(pdi));
            row.add(priority);
            row.add(status);
            // Polymorphic call: invokes overridden getStorageInstructions()
            row.add(item.getStorageInstructions());

            tableModel.addRow(row);
            totalQty += item.getQuantity();
            displayedCount++;
        }

        lblStatusCount.setText("Showing " + displayedCount + " item records | Total Volume: " + 
                               String.format("%.1f", totalQty) + " units in view");
    }

    @Override
    public void actionPerformed(ActionEvent e) {
        if (e.getSource() == btnSearch) {
            performSearch();
        } else if (e.getSource() == btnRefresh || e.getSource() == cbFilter) {
            loadInventoryData();
        } else if (e.getSource() == btnSortPDI) {
            sortAndDisplay();
        }
    }

    private void performSearch() {
        String keyword = txtSearch.getText().trim();
        if (keyword.isEmpty()) {
            loadInventoryData();
            return;
        }
        try {
            Vector<FoodItem> results = dao.searchItems(keyword);
            displayItemsInTable(results);
        } catch (Exception ex) {
            JOptionPane.showMessageDialog(this, "Search error: " + ex.getMessage(), "Error", JOptionPane.ERROR_MESSAGE);
        }
    }

    private void sortAndDisplay() {
        try {
            Vector<FoodItem> items = dao.getAllItems();
            // Sort using classic Bubble Sort
            PriorityPricingService.sortByUrgencyDescending(items);
            displayItemsInTable(items);
            JOptionPane.showMessageDialog(this, 
                "Inventory sorted by Priority Distribution Index (PDI) in descending order.\nMost urgent items are displayed first.", 
                "Priority Sorted", 
                JOptionPane.INFORMATION_MESSAGE);
        } catch (Exception ex) {
            JOptionPane.showMessageDialog(this, "Sort error: " + ex.getMessage(), "Error", JOptionPane.ERROR_MESSAGE);
        }
    }
}
