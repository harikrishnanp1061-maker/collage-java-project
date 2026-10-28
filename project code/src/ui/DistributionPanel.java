package ui;

import database.FoodBankDAO;
import exception.ExpiredItemDistributionException;
import exception.InvalidQuantityException;
import model.DistributionRecord;
import model.FoodItem;
import service.PriorityPricingService;

import javax.swing.BorderFactory;
import javax.swing.JButton;
import javax.swing.JComboBox;
import javax.swing.JLabel;
import javax.swing.JOptionPane;
import javax.swing.JPanel;
import javax.swing.JScrollPane;
import javax.swing.JTextArea;
import javax.swing.JTextField;
import java.awt.BorderLayout;
import java.awt.Color;
import java.awt.Dimension;
import java.awt.FlowLayout;
import java.awt.Font;
import java.awt.GridLayout;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.Vector;

/**
 * DistributionPanel - Module D: Distribution & Food Bank Subsidy Interface
 * 
 * Records food distribution transactions, enforces safety rules by blocking expired goods,
 * applies dynamic subsidies, updates stock, and generates itemized distribution receipts.
 * 
 * College Syllabus Mapping:
 * - Module 3: Exception Handling (Custom exceptions: InvalidQuantityException, ExpiredItemDistributionException)
 * - Module 4: Swing controls (JTextArea for receipt generation, ComboBox, TextFields)
 * - Module 4: JDBC database updates
 */
public class DistributionPanel extends JPanel implements ActionListener {

    private JComboBox<String> cbItemSelect;
    private JTextField txtRecipient;
    private JTextField txtDistributeQty;
    private JLabel lblItemDetails;
    private JLabel lblSubsidyInfo;

    private JButton btnPreviewReceipt;
    private JButton btnConfirmDistribute;
    private JButton btnClear;

    private JTextArea txtReceiptArea;

    private FoodBankDAO dao;
    private MainFrame mainFrame;
    private Vector<FoodItem> availableItems;

    public DistributionPanel(MainFrame mainFrame) {
        this.mainFrame = mainFrame;
        this.dao = new FoodBankDAO();

        setLayout(new BorderLayout(15, 15));
        setBorder(BorderFactory.createEmptyBorder(20, 25, 20, 25));

        // Header Title
        JLabel lblTitle = new JLabel("Distribution & Dynamic Subsidy Billing Interface", JLabel.LEFT);
        lblTitle.setFont(new Font("Arial", Font.BOLD, 18));
        lblTitle.setForeground(new Color(30, 60, 100));
        add(lblTitle, BorderLayout.NORTH);

        // Center split: Left form + Right receipt
        JPanel centerContainer = new JPanel(new GridLayout(1, 2, 20, 10));

        // Left Form Panel
        JPanel leftPanel = new JPanel(new BorderLayout(10, 10));
        leftPanel.setBorder(BorderFactory.createTitledBorder("Distribution Transaction Details"));

        JPanel inputFields = new JPanel(new GridLayout(6, 2, 10, 12));
        inputFields.setBorder(BorderFactory.createEmptyBorder(10, 10, 10, 10));

        cbItemSelect = new JComboBox<String>();
        cbItemSelect.addActionListener(this);

        txtRecipient = new JTextField("Community Center / Shelter");
        txtDistributeQty = new JTextField();

        lblItemDetails = new JLabel("Stock: - | Expiry: -");
        lblItemDetails.setFont(new Font("Arial", Font.BOLD, 12));

        lblSubsidyInfo = new JLabel("Subsidy: - | Net Price: -");
        lblSubsidyInfo.setFont(new Font("Arial", Font.BOLD, 12));
        lblSubsidyInfo.setForeground(new Color(0, 120, 50));

        inputFields.add(new JLabel("Select Food Item:"));
        inputFields.add(cbItemSelect);

        inputFields.add(new JLabel("Selected Item Status:"));
        inputFields.add(lblItemDetails);

        inputFields.add(new JLabel("Recipient / Organization:"));
        inputFields.add(txtRecipient);

        inputFields.add(new JLabel("Quantity to Distribute:"));
        inputFields.add(txtDistributeQty);

        inputFields.add(new JLabel("Dynamic Subsidy Tier:"));
        inputFields.add(lblSubsidyInfo);

        leftPanel.add(inputFields, BorderLayout.CENTER);

        // Left Action Buttons
        JPanel actionBtnGrid = new JPanel(new FlowLayout(FlowLayout.CENTER, 10, 10));
        btnPreviewReceipt = new JButton("Generate Preview");
        btnPreviewReceipt.setFont(new Font("Arial", Font.PLAIN, 12));
        btnPreviewReceipt.setForeground(new Color(20, 20, 20));
        btnPreviewReceipt.addActionListener(this);

        btnConfirmDistribute = new JButton("Confirm Distribution");
        btnConfirmDistribute.setOpaque(true);
        btnConfirmDistribute.setBackground(new Color(30, 110, 50));
        btnConfirmDistribute.setForeground(Color.WHITE);
        btnConfirmDistribute.setFont(new Font("Arial", Font.BOLD, 12));
        btnConfirmDistribute.addActionListener(this);

        btnClear = new JButton("Reset");
        btnClear.setFont(new Font("Arial", Font.PLAIN, 12));
        btnClear.setForeground(new Color(20, 20, 20));
        btnClear.addActionListener(this);

        actionBtnGrid.add(btnPreviewReceipt);
        actionBtnGrid.add(btnConfirmDistribute);
        actionBtnGrid.add(btnClear);
        leftPanel.add(actionBtnGrid, BorderLayout.SOUTH);

        centerContainer.add(leftPanel);

        // Right Receipt Panel
        JPanel rightPanel = new JPanel(new BorderLayout(10, 10));
        rightPanel.setBorder(BorderFactory.createTitledBorder("Generated Distribution Receipt"));

        txtReceiptArea = new JTextArea();
        txtReceiptArea.setFont(new Font("Monospaced", Font.BOLD, 12));
        txtReceiptArea.setEditable(false);
        txtReceiptArea.setBackground(Color.WHITE);
        txtReceiptArea.setForeground(new Color(25, 25, 25)); // Deep dark charcoal text
        txtReceiptArea.setText("\n  Receipt preview will appear here upon entering distribution details.");

        JScrollPane receiptScroll = new JScrollPane(txtReceiptArea);
        rightPanel.add(receiptScroll, BorderLayout.CENTER);

        centerContainer.add(rightPanel);
        add(centerContainer, BorderLayout.CENTER);

        // Populate items
        populateItemSelect();
    }

    /**
     * Populate items dropdown
     */
    public void populateItemSelect() {
        try {
            cbItemSelect.removeActionListener(this);
            cbItemSelect.removeAllItems();

            availableItems = dao.getAllItems();
            for (int i = 0; i < availableItems.size(); i++) {
                FoodItem it = availableItems.get(i);
                int days = PriorityPricingService.calculateDaysRemaining(it.getExpiryDate());
                String tag = (days < 0) ? "[EXPIRED] " : (days <= 5 ? "[URGENT] " : "");
                cbItemSelect.addItem(tag + it.getItemId() + " - " + it.getName() + " (" + it.getQuantity() + " " + it.getUnit() + ")");
            }

            cbItemSelect.addActionListener(this);

            if (availableItems.size() > 0) {
                updateSelectionPreview(0);
            }
        } catch (Exception e) {
            System.out.println("[DistributionPanel] Error populating items: " + e.getMessage());
        }
    }

    private void updateSelectionPreview(int idx) {
        if (availableItems != null && idx >= 0 && idx < availableItems.size()) {
            FoodItem item = availableItems.get(idx);
            int days = PriorityPricingService.calculateDaysRemaining(item.getExpiryDate());

            lblItemDetails.setText("Stock: " + item.getQuantity() + " " + item.getUnit() + 
                                  " | Days Left: " + days);

            if (days < 0) {
                lblSubsidyInfo.setText("BLOCKED: Item is Expired");
                lblSubsidyInfo.setForeground(Color.RED);
            } else {
                try {
                    double subsidy = PriorityPricingService.calculateSubsidyPercentage(days);
                    double effPrice = PriorityPricingService.calculateEffectivePrice(item.getBasePrice(), days);
                    lblSubsidyInfo.setText(subsidy + "% Subsidy | Net: Rs. " + String.format("%.2f", effPrice) + "/" + item.getUnit());
                    lblSubsidyInfo.setForeground(new Color(0, 120, 50));
                } catch (ExpiredItemDistributionException ex) {
                    lblSubsidyInfo.setText("BLOCKED: Expired");
                    lblSubsidyInfo.setForeground(Color.RED);
                }
            }
        }
    }

    @Override
    public void actionPerformed(ActionEvent e) {
        if (e.getSource() == cbItemSelect) {
            int idx = cbItemSelect.getSelectedIndex();
            if (idx >= 0) {
                updateSelectionPreview(idx);
            }
        } else if (e.getSource() == btnPreviewReceipt) {
            generateReceiptPreview();
        } else if (e.getSource() == btnConfirmDistribute) {
            executeDistribution();
        } else if (e.getSource() == btnClear) {
            txtDistributeQty.setText("");
            txtReceiptArea.setText("");
        }
    }

    /**
     * Generate text receipt preview
     */
    private DistributionRecord validateAndPrepareRecord() throws InvalidQuantityException, ExpiredItemDistributionException {
        int idx = cbItemSelect.getSelectedIndex();
        if (idx < 0 || availableItems == null || idx >= availableItems.size()) {
            throw new InvalidQuantityException("No food item selected.");
        }

        FoodItem item = availableItems.get(idx);

        // REQUIREMENT 2: Expired items rejected BEFORE any subsidy or pricing calculation
        int daysLeft = PriorityPricingService.calculateDaysRemaining(item.getExpiryDate());
        if (daysLeft < 0) {
            throw new ExpiredItemDistributionException(
                "Food Safety Violation: Item [" + item.getName() + "] expired " + 
                Math.abs(daysLeft) + " days ago. Distribution and pricing calculations are strictly prohibited."
            );
        }

        String recipient = txtRecipient.getText().trim();
        if (recipient.isEmpty()) {
            recipient = "General Beneficiary";
        }

        double qty = 0;
        try {
            qty = Double.parseDouble(txtDistributeQty.getText().trim());
        } catch (NumberFormatException nfe) {
            throw new InvalidQuantityException("Please enter a valid numeric distribution quantity.");
        }

        if (qty <= 0) {
            throw new InvalidQuantityException("Distribution quantity must be greater than zero.");
        }

        if (qty > item.getQuantity()) {
            throw new InvalidQuantityException("Requested quantity (" + qty + " " + item.getUnit() + 
                ") exceeds available stock (" + item.getQuantity() + " " + item.getUnit() + ").");
        }

        // Apply rule-based dynamic subsidy
        double subsidyPercent = PriorityPricingService.calculateSubsidyPercentage(daysLeft);
        double effectivePrice = PriorityPricingService.calculateEffectivePrice(item.getBasePrice(), daysLeft);
        double totalValue = qty * effectivePrice;

        SimpleDateFormat sdfTxn = new SimpleDateFormat("yyyyMMddHHmmss");
        String txnId = "TXN-" + sdfTxn.format(new Date());

        SimpleDateFormat sdfDate = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss");
        String txnDate = sdfDate.format(new Date());

        return new DistributionRecord(
                txnId, item.getItemId(), item.getName(), recipient, 
                qty, item.getUnit(), item.getBasePrice(), subsidyPercent, 
                effectivePrice, totalValue, txnDate
        );
    }

    private void generateReceiptPreview() {
        try {
            DistributionRecord rec = validateAndPrepareRecord();

            StringBuilder sb = new StringBuilder();
            sb.append("====================================================\n");
            sb.append("             CHRONOCHEF FOOD BANK RECEIPT           \n");
            sb.append("           Zero Waste Distribution Program          \n");
            sb.append("====================================================\n");
            sb.append(String.format(" Transaction ID : %s\n", rec.getTransactionId()));
            sb.append(String.format(" Date & Time    : %s\n", rec.getTransactionDate()));
            sb.append(String.format(" Recipient Name : %s\n", rec.getRecipientName()));
            sb.append("----------------------------------------------------\n");
            sb.append(String.format(" Item ID        : %s\n", rec.getItemId()));
            sb.append(String.format(" Food Name      : %s\n", rec.getItemName()));
            sb.append(String.format(" Quantity Issued: %.2f %s\n", rec.getDistributedQuantity(), rec.getUnit()));
            sb.append(String.format(" Nominal Price  : Rs. %.2f per %s\n", rec.getBasePrice(), rec.getUnit()));
            sb.append(String.format(" Subsidy Applied: %.0f%% (Waste-Reduction Tier)\n", rec.getDiscountPercent()));
            sb.append(String.format(" Effective Price: Rs. %.2f per %s\n", rec.getEffectivePrice(), rec.getUnit()));
            sb.append("----------------------------------------------------\n");
            sb.append(String.format(" TOTAL PAYABLE  : Rs. %.2f\n", rec.getTotalValue()));
            if (rec.getTotalValue() == 0.0) {
                sb.append("   *** 100% SUBSIDIZED / FREE DONATION GRANTED *** \n");
            }
            sb.append("====================================================\n");
            sb.append(" Food Safety Certified: Item checked within expiry. \n");
            sb.append(" Thank you for helping minimize community food waste!\n");

            txtReceiptArea.setText(sb.toString());

        } catch (ExpiredItemDistributionException ex) {
            JOptionPane.showMessageDialog(this, ex.getMessage(), "Food Safety Guard", JOptionPane.ERROR_MESSAGE);
            txtReceiptArea.setText("\n  DISTRIBUTION BLOCKED:\n  " + ex.getMessage());
        } catch (InvalidQuantityException ex) {
            JOptionPane.showMessageDialog(this, ex.getMessage(), "Validation Error", JOptionPane.WARNING_MESSAGE);
        }
    }

    private void executeDistribution() {
        try {
            DistributionRecord rec = validateAndPrepareRecord();

            int confirm = JOptionPane.showConfirmDialog(this, 
                "Confirm distribution of " + rec.getDistributedQuantity() + " " + rec.getUnit() + 
                " of [" + rec.getItemName() + "] to [" + rec.getRecipientName() + "]?\nTotal: Rs. " + rec.getTotalValue(),
                "Confirm Distribution",
                JOptionPane.YES_NO_OPTION);

            if (confirm == JOptionPane.YES_OPTION) {
                boolean ok = dao.recordDistribution(rec);
                if (ok) {
                    JOptionPane.showMessageDialog(this, 
                        "Distribution completed successfully!\nReceipt #" + rec.getTransactionId() + " generated.",
                        "Success", 
                        JOptionPane.INFORMATION_MESSAGE);

                    txtDistributeQty.setText("");
                    mainFrame.refreshAllViews();
                } else {
                    JOptionPane.showMessageDialog(this, "Failed to record transaction.", "Error", JOptionPane.ERROR_MESSAGE);
                }
            }

        } catch (ExpiredItemDistributionException ex) {
            JOptionPane.showMessageDialog(this, ex.getMessage(), "Food Safety Block", JOptionPane.ERROR_MESSAGE);
        } catch (InvalidQuantityException ex) {
            JOptionPane.showMessageDialog(this, ex.getMessage(), "Input Validation", JOptionPane.WARNING_MESSAGE);
        } catch (Exception ex) {
            JOptionPane.showMessageDialog(this, "Distribution transaction error: " + ex.getMessage(), "Database Error", JOptionPane.ERROR_MESSAGE);
        }
    }
}
