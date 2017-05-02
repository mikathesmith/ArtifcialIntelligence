public class LineChart extends JFrame {
 
    public LineChart() {
        super("Line Chart");
 
        JPanel chartPanel = createChartPanel();
        add(chartPanel, BorderLayout.CENTER);
 
        setSize(640, 480);
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        setLocationRelativeTo(null);
    }
 
    private JPanel createChartPanel() {
        // creates a line chart object
        // returns the chart panel
    }
 
    private XYDataset createDataset() {
        // creates an XY dataset...
        // returns the dataset
    }
 
    public static void main(String[] args) {
        SwingUtilities.invokeLater(new Runnable() {
            @Override
            public void run() {
                new XYLineChartExample().setVisible(true);
            }
        });
    }
}