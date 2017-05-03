import java.io.BufferedReader;
import java.io.FileReader;
import java.util.Scanner;
import java.io.*; 
import javafx.application.Application;
import javafx.scene.Scene;
import javafx.scene.chart.CategoryAxis;
import javafx.scene.chart.LineChart;
import javafx.scene.chart.NumberAxis;
import javafx.scene.chart.XYChart;
import javafx.scene.chart.XYChart.Series;
import javafx.stage.Stage;
 
 
public class FitnessLineChart extends Application {
	private static final String FILENAME = "fitnessdata.txt";
	
	public void addToChart(Series<Number, Number> series, int generation, float fitness){
		series.getData().add(new XYChart.Data<Number, Number>(generation, fitness));
		
	}
 
    @Override public void start(Stage stage) {
    	  stage.setTitle("G");
          final NumberAxis xAxis = new NumberAxis();
          final NumberAxis yAxis = new NumberAxis();
          xAxis.setLabel("Generation");  //should be 1 to 500 
          yAxis.setLabel("Fitness"); 
          
          final LineChart<Number,Number> lineChart = 
                  new LineChart<Number,Number>(xAxis,yAxis);
                  
          lineChart.setTitle("Fitness over 500 Generations");
                                  
          Series<Number, Number> series = new XYChart.Series<Number, Number>();
          series.setName("Mika Smith");
          
          
    	try {
    	    BufferedReader in = new BufferedReader(new FileReader(FILENAME));
    	    String str;
    	    
    	    //Figure out how to read in 2 ints on one line using bufferedreader!! 
    	    while ((str = in.readLine()) != null){
    	    	str= in.readLine(); 
    	    	Scanner sc = new Scanner(str);
    	    	int gen = sc.nextInt();
    	    	float fitness = sc.nextFloat(); 
    	   // 	System.out.println(gen + " " + fitness);
    	    	addToChart(series, gen, fitness); 
    	    }
    	        
    	    in.close();
    	} catch (IOException e) {
    	}
    	
    	
      
   /*     while(sc.hasNextLine()){
        	
        }
        */

        
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