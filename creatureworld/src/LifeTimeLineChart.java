import java.util.Scanner;
import java.io.*; 
import javafx.application.Application;
import javafx.scene.Scene;
import javafx.scene.chart.LineChart;
import javafx.scene.chart.NumberAxis;
import javafx.scene.chart.XYChart;
import javafx.scene.chart.XYChart.Series;
import javafx.stage.Stage;
 
/**
* The Life Time LineChart class extends the JavaFX LineChart Application Class. 
* 
* Produce a line chart plotting the data from MyWorld after the evolution has 
* been inducted. Plot the life time of creatures over generations.  
* 
* Note: Must delete old fitnessdata.txt everytime you want to run a new round 
*
* @author  Mika Smith 
* @version 5.0
* @since   2017-04-05 
*/

public class LifeTimeLineChart extends Application {
	private static final String FILENAME = "fitnessdata.txt";
	
	/*Add a data point to the chart*/ 
	public void addToChart(Series<Number, Number> series, int generation, float fitness){
		series.getData().add(new XYChart.Data<Number, Number>(generation, fitness));
	}
 
    @Override public void start(Stage stage) {
    	  stage.setTitle("Change in Average Life Time");
          final NumberAxis xAxis = new NumberAxis();
          final NumberAxis yAxis = new NumberAxis();
          xAxis.setLabel("Generation");
          yAxis.setLabel("Average Life Time");
          
          //Manually set lower and upper bounds for fitness on the y axis
          yAxis.setLowerBound(20); 
          yAxis.setUpperBound(60);
          yAxis.setAutoRanging(false);
          
          //Create the line chart 
          final LineChart<Number,Number> lineChart =  new LineChart<Number,Number>(xAxis,yAxis);
          
          lineChart.setCreateSymbols(false); //creates more of a trend 
          
          //Create window with line chart 
          Scene scene  = new Scene(lineChart,800,600);
          
          //Create data series for lifetime over generations
	      Series<Number, Number> series2 = new XYChart.Series<Number, Number>();
		  series2.setName("Average Lifetime");
	           
	      //Read in input from our file generated from MyWorld containing values of average fitness 
		  int gen=0; 
	      try {
	    	    BufferedReader in = new BufferedReader(new FileReader(FILENAME));
	    	    String str;
	    	    
	    	    while ((str = in.readLine()) != null){
	    	    	str= in.readLine(); 
	    	    	Scanner sc = new Scanner(str);
	    	    	gen = sc.nextInt();
	    	    	float fitness = sc.nextFloat(); 
	    	    	float life = sc.nextFloat(); 
	    	    	addToChart(series2, gen, life);
	    	    	sc.close(); 
	    	    } 
	    	    in.close();
	    	} catch (IOException e) {
	    		e.printStackTrace();
	    	}
	      lineChart.setTitle("Average Life Time over " + gen + " Generations");
	    //Add our series data to the linechart 
        lineChart.getData().add(series2); //Average lifetime
       
        //Add linechart to window
        stage.setScene(scene);
        stage.show();
    }
 
    public static void main(String[] args) {
        launch(args);
    }
}