import database.DataSeeder;
import database.DatabaseManager;
import ui.MainFrame;

import javax.swing.SwingUtilities;
import javax.swing.UIManager;

/**
 * Main - Entry Point for the ChronoChef Food Bank Management System
 * 
 * College Syllabus Mapping:
 * - Module 1: Structure of a simple Java program (Main method, JVM entry point)
 * - Module 4: Swing GUI Initialization via Event Dispatch Thread (SwingUtilities.invokeLater)
 */
public class Main {

    public static void main(String[] args) {
        System.out.println("==========================================================");
        System.out.println("  Starting ChronoChef: Smart Dynamic Pricing & Expiry Tracker");
        System.out.println("  Course: PBCST304 Object Oriented Programming Project");
        System.out.println("==========================================================");

        // 1. Initialize SQLite Database Connection (Singleton Pattern)
        DatabaseManager.getInstance();

        // 2. Pre-populate database with diverse dummy data if empty
        DataSeeder.seedIfEmpty();

        // 3. Launch Graphical User Interface on Swing Event Dispatch Thread
        SwingUtilities.invokeLater(new Runnable() {
            @Override
            public void run() {
                try {
                    // Module 4, Slides 16-17: Pluggable Look and Feel (PLAF)
                    // Nimbus ensures custom button backgrounds and high-contrast text render properly
                    boolean nimbusSet = false;
                    for (UIManager.LookAndFeelInfo info : UIManager.getInstalledLookAndFeels()) {
                        if ("Nimbus".equals(info.getName())) {
                            UIManager.setLookAndFeel(info.getClassName());
                            nimbusSet = true;
                            break;
                        }
                    }
                    if (!nimbusSet) {
                        UIManager.setLookAndFeel(UIManager.getCrossPlatformLookAndFeelClassName());
                    }
                } catch (Exception e) {
                    // Fallback to default Java Swing look-and-feel if unavailable
                }

                MainFrame frame = new MainFrame();
                frame.setVisible(true);
                System.out.println("[Main] ChronoChef GUI is now visible and active.");
            }
        });
    }
}
