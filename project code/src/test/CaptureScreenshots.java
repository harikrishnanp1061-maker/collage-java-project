package test;

import database.DataSeeder;
import ui.MainFrame;

import javax.imageio.ImageIO;
import javax.swing.JButton;
import java.awt.Component;
import java.awt.Container;
import java.awt.Graphics2D;
import java.awt.image.BufferedImage;
import java.io.File;
import java.lang.reflect.Field;
import java.lang.reflect.Method;

public class CaptureScreenshots {
    public static void main(String[] args) {
        try {
            System.out.println("Initializing DB Seeder...");
            DataSeeder.seedIfEmpty();

            System.out.println("Instantiating MainFrame...");
            MainFrame frame = new MainFrame();
            frame.setSize(1080, 680);
            frame.setLocationRelativeTo(null);
            frame.setVisible(true);

            // Give Swing a moment to layout and render
            Thread.sleep(1200);

            // Get fields via reflection to click tabs
            Field btnNavInventoryField = MainFrame.class.getDeclaredField("btnNavInventory");
            Field btnNavInputField = MainFrame.class.getDeclaredField("btnNavInput");
            Field btnNavManageField = MainFrame.class.getDeclaredField("btnNavManage");
            Field btnNavDistributeField = MainFrame.class.getDeclaredField("btnNavDistribute");
            Field btnNavAnalyticsField = MainFrame.class.getDeclaredField("btnNavAnalytics");

            btnNavInventoryField.setAccessible(true);
            btnNavInputField.setAccessible(true);
            btnNavManageField.setAccessible(true);
            btnNavDistributeField.setAccessible(true);
            btnNavAnalyticsField.setAccessible(true);

            JButton btnInventory = (JButton) btnNavInventoryField.get(frame);
            JButton btnInput = (JButton) btnNavInputField.get(frame);
            JButton btnManage = (JButton) btnNavManageField.get(frame);
            JButton btnDistribute = (JButton) btnNavDistributeField.get(frame);
            JButton btnAnalytics = (JButton) btnNavAnalyticsField.get(frame);

            File outDir = new File("screenshots");
            if (!outDir.exists()) outDir.mkdirs();

            // Capture 1: Inventory (Default)
            btnInventory.doClick();
            Thread.sleep(600);
            saveFrame(frame, "screenshots/01_inventory_tracker.png");

            // Capture 2: Input Panel
            btnInput.doClick();
            Thread.sleep(600);
            saveFrame(frame, "screenshots/02_input_panel.png");

            // Capture 3: Manage Stock
            btnManage.doClick();
            Thread.sleep(600);
            saveFrame(frame, "screenshots/03_manage_stock.png");

            // Capture 4: Distribute & Bill
            btnDistribute.doClick();
            Thread.sleep(600);
            saveFrame(frame, "screenshots/04_distribute_billing.png");

            // Capture 5: Analytics
            btnAnalytics.doClick();
            Thread.sleep(600);
            saveFrame(frame, "screenshots/05_analytics_dashboard.png");

            frame.dispose();
            System.out.println("All screenshots successfully captured into screenshots/!");
            System.exit(0);
        } catch (Exception e) {
            e.printStackTrace();
            System.exit(1);
        }
    }

    private static void saveFrame(MainFrame frame, String path) {
        try {
            int w = frame.getWidth();
            int h = frame.getHeight();
            BufferedImage image = new BufferedImage(w, h, BufferedImage.TYPE_INT_RGB);
            Graphics2D g2 = image.createGraphics();
            frame.printAll(g2);
            g2.dispose();
            ImageIO.write(image, "png", new File(path));
            System.out.println("Saved: " + path + " (" + w + "x" + h + ")");
        } catch (Exception e) {
            System.err.println("Failed to save " + path + ": " + e.getMessage());
        }
    }
}
