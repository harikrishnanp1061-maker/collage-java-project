package ui;

import database.FoodBankDAO;
import model.DistributionRecord;
import model.FoodItem;
import service.PriorityPricingService;

import javax.swing.BorderFactory;
import javax.swing.JButton;
import javax.swing.JLabel;
import javax.swing.JOptionPane;
import javax.swing.JPanel;
import javax.swing.JScrollPane;
import javax.swing.JTable;
import javax.swing.table.DefaultTableModel;
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
 * AnalyticsPanel - Module E: Analysis and Reporting Interface
 * 
 * Aggregates live metrics from the central database:
 * - Total inventory volume
 * - Urgent and expired items counts
 * - Total waste prevented and value distributed
 * - Transaction log table
 * 
 * College Syllabus Mapping:
 * - Module 4: Swing controls (JTable, JPanel, GridLayout)
 * - Module 1: Calculations, Iteration statements (for loops)
 */
public class AnalyticsPanel extends JPanel implements ActionListener {

    private JLabel lblTotalItems;
    private JLabel lblTotalQuantity;
    private JLabel lblUrgentCount;
    private JLabel lblExpiredCount;
    private JLabel lblTotalDistributed;
    private JLabel lblTotalValueSubsidized;

    private JTable transactionTable;
    private DefaultTableModel transTableModel;
    private JButton btnRefresh;

    private FoodBankDAO dao;
    private MainFrame mainFrame;

    public AnalyticsPanel(MainFrame mainFrame) {
        this.mainFrame = mainFrame;
        this.dao = new FoodBankDAO();

        setLayout(new BorderLayout(15, 15));
        setBorder(BorderFactory.createEmptyBorder(15, 20, 15, 20));

        // Top Header
        JPanel northPanel = new JPanel(new BorderLayout(10, 10));

        JLabel lblTitle = new JLabel("Analysis & Reporting: Food Bank Impact Overview", JLabel.LEFT);
        lblTitle.setFont(new Font("Arial", Font.BOLD, 18));
        lblTitle.setForeground(new Color(30, 60, 100));
        northPanel.add(lblTitle, BorderLayout.WEST);

        btnRefresh = new JButton("Refresh Analytics");
        btnRefresh.addActionListener(this);
        northPanel.add(btnRefresh, BorderLayout.EAST);

        // Metric Summary Cards in 2x3 Grid
        JPanel metricsGrid = new JPanel(new GridLayout(2, 3, 15, 15));
        metricsGrid.setBorder(BorderFactory.createEmptyBorder(10, 0, 10, 0));

        lblTotalItems = createMetricLabel("0");
        lblTotalQuantity = createMetricLabel("0.0");
        lblUrgentCount = createMetricLabel("0");
        lblExpiredCount = createMetricLabel("0");
        lblTotalDistributed = createMetricLabel("0");
        lblTotalValueSubsidized = createMetricLabel("Rs. 0.00");

        metricsGrid.add(createMetricCard("Total Items Tracked", lblTotalItems, new Color(230, 240, 255)));
        metricsGrid.add(createMetricCard("Total Available Stock (Units)", lblTotalQuantity, new Color(235, 250, 235)));
        metricsGrid.add(createMetricCard("Urgent Items (0-5 Days Left)", lblUrgentCount, new Color(255, 245, 230)));
        metricsGrid.add(createMetricCard("Expired / Quarantined Items", lblExpiredCount, new Color(255, 235, 235)));
        metricsGrid.add(createMetricCard("Distributions Completed", lblTotalDistributed, new Color(240, 235, 255)));
        metricsGrid.add(createMetricCard("Total Value Subsidized", lblTotalValueSubsidized, new Color(230, 250, 250)));

        northPanel.add(metricsGrid, BorderLayout.SOUTH);
        add(northPanel, BorderLayout.NORTH);

        // Center: Distribution History Table
        JPanel tableContainer = new JPanel(new BorderLayout(5, 5));
        tableContainer.setBorder(BorderFactory.createTitledBorder("Recent Distribution Transactions Log"));

        String[] transColumns = {
            "Txn ID", "Timestamp", "Food Item", "Recipient Name", "Quantity", "Unit", "Base Price", "Subsidy %", "Total Paid"
        };
        transTableModel = new DefaultTableModel(transColumns, 0) {
            @Override
            public boolean isCellEditable(int row, int column) {
                return false;
            }
        };

        transactionTable = new JTable(transTableModel);
        transactionTable.setRowHeight(24);
        transactionTable.getTableHeader().setFont(new Font("Arial", Font.BOLD, 12));
        transactionTable.getTableHeader().setBackground(new Color(235, 240, 248));

        JScrollPane scrollPane = new JScrollPane(transactionTable);
        tableContainer.add(scrollPane, BorderLayout.CENTER);

        add(tableContainer, BorderLayout.CENTER);

        // Load data
        loadAnalyticsData();
    }

    private JLabel createMetricLabel(String initialText) {
        JLabel label = new JLabel(initialText, JLabel.CENTER);
        label.setFont(new Font("Arial", Font.BOLD, 22));
        label.setForeground(new Color(20, 40, 70));
        return label;
    }

    private JPanel createMetricCard(String title, JLabel valueLabel, Color bg) {
        JPanel card = new JPanel(new BorderLayout(5, 5));
        card.setBackground(bg);
        card.setBorder(BorderFactory.createCompoundBorder(
                BorderFactory.createLineBorder(new Color(210, 220, 235), 1),
                BorderFactory.createEmptyBorder(10, 10, 10, 10)
        ));

        JLabel lblCardTitle = new JLabel(title, JLabel.CENTER);
        lblCardTitle.setFont(new Font("Arial", Font.PLAIN, 12));
        lblCardTitle.setForeground(new Color(80, 90, 100));

        card.add(lblCardTitle, BorderLayout.NORTH);
        card.add(valueLabel, BorderLayout.CENTER);
        return card;
    }

    /**
     * Compute summary metrics and populate tables from database
     */
    public void loadAnalyticsData() {
        try {
            // 1. Compute Inventory Metrics
            Vector<FoodItem> items = dao.getAllItems();
            int totalItems = items.size();
            double totalStock = 0.0;
            int urgentCount = 0;
            int expiredCount = 0;

            for (int i = 0; i < items.size(); i++) {
                FoodItem it = items.get(i);
                totalStock += it.getQuantity();

                int days = PriorityPricingService.calculateDaysRemaining(it.getExpiryDate());
                if (days < 0) {
                    expiredCount++;
                } else if (days <= 5) {
                    urgentCount++;
                }
            }

            lblTotalItems.setText(String.valueOf(totalItems));
            lblTotalQuantity.setText(String.format("%.1f", totalStock));
            lblUrgentCount.setText(String.valueOf(urgentCount));
            lblExpiredCount.setText(String.valueOf(expiredCount));

            // 2. Compute Distribution Metrics & Populate Table
            Vector<DistributionRecord> distributions = dao.getAllDistributions();
            transTableModel.setRowCount(0);

            double totalSubsidizedValue = 0.0;
            for (int i = 0; i < distributions.size(); i++) {
                DistributionRecord d = distributions.get(i);

                Vector<Object> row = new Vector<Object>();
                row.add(d.getTransactionId());
                row.add(d.getTransactionDate());
                row.add(d.getItemName());
                row.add(d.getRecipientName());
                row.add(d.getDistributedQuantity());
                row.add(d.getUnit());
                row.add("Rs. " + String.format("%.2f", d.getBasePrice()));
                row.add(String.format("%.0f%%", d.getDiscountPercent()));
                row.add("Rs. " + String.format("%.2f", d.getTotalValue()));
                transTableModel.addRow(row);

                // Calculate subsidy amount granted: (basePrice - effectivePrice) * qty
                double subsidyPerUnit = d.getBasePrice() - d.getEffectivePrice();
                totalSubsidizedValue += (subsidyPerUnit * d.getDistributedQuantity());
            }

            lblTotalDistributed.setText(String.valueOf(distributions.size()));
            lblTotalValueSubsidized.setText("Rs. " + String.format("%.2f", totalSubsidizedValue));

        } catch (Exception e) {
            JOptionPane.showMessageDialog(this, "Error updating analytics: " + e.getMessage(), "Error", JOptionPane.ERROR_MESSAGE);
        }
    }

    @Override
    public void actionPerformed(ActionEvent e) {
        if (e.getSource() == btnRefresh) {
            loadAnalyticsData();
        }
    }
}
