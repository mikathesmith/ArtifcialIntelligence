import javafx.application.Application;
import javafx.scene.Scene;
import javafx.scene.chart.CategoryAxis;
import javafx.scene.chart.LineChart;
import javafx.scene.chart.NumberAxis;
import javafx.scene.chart.XYChart;
import javafx.scene.chart.XYChart.Series;
import javafx.stage.Stage;
 
 
public class LineChart extends Application {
 
    @Override public void start(Stage stage) {
        stage.setTitle("Line Chart Sample");
        final CategoryAxis xAxis = new CategoryAxis();
        final NumberAxis yAxis = new NumberAxis();
        xAxis.setLabel("Generation");       
        
        final LineChart<String,Number> lineChart = 
                new LineChart<String,Number>(xAxis,yAxis);
                
        lineChart.setTitle("Fitness over 500 Generations");
                                
        Series<String, Number> series = new XYChart.Series<String, Number>();
        series.setName("Mika Smith");
        
        series.getData().add(new XYChart.Data<String, Number>("Jan", 23));
        series.getData().add(new XYChart.Data<String, Number>("Feb", 14));
        series.getData().add(new XYChart.Data<String, Number>("Mar", 15));
        series.getData().add(new XYChart.Data<String, Number>("Apr", 24));
        series.getData().add(new XYChart.Data<String, Number>("May", 34));
        series.getData().add(new XYChart.Data<String, Number>("Jun", 36));
        series.getData().add(new XYChart.Data<String, Number>("Jul", 22));
        series.getData().add(new XYChart.Data<String, Number>("Aug", 45));
        series.getData().add(new XYChart.Data<String, Number>("Sep", 43));
        series.getData().add(new XYChart.Data<String, Number>("Oct", 17));
        series.getData().add(new XYChart.Data<String, Number>("Nov", 29));
        series.getData().add(new XYChart.Data<String, Number>("Dec", 25));
        
        
        Scene scene  = new Scene(lineChart,800,600);
        lineChart.getData().add(series);
       // add(series);
       
        stage.setScene(scene);
        stage.show();
    }
 
    public static void main(String[] args) {
        launch(args);
    }
}