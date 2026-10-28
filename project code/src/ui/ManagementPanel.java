package ui;

import database.FoodBankDAO;
import model.FoodItem;
import model.PackagedItem;
import model.PerishableItem;

import javax.swing.BorderFactory;
import javax.swing.JButton;
import javax.swing.JComboBox;
import javax.swing.JLabel;
import javax.swing.JOptionPane;
import javax.swing.JPanel;
import javax.swing.JTextField;
import java.awt.BorderLayout;
import java.awt.Color;
import java.awt.Dimension;
import java.awt.FlowLayout;
import java.awt.Font;
import java.awt.GridLayout;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.util.Vector;

/**
 * ManagementPanel - Module C: Inventory Management Interface
 * 
 * Allows modifying existing records, restocking incoming quantity,
 * and writing off / deleting damaged stock.
 * 
 * College Syllabus Mapping:
 * - Module 4: Swing controls and layout managers
 * - Module 4: JDBC CRUD operations (Update, Delete)
 * - Module 3: Exception handling
 */
public class ManagementPanel extends JPanel implements ActionListener {

    private JComboBox<String> cbItemSelector;
    private JTextField txtId;
    private JTextField txtName;
    private JComboBox<String> cbCategory;
    private JTextField txtCurrentQty;
    private JTextField txtUnit;
    private JTextField txtExpiryDate;
    private JTextField txtBasePrice;

    private JTextField txtRestockQty;
    private JButton btnRestock;
    private JButton btnUpdate;
    private JButton btnDelete;

    private FoodBankDAO dao;
    private MainFrame mainFrame;
    private Vector<FoodItem> currentItemList;

    public ManagementPanel(MainFrame mainFrame) {
        this.mainFrame = mainFrame;
        this.dao = new FoodBankDAO();

        setLayout(new BorderLayout(15, 15));
        setBorder(BorderFactory.createEmptyBorder(20, 30, 20, 30));

        // Title & Selector Panel
        JPanel northPanel = new JPanel(new BorderLayout(10, 10));

        JLabel lblTitle = new JLabel("Inventory Management: Edit Details & Stock Inflow", JLabel.LEFT);
        lblTitle.setFont(new Font("Arial", Font.BOLD, 18));
        lblTitle.setForeground(new Color(30, 60, 100));
        northPanel.add(lblTitle, BorderLayout.NORTH);

        JPanel selectPanel = new JPanel(new FlowLayout(FlowLayout.LEFT, 10, 5));
        selectPanel.add(new JLabel("Select Existing Food Item:"));
        cbItemSelector = new JComboBox<String>();
        cbItemSelector.setPreferredSize(new Dimension(350, 28));
        cbItemSelector.addActionListener(this);
        selectPanel.add(cbItemSelector);

        JButton btnReloadList = new JButton("Refresh List");
        btnReloadList.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                populateItemSelector();
            }
        });
        selectPanel.add(btnReloadList);

        northPanel.add(selectPanel, BorderLayout.CENTER);
        add(northPanel, BorderLayout.NORTH);

        // Edit Form Panel
        JPanel formPanel = new JPanel(new GridLayout(8, 2, 10, 10));
        formPanel.setBorder(BorderFactory.createCompoundBorder(
                BorderFactory.createLineBorder(new Color(200, 210, 225), 1),
                BorderFactory.createEmptyBorder(15, 20, 15, 20)
        ));

        txtId = new JTextField();
        txtId.setEditable(false); // ID is immutable primary key
        txtId.setBackground(new Color(245, 245, 245));

        txtName = new JTextField();
        String[] categories = {"Dairy", "Produce", "Bakery", "Canned Goods", "Grains", "Beverages", "Other"};
        cbCategory = new JComboBox<String>(categories);

        txtCurrentQty = new JTextField();
        txtCurrentQty.setEditable(false);
        txtCurrentQty.setBackground(new Color(245, 245, 245));

        txtUnit = new JTextField();
        txtExpiryDate = new JTextField();
        txtBasePrice = new JTextField();

        formPanel.add(new JLabel("Item ID (Primary Key):"));
        formPanel.add(txtId);

        formPanel.add(new JLabel("Food Item Name:"));
        formPanel.add(txtName);

        formPanel.add(new JLabel("Category:"));
        formPanel.add(cbCategory);

        formPanel.add(new JLabel("Current Available Stock:"));
        formPanel.add(txtCurrentQty);

        formPanel.add(new JLabel("Unit of Measurement:"));
        formPanel.add(txtUnit);

        formPanel.add(new JLabel("Expiry Date (YYYY-MM-DD):"));
        formPanel.add(txtExpiryDate);

        formPanel.add(new JLabel("Nominal Base Price (Rs.):"));
        formPanel.add(txtBasePrice);

        add(formPanel, BorderLayout.CENTER);

        // Bottom Actions Panel (Restocking + Updating + Removing)
        JPanel bottomPanel = new JPanel(new BorderLayout(10, 10));

        // Restock Section
        JPanel restockBox = new JPanel(new FlowLayout(FlowLayout.LEFT, 10, 8));
        restockBox.setBorder(BorderFactory.createTitledBorder("Inflow / Restock Additional Quantity"));

        restockBox.add(new JLabel("Add Incoming Quantity:"));
        txtRestockQty = new JTextField(8);
        restockBox.add(txtRestockQty);

        btnRestock = new JButton("Restock Item");
        btnRestock.setOpaque(true);
        btnRestock.setBackground(new Color(30, 110, 50));
        btnRestock.setForeground(Color.WHITE);
        btnRestock.setFont(new Font("Arial", Font.BOLD, 12));
        btnRestock.addActionListener(this);
        restockBox.add(btnRestock);

        bottomPanel.add(restockBox, BorderLayout.NORTH);

        // Update and Delete Actions
        JPanel actionButtons = new JPanel(new FlowLayout(FlowLayout.RIGHT, 15, 10));

        btnUpdate = new JButton("Update Item Details");
        btnUpdate.setOpaque(true);
        btnUpdate.setBackground(new Color(35, 75, 125));
        btnUpdate.setForeground(Color.WHITE);
        btnUpdate.setFont(new Font("Arial", Font.BOLD, 12));
        btnUpdate.setPreferredSize(new Dimension(160, 32));
        btnUpdate.addActionListener(this);
        actionButtons.add(btnUpdate);

        btnDelete = new JButton("Write-Off / Delete Item");
        btnDelete.setOpaque(true);
        btnDelete.setBackground(new Color(175, 40, 40));
        btnDelete.setForeground(Color.WHITE);
        btnDelete.setFont(new Font("Arial", Font.BOLD, 12));
        btnDelete.setPreferredSize(new Dimension(170, 32));
        btnDelete.addActionListener(this);
        actionButtons.add(btnDelete);

        bottomPanel.add(actionButtons, BorderLayout.SOUTH);
        add(bottomPanel, BorderLayout.SOUTH);

        // Populate items dropdown
        populateItemSelector();
    }

    /**
     * Populate items into selector dropdown
     */
    public void populateItemSelector() {
        try {
            cbItemSelector.removeActionListener(this);
            cbItemSelector.removeAllItems();

            currentItemList = dao.getAllItems();
            for (int i = 0; i < currentItemList.size(); i++) {
                FoodItem item = currentItemList.get(i);
                cbItemSelector.addItem(item.getItemId() + " - " + item.getName() + " (" + item.getQuantity() + " " + item.getUnit() + ")");
            }

            cbItemSelector.addActionListener(this);

            if (currentItemList.size() > 0) {
                loadSelectedItemFields(0);
            } else {
                clearFields();
            }
        } catch (Exception e) {
            System.out.println("[ManagementPanel] Error populating selector: " + e.getMessage());
        }
    }

    private void loadSelectedItemFields(int index) {
        if (currentItemList != null && index >= 0 && index < currentItemList.size()) {
            FoodItem item = currentItemList.get(index);
            txtId.setText(item.getItemId());
            txtName.setText(item.getName());
            cbCategory.setSelectedItem(item.getCategory());
            txtCurrentQty.setText(String.valueOf(item.getQuantity()));
            txtUnit.setText(item.getUnit());
            txtExpiryDate.setText(item.getExpiryDate());
            txtBasePrice.setText(String.valueOf(item.getBasePrice()));
        }
    }

    private void clearFields() {
        txtId.setText("");
        txtName.setText("");
        txtCurrentQty.setText("");
        txtUnit.setText("");
        txtExpiryDate.setText("");
        txtBasePrice.setText("");
    }

    @Override
    public void actionPerformed(ActionEvent e) {
        if (e.getSource() == cbItemSelector) {
            int idx = cbItemSelector.getSelectedIndex();
            if (idx >= 0) {
                loadSelectedItemFields(idx);
            }
        } else if (e.getSource() == btnRestock) {
            performRestock();
        } else if (e.getSource() == btnUpdate) {
            performUpdate();
        } else if (e.getSource() == btnDelete) {
            performDelete();
        }
    }

    private void performRestock() {
        String id = txtId.getText().trim();
        if (id.isEmpty()) {
            JOptionPane.showMessageDialog(this, "Please select an item first.", "Warning", JOptionPane.WARNING_MESSAGE);
            return;
        }

        try {
            double addQty = Double.parseDouble(txtRestockQty.getText().trim());
            if (addQty <= 0) {
                JOptionPane.showMessageDialog(this, "Restock quantity must be positive.", "Validation Error", JOptionPane.ERROR_MESSAGE);
                return;
            }

            boolean ok = dao.restockItem(id, addQty);
            if (ok) {
                JOptionPane.showMessageDialog(this, "Successfully restocked " + addQty + " units!", "Success", JOptionPane.INFORMATION_MESSAGE);
                txtRestockQty.setText("");
                mainFrame.refreshAllViews();
            }
        } catch (NumberFormatException nfe) {
            JOptionPane.showMessageDialog(this, "Please enter a valid numeric quantity.", "Error", JOptionPane.ERROR_MESSAGE);
        } catch (Exception ex) {
            JOptionPane.showMessageDialog(this, "Restock failed: " + ex.getMessage(), "Database Error", JOptionPane.ERROR_MESSAGE);
        }
    }

    private void performUpdate() {
        String id = txtId.getText().trim();
        if (id.isEmpty()) {
            JOptionPane.showMessageDialog(this, "Please select an item first.", "Warning", JOptionPane.WARNING_MESSAGE);
            return;
        }

        try {
            String name = txtName.getText().trim();
            String category = (String) cbCategory.getSelectedItem();
            String unit = txtUnit.getText().trim();
            String expDate = txtExpiryDate.getText().trim();
            double price = Double.parseDouble(txtBasePrice.getText().trim());

            if (name.isEmpty() || expDate.isEmpty()) {
                JOptionPane.showMessageDialog(this, "Name and Expiry Date cannot be empty.", "Error", JOptionPane.ERROR_MESSAGE);
                return;
            }

            // Find current item to preserve its type
            FoodItem current = dao.getItemById(id);
            if (current != null) {
                current.setName(name);
                current.setCategory(category);
                current.setUnit(unit);
                current.setExpiryDate(expDate);
                current.setBasePrice(price);

                boolean ok = dao.updateItem(current);
                if (ok) {
                    JOptionPane.showMessageDialog(this, "Item details updated successfully!", "Success", JOptionPane.INFORMATION_MESSAGE);
                    mainFrame.refreshAllViews();
                }
            }
        } catch (NumberFormatException nfe) {
            JOptionPane.showMessageDialog(this, "Invalid number entered for price.", "Error", JOptionPane.ERROR_MESSAGE);
        } catch (Exception ex) {
            JOptionPane.showMessageDialog(this, "Update failed: " + ex.getMessage(), "Database Error", JOptionPane.ERROR_MESSAGE);
        }
    }

    private void performDelete() {
        String id = txtId.getText().trim();
        if (id.isEmpty()) {
            JOptionPane.showMessageDialog(this, "Please select an item to write off.", "Warning", JOptionPane.WARNING_MESSAGE);
            return;
        }

        int choice = JOptionPane.showConfirmDialog(this, 
                "Are you sure you want to write-off / delete item [" + id + " - " + txtName.getText() + "]?", 
                "Confirm Write-Off", 
                JOptionPane.YES_NO_OPTION);

        if (choice == JOptionPane.YES_OPTION) {
            try {
                boolean ok = dao.deleteItem(id);
                if (ok) {
                    JOptionPane.showMessageDialog(this, "Item removed from inventory successfully.", "Success", JOptionPane.INFORMATION_MESSAGE);
                    mainFrame.refreshAllViews();
                }
            } catch (Exception ex) {
                JOptionPane.showMessageDialog(this, "Delete failed: " + ex.getMessage(), "Database Error", JOptionPane.ERROR_MESSAGE);
            }
        }
    }
}
