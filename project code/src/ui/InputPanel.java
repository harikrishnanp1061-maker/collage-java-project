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
import java.awt.event.ItemEvent;
import java.awt.event.ItemListener;
import java.text.SimpleDateFormat;
import java.util.Date;

/**
 * InputPanel - Module A: Data Input Interface
 * 
 * Allows users to register new food inventory items.
 * Validates inputs, handles exceptions, and stores records via DAO.
 * 
 * College Syllabus Mapping:
 * - Module 4: Swing controls (JPanel, JLabel, JTextField, JComboBox, JButton)
 * - Module 4: Swing Layout Managers (BorderLayout, GridLayout, FlowLayout)
 * - Module 4: Delegation Event Model (ActionListener, ItemListener)
 * - Module 3: Exception Handling (try-catch for NumberFormatException & Date validation)
 */
public class InputPanel extends JPanel implements ActionListener, ItemListener {

    private JTextField txtId;
    private JTextField txtName;
    private JComboBox<String> cbCategory;
    private JComboBox<String> cbItemType;
    private JTextField txtQuantity;
    private JComboBox<String> cbUnit;
    private JTextField txtReceivedDate;
    private JTextField txtExpiryDate;
    private JTextField txtBasePrice;
    private JLabel lblExtra;
    private JTextField txtExtra;

    private JButton btnSave;
    private JButton btnClear;

    private FoodBankDAO dao;
    private MainFrame mainFrame;

    public InputPanel(MainFrame mainFrame) {
        this.mainFrame = mainFrame;
        this.dao = new FoodBankDAO();

        setLayout(new BorderLayout(15, 15));
        setBorder(BorderFactory.createEmptyBorder(20, 30, 20, 30));

        // Header Title
        JLabel lblTitle = new JLabel("Data Input: Register Incoming Food Item", JLabel.LEFT);
        lblTitle.setFont(new Font("Arial", Font.BOLD, 18));
        lblTitle.setForeground(new Color(30, 60, 100));
        add(lblTitle, BorderLayout.NORTH);

        // Form Container Panel
        JPanel formPanel = new JPanel(new GridLayout(10, 2, 10, 12));
        formPanel.setBorder(BorderFactory.createCompoundBorder(
                BorderFactory.createLineBorder(new Color(200, 210, 225), 1),
                BorderFactory.createEmptyBorder(15, 20, 15, 20)
        ));

        // Initialize Form Fields
        txtId = new JTextField();
        txtName = new JTextField();

        String[] categories = {"Dairy", "Produce", "Bakery", "Canned Goods", "Grains", "Beverages", "Other"};
        cbCategory = new JComboBox<String>(categories);

        String[] types = {"PERISHABLE", "PACKAGED"};
        cbItemType = new JComboBox<String>(types);
        cbItemType.addItemListener(this);

        txtQuantity = new JTextField();

        String[] units = {"kg", "Liters", "Packets", "Cans", "Boxes", "Tubs", "Loaves"};
        cbUnit = new JComboBox<String>(units);

        SimpleDateFormat sdf = new SimpleDateFormat("yyyy-MM-dd");
        txtReceivedDate = new JTextField(sdf.format(new Date()));
        txtExpiryDate = new JTextField(); // Empty prompt
        txtBasePrice = new JTextField("30.0");

        lblExtra = new JLabel("Storage Temperature (°C):");
        txtExtra = new JTextField("4.0");

        // Add fields to grid
        formPanel.add(new JLabel("Item ID (e.g., FD-1011):"));
        formPanel.add(txtId);

        formPanel.add(new JLabel("Food Item Name:"));
        formPanel.add(txtName);

        formPanel.add(new JLabel("Food Category:"));
        formPanel.add(cbCategory);

        formPanel.add(new JLabel("Item Type:"));
        formPanel.add(cbItemType);

        formPanel.add(new JLabel("Quantity:"));
        formPanel.add(txtQuantity);

        formPanel.add(new JLabel("Unit of Measurement:"));
        formPanel.add(cbUnit);

        formPanel.add(new JLabel("Date Received (YYYY-MM-DD):"));
        formPanel.add(txtReceivedDate);

        formPanel.add(new JLabel("Expiry Date (YYYY-MM-DD):"));
        formPanel.add(txtExpiryDate);

        formPanel.add(new JLabel("Nominal Base Price (Rs.):"));
        formPanel.add(txtBasePrice);

        formPanel.add(lblExtra);
        formPanel.add(txtExtra);

        add(formPanel, BorderLayout.CENTER);

        // Button Panel
        JPanel buttonPanel = new JPanel(new FlowLayout(FlowLayout.RIGHT, 15, 10));
        btnSave = new JButton("Save Food Item");
        btnSave.setFont(new Font("Arial", Font.BOLD, 13));
        btnSave.setOpaque(true);
        btnSave.setBackground(new Color(30, 110, 50));
        btnSave.setForeground(Color.WHITE);
        btnSave.setPreferredSize(new Dimension(160, 35));
        btnSave.addActionListener(this);

        btnClear = new JButton("Clear Form");
        btnClear.setPreferredSize(new Dimension(120, 35));
        btnClear.setFont(new Font("Arial", Font.PLAIN, 12));
        btnClear.setForeground(new Color(30, 30, 30));
        btnClear.addActionListener(this);

        buttonPanel.add(btnClear);
        buttonPanel.add(btnSave);
        add(buttonPanel, BorderLayout.SOUTH);
    }

    /**
     * ItemListener for switching extra field between Perishable and Packaged
     */
    @Override
    public void itemStateChanged(ItemEvent e) {
        if (e.getStateChange() == ItemEvent.SELECTED) {
            String selectedType = (String) cbItemType.getSelectedItem();
            if ("PERISHABLE".equalsIgnoreCase(selectedType)) {
                lblExtra.setText("Storage Temperature (°C):");
                txtExtra.setText("4.0");
            } else {
                lblExtra.setText("Batch / Lot Number:");
                txtExtra.setText("BATCH-2026-A");
            }
        }
    }

    /**
     * ActionListener handling Save and Clear button events
     */
    @Override
    public void actionPerformed(ActionEvent e) {
        if (e.getSource() == btnSave) {
            saveFoodItem();
        } else if (e.getSource() == btnClear) {
            clearForm();
        }
    }

    private void saveFoodItem() {
        // Step 1: Validate essential text fields
        String id = txtId.getText().trim();
        String name = txtName.getText().trim();
        String category = (String) cbCategory.getSelectedItem();
        String type = (String) cbItemType.getSelectedItem();
        String unit = (String) cbUnit.getSelectedItem();
        String recDate = txtReceivedDate.getText().trim();
        String expDate = txtExpiryDate.getText().trim();

        if (id.isEmpty() || name.isEmpty() || expDate.isEmpty() || recDate.isEmpty()) {
            JOptionPane.showMessageDialog(this, 
                "Please fill in all essential fields (ID, Name, Dates).", 
                "Input Validation Error", 
                JOptionPane.WARNING_MESSAGE);
            return;
        }

        // Step 2: Validate Numerical Inputs with try-catch
        double quantity = 0.0;
        double price = 0.0;
        try {
            quantity = Double.parseDouble(txtQuantity.getText().trim());
            if (quantity <= 0) {
                JOptionPane.showMessageDialog(this, "Quantity must be greater than zero.", "Validation Error", JOptionPane.ERROR_MESSAGE);
                return;
            }
        } catch (NumberFormatException nfe) {
            JOptionPane.showMessageDialog(this, "Invalid quantity entered. Please enter a valid number.", "Number Format Error", JOptionPane.ERROR_MESSAGE);
            return;
        }

        try {
            price = Double.parseDouble(txtBasePrice.getText().trim());
            if (price < 0) {
                JOptionPane.showMessageDialog(this, "Base price cannot be negative.", "Validation Error", JOptionPane.ERROR_MESSAGE);
                return;
            }
        } catch (NumberFormatException nfe) {
            JOptionPane.showMessageDialog(this, "Invalid base price entered.", "Number Format Error", JOptionPane.ERROR_MESSAGE);
            return;
        }

        // Step 3: Validate Date Format (YYYY-MM-DD)
        if (!expDate.matches("\\d{4}-\\d{2}-\\d{2}") || !recDate.matches("\\d{4}-\\d{2}-\\d{2}")) {
            JOptionPane.showMessageDialog(this, "Dates must strictly follow YYYY-MM-DD format.", "Date Format Error", JOptionPane.ERROR_MESSAGE);
            return;
        }

        // Step 4: Construct Polymorphic Entity based on Selected Type
        FoodItem newItem = null;
        if ("PERISHABLE".equalsIgnoreCase(type)) {
            double temp = 4.0;
            try {
                temp = Double.parseDouble(txtExtra.getText().trim());
            } catch (NumberFormatException nfe) {
                temp = 4.0;
            }
            newItem = new PerishableItem(id, name, category, quantity, unit, recDate, expDate, price, temp);
        } else {
            String batch = txtExtra.getText().trim();
            if (batch.isEmpty()) batch = "BATCH-GEN";
            newItem = new PackagedItem(id, name, category, quantity, unit, recDate, expDate, price, batch);
        }

        // Step 5: Save to Database via DAO
        try {
            boolean success = dao.addItem(newItem);
            if (success) {
                JOptionPane.showMessageDialog(this, 
                    "Food Item [" + name + "] registered successfully!", 
                    "Success", 
                    JOptionPane.INFORMATION_MESSAGE);
                clearForm();
                // Refresh shared views
                mainFrame.refreshAllViews();
            } else {
                JOptionPane.showMessageDialog(this, "Failed to save item. Check if Item ID is already in use.", "Database Error", JOptionPane.ERROR_MESSAGE);
            }
        } catch (Exception ex) {
            JOptionPane.showMessageDialog(this, "Error inserting item: " + ex.getMessage(), "Database Error", JOptionPane.ERROR_MESSAGE);
        }
    }

    private void clearForm() {
        txtId.setText("");
        txtName.setText("");
        txtQuantity.setText("");
        txtExpiryDate.setText("");
        txtBasePrice.setText("30.0");
        if ("PERISHABLE".equalsIgnoreCase((String) cbItemType.getSelectedItem())) {
            txtExtra.setText("4.0");
        } else {
            txtExtra.setText("BATCH-2026-A");
        }
    }
}
