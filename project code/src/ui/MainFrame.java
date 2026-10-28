package ui;

import javax.swing.BorderFactory;
import javax.swing.JButton;
import javax.swing.JFrame;
import javax.swing.JLabel;
import javax.swing.JPanel;
import java.awt.BorderLayout;
import java.awt.CardLayout;
import java.awt.Color;
import java.awt.Dimension;
import java.awt.FlowLayout;
import java.awt.Font;
import java.awt.GridLayout;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;

/**
 * MainFrame - Main Application Window for ChronoChef
 * 
 * Coordinates all five interfaces within a single JFrame using CardLayout.
 * 
 * College Syllabus Mapping:
 * - Module 4: Swings Fundamentals - JFrame as top-level container (Slide 24, 28)
 * - Module 4: CardLayout (Slides 49-55): Arranges views like a stack of cards
 * - Module 4: Delegation Event Model (ActionListener and ActionEvent)
 * - Module 4: Model-View-Controller (View Coordinator)
 */
public class MainFrame extends JFrame implements ActionListener {

    private CardLayout cardLayout;
    private JPanel cardsPanel;

    // The Five Application Panels (Views)
    private InputPanel inputPanel;
    private InventoryPanel inventoryPanel;
    private ManagementPanel managementPanel;
    private DistributionPanel distributionPanel;
    private AnalyticsPanel analyticsPanel;

    // Navigation Buttons
    private JButton btnNavInput;
    private JButton btnNavInventory;
    private JButton btnNavManage;
    private JButton btnNavDistribute;
    private JButton btnNavAnalytics;

    private JLabel lblFooterStatus;

    // Card Names constants
    public static final String CARD_INPUT = "INPUT";
    public static final String CARD_INVENTORY = "INVENTORY";
    public static final String CARD_MANAGE = "MANAGE";
    public static final String CARD_DISTRIBUTE = "DISTRIBUTE";
    public static final String CARD_ANALYTICS = "ANALYTICS";

    public MainFrame() {
        super("ChronoChef - Smart Dynamic Pricing & Expiry Tracker for Food Banks");

        // Window Settings (Module 4, Slide 38)
        setSize(1080, 680);
        setMinimumSize(new Dimension(960, 600));
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        setLocationRelativeTo(null); // Center on screen
        setLayout(new BorderLayout());

        // 1. Top Header Banner Panel
        JPanel topHeaderPanel = new JPanel(new BorderLayout());
        topHeaderPanel.setBackground(new Color(25, 45, 80));
        topHeaderPanel.setBorder(BorderFactory.createEmptyBorder(12, 20, 10, 20));

        JLabel lblAppName = new JLabel("ChronoChef: Food Bank Expiry & Dynamic Subsidy Tracker");
        lblAppName.setFont(new Font("Arial", Font.BOLD, 20));
        lblAppName.setForeground(Color.WHITE);

        JLabel lblSub = new JLabel("PBCST304 Object Oriented Programming College Project");
        lblSub.setFont(new Font("Arial", Font.ITALIC, 11));
        lblSub.setForeground(new Color(190, 210, 240));

        JPanel titleBlock = new JPanel(new GridLayout(2, 1));
        titleBlock.setOpaque(false);
        titleBlock.add(lblAppName);
        titleBlock.add(lblSub);
        topHeaderPanel.add(titleBlock, BorderLayout.WEST);

        // 2. Navigation Bar Panel (Module 4 FlowLayout)
        JPanel navPanel = new JPanel(new FlowLayout(FlowLayout.RIGHT, 8, 4));
        navPanel.setOpaque(false);

        btnNavInput = createNavButton("1. Add Item", CARD_INPUT);
        btnNavInventory = createNavButton("2. Expiry Tracker", CARD_INVENTORY);
        btnNavManage = createNavButton("3. Manage Stock", CARD_MANAGE);
        btnNavDistribute = createNavButton("4. Distribute & Bill", CARD_DISTRIBUTE);
        btnNavAnalytics = createNavButton("5. Analytics", CARD_ANALYTICS);

        navPanel.add(btnNavInput);
        navPanel.add(btnNavInventory);
        navPanel.add(btnNavManage);
        navPanel.add(btnNavDistribute);
        navPanel.add(btnNavAnalytics);

        topHeaderPanel.add(navPanel, BorderLayout.EAST);
        add(topHeaderPanel, BorderLayout.NORTH);

        // 3. Center Container with CardLayout (Module 4, Slides 49-55)
        cardLayout = new CardLayout();
        cardsPanel = new JPanel(cardLayout);

        // Instantiate the 5 Views
        inputPanel = new InputPanel(this);
        inventoryPanel = new InventoryPanel(this);
        managementPanel = new ManagementPanel(this);
        distributionPanel = new DistributionPanel(this);
        analyticsPanel = new AnalyticsPanel(this);

        // Add views to CardLayout deck
        cardsPanel.add(inventoryPanel, CARD_INVENTORY);   // Default view
        cardsPanel.add(inputPanel, CARD_INPUT);
        cardsPanel.add(managementPanel, CARD_MANAGE);
        cardsPanel.add(distributionPanel, CARD_DISTRIBUTE);
        cardsPanel.add(analyticsPanel, CARD_ANALYTICS);

        add(cardsPanel, BorderLayout.CENTER);

        // 4. Bottom Footer Status Bar
        JPanel footerPanel = new JPanel(new FlowLayout(FlowLayout.LEFT, 15, 6));
        footerPanel.setBackground(new Color(240, 243, 248));
        footerPanel.setBorder(BorderFactory.createMatteBorder(1, 0, 0, 0, new Color(210, 220, 235)));

        lblFooterStatus = new JLabel("System Ready | Connected to SQLite Database (chronochef.db) | Single Source of Truth Active");
        lblFooterStatus.setFont(new Font("Arial", Font.PLAIN, 12));
        lblFooterStatus.setForeground(new Color(60, 75, 95));
        footerPanel.add(lblFooterStatus);

        add(footerPanel, BorderLayout.SOUTH);

        // Start by displaying the Expiry Tracker view
        highlightActiveButton(btnNavInventory);
        cardLayout.show(cardsPanel, CARD_INVENTORY);
    }

    private JButton createNavButton(String label, String command) {
        JButton btn = new JButton(label);
        btn.setActionCommand(command);
        btn.setFont(new Font("Arial", Font.BOLD, 12));
        btn.setFocusPainted(false);
        btn.setOpaque(true);
        btn.setBackground(new Color(35, 65, 110));
        btn.setForeground(Color.WHITE);
        btn.setPreferredSize(new Dimension(140, 32));
        btn.addActionListener(this);
        return btn;
    }

    private void highlightActiveButton(JButton activeBtn) {
        JButton[] buttons = {btnNavInput, btnNavInventory, btnNavManage, btnNavDistribute, btnNavAnalytics};
        for (int i = 0; i < buttons.length; i++) {
            if (buttons[i] == activeBtn) {
                buttons[i].setBackground(new Color(255, 175, 30)); // Bright golden-amber
                buttons[i].setForeground(new Color(20, 20, 20));    // Deep black for contrast
            } else {
                buttons[i].setBackground(new Color(35, 65, 110));  // Dark navy
                buttons[i].setForeground(Color.WHITE);
            }
        }
    }

    /**
     * Event Handling: Delegation Event Model (Module 4, Slides 63-65)
     */
    @Override
    public void actionPerformed(ActionEvent e) {
        String cmd = e.getActionCommand();
        highlightActiveButton((JButton) e.getSource());

        // Switch active Card view
        cardLayout.show(cardsPanel, cmd);

        // Refresh view when visited to guarantee data consistency
        if (CARD_INVENTORY.equals(cmd)) {
            inventoryPanel.loadInventoryData();
        } else if (CARD_MANAGE.equals(cmd)) {
            managementPanel.populateItemSelector();
        } else if (CARD_DISTRIBUTE.equals(cmd)) {
            distributionPanel.populateItemSelect();
        } else if (CARD_ANALYTICS.equals(cmd)) {
            analyticsPanel.loadAnalyticsData();
        }
    }

    /**
     * Refresh all 5 views to enforce consistent underlying database state
     */
    public void refreshAllViews() {
        inventoryPanel.loadInventoryData();
        managementPanel.populateItemSelector();
        distributionPanel.populateItemSelect();
        analyticsPanel.loadAnalyticsData();
    }
}
