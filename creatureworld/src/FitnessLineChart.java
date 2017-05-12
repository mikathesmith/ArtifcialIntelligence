import java.util.Scanner;
import java.io.*; 
import javafx.application.Application;
import javafx.scene.Scene;
import javafx.scene.chart.LineChart;
import javafx.scene.chart.NumberAxis;
import javafx.scene.chart.XYChart;
import javafx.scene.chart.XYChart.Series;
import javafx.stage.Stage;
 
//import static thorwin.math.Math.polyfit;
//import static thorwin.math.Math.polynomial;
 
/**
* The FitnessLineChart class extends the JavaFX LineChart Application Class. 
* 
* Produce a line chart plotting the data from MyWorld after the evolution has 
* been inducted. Plot the fitness of creatures over generations.  
* 
* Note: Must delete old fitnessdata.txt everytime you want to run a new round 
*
* @author  Mika Smith 
* @version 5.0
* @since   2017-04-05 
*/

public class FitnessLineChart extends Application {
	private static final String FILENAME = "fitnessdata.txt";
	
	/*Add a data point to the chart*/ 
	public void addToChart(Series<Number, Number> series, int generation, float fitness){
		series.getData().add(new XYChart.Data<Number, Number>(generation, fitness));
	}
 
    @Override public void start(Stage stage) {
    	  stage.setTitle("Change in Average Fitness");
          final NumberAxis xAxis = new NumberAxis();
          final NumberAxis yAxis = new NumberAxis();
          xAxis.setLabel("Generation");
          yAxis.setLabel("Average Fitness"); 
          
          //Manually set lower and upper bounds for fitness on the y axis
          yAxis.setLowerBound(1); 
          yAxis.setUpperBound(9);
          yAxis.setAutoRanging(false);
          
          //Create the line chart 
          final LineChart<Number,Number> lineChart =  new LineChart<Number,Number>(xAxis,yAxis);
          lineChart.setCreateSymbols(false); //creates more of a trend 
          
          //Create window with line chart 
          Scene scene  = new Scene(lineChart,800,600);
          
          //Create data series for fitness over fenerations
          Series<Number, Number> series = new XYChart.Series<Number, Number>();
	      series.setName("Average Fitness over generations");
	      
	      //Trend line 
	   //   Series<Number, Number> series2 = new XYChart.Series<Number, Number>();
	    //  series2.setName("Trend Line");
	     // double[] ys = new double[500];
	      //double[] xs = new double[500];
	      //int xi= 0, yi=0; 
	           
	      //Read in input from our file generated from MyWorld containing values of average fitness 
	      int gen=0; 
	      try {
	    	    BufferedReader in = new BufferedReader(new FileReader(FILENAME));
	    	    String str;
	    	    
	    	    while ((str = in.readLine()) != null){
	    	    	str= in.readLine(); 
	    	    	Scanner sc = new Scanner(str);
	    	    	gen = sc.nextInt();
	    	 //   	xs[xi] = (double) gen;
	    	  //  	xi++;
	    	    	float fitness = sc.nextFloat(); 
	    	    	float life = sc.nextFloat(); 
	    	 //   	System.out.println(life);
	    	   // 	ys[yi] = (double)fitness; 
	    	   // 	yi++;
	    	    	addToChart(series, gen, fitness); 
	    	    	sc.close(); 
	    	    } 
	    	    in.close();
	    	} catch (IOException e) {
	    		e.printStackTrace();
	    	}
	      lineChart.setTitle("Average Fitness over " + gen + " Generations");
	    	
	      
	  /*    	double[] coefficients = polyfit(xs, ys, 2); //polynomial trend algorithm, xs and ys are double arrays holding data points?? or axis?
	
	        for (double x = 0; x <= 5.0; x += 0.05) {
	            double y = polynomial(x, coefficients);
	            System.out.println(y);
	            series2.getData().add(new XYChart.Data<>(x, y));
	        }*/ 
	    
	    	
	      //Add our series data to the linechart 
        lineChart.getData().add(series); //Average fitness
       
        //Add linechart to window
        stage.setScene(scene);
        stage.show();
        
    //    stage.setScene(scene2);
      //  stage.show();
    }
 
    public static void main(String[] args) {
        launch(args);
    }
}