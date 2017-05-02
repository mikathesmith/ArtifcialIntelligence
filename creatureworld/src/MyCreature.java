import cosc343.assig2.Creature;
import java.util.*; 
import java.util.Random;

/**
* The MyCreate extends the cosc343 assignment 2 Creature.  Here you implement
* creatures chromosome and the agent function that maps creature percepts to
* actions.  
* 
* Implement a chromosome governed model that maps percepts to actions in the 
* AgentFunction. Implement creature behaviour. 
*
* @author  Mika Smith 
* @version 2.0
* @since   2017-04-05 
*/
public class MyCreature extends Creature {

  // Random number generator
  Random rand = new Random();
    private final int numPercepts;
    private final int numActions;
    static int pID=0;  
    int parentID=0;
    private int[] chromosome; 
    public HashMap<String, Integer> directionMap = new HashMap<String, Integer>()
    {{
	    put("000", 0);
	    put("001", 1);
	    put("010", 2);
	    put("011", 3);
	    put("100", 4);
	    put("101", 5);
	    put("110", 6);
	    put("111", 7);
    }};
    
    

  /* Empty constructor - might be a good idea here to put the code that 
   initialises the chromosome to some random state  
  
  Initialisation of chromosome and anything else the creature requires should 
  go in here 
  
   Input: numPercept - number of percepts that creature will be receiving
          numAction - number of action output vector that creature will need
                      to produce on every turn
  */
  public MyCreature(int numPercepts, int numActions) { //This whole class s its chromosome!
      this.numPercepts = numPercepts;
      this.numActions = numActions;  //expected from the agentfunction
      pID++; 
      parentID = pID; //way to uniquelly identify a creature 
      chromosome = new int[7];
      //Index 0 = eat green stawberry or not
      //Index 1, 2, 3 = avoidance behaviour if x1, opposite behaviour if x2, or if both? 
      //Index 4, 5, 6 = attraction behaviour 
      //Index 7 = follow other creatures or not
      //Index 8 = always random behaviour 
      for(int i=0; i < chromosome.length;i++){
    	  chromosome[i] = rand.nextInt(2); //initialises genes to either 1 or 0 
      }
      
      //chromosome encoding goes here - how it reacts to percepts.  
      //Array or seperate values? 
	      //whether to avoid monsters
	      //direction to avoid
	      //direction to go towards
	      //avoid or towards other creature's, or dont care 
	      //avoid or towards food, or dont care
	      //eat green strawberries or not 
      //
  }
  public String findGene(int a, int b, int c){
	  StringBuilder gene = new StringBuilder();
	  gene.append(a);
	  gene.append(b);
	  gene.append(c);
	  return gene.toString();
	  
  }
  //pass in a gene encoding movement behaviour, need to look it up and return the associated action
  public int findDirection(String gene){ //have a bool value opposite? 
	  return directionMap.get(gene); 
  }
  
  /* This function must be overridden by MyCreature, because it implements
     the AgentFunction which controls creature behavoiur.  This behaviour
     should be governed by a model (that you need to come up with) that is
     parameterise by the chromosome.  AgentFunction can access any variable
     in the chromosome constructor. 
  
     Input: percepts - an array of percepts
            numPercepts - the size of the array of percepts depend on the percept
                          chosen - 8
            numExpectedAction - this number tells you what the expected size
                                of the returned array of percepts should bes -11
     Returns: an array of actions 
     
    
     
  */
  @Override 
  public float[] AgentFunction(int[] percepts, int numPercepts, int numExpectedActions) {
	//need to compute action vector from percept vector. Parametrised by the chromosome, so that when  
	 //the chromosome values change, the computation changes.  
      
      // This is where your chromosome gives rise to the model that maps
      // percepts to actions.  This function governs your creature's behaviour.
      // You need to figure out what model you want to use, and how you're going
      // to encode its parameters in a chromosome.
      
      // At the moment, the actions are chosen completely at random, ignoring
      // the percepts.  You need to replace this code.
      float actions[] = new float[numExpectedActions];
      int moveDirection;
      Boolean eat= (chromosome[0]==1) ? true : false;
      String avoidance = findGene(chromosome[1], chromosome[2], chromosome[3]);
	  String attraction = findGene(chromosome[4], chromosome[5], chromosome[6]);
      
      //the random values must be changed so they are based on the parameters of a
      //given creature's chromosome. 
      for(int i=0;i<numExpectedActions;i++) { //get rid of loop eventually? 
    	  //setting to arbitrary values, though could be used as priority as the action with
    	  //the largest value will be executed.
    	  
    	  //Note: more than one percept could be set! 
    	  
    	  //extract chromosome[2-4] as avoidance behaviour
  
    	  //use a choose random action function. 
    	 if(percepts[7]==1){ //on red strawberry 
    		 actions[9] = 10;   //ALWAYS eat the strawberry
    	 }else if(percepts[6]==1){ //on green strawberry, 
    		 //eat = rand.nextBoolean(); //randomly, either eat or dont 
    		 if(eat){ //
    			 actions[9] = 10; 
    	//		 System.out.println(parentID + " chose to eat");
    		 }else{
    	//		 System.out.println(parentID + " said ew gross no thanks");
    		 }
    	 }else if(percepts[0]==1){ //monsters in vicinity  - should be priority! 
    		// System.out.println("Avoided! direction 1" );
    		 moveDirection = findDirection(avoidance);
    		// System.out.println("Moving in direction " + moveDirection);
    		 actions[moveDirection] = 10; //0 to 7 inclusive for movement in some direction 
    	 }else if(percepts[1]==1){ //monsters in other vicinity 
    		 moveDirection = findDirection(avoidance);  //move in opposite direction 
    		// System.out.println("Avoided! direction 2" );
    		 actions[moveDirection] = 10; 
    	 }else{ //no mosters in vicinity
    		 if(percepts[4]==1){
    			moveDirection = findDirection(attraction); //there is food, move towards  
    			actions[moveDirection] = 10; 
    		 }
    		 if(percepts[5]==1){
    			 moveDirection = findDirection(attraction); //there is food, move towards  
     			 actions[moveDirection] = 10; 
    	     }
    		 actions[10] = 5; //currently do random movement  
    		 //want to change to if safe from monsters, move towards creatures or strawberries. 
    	 }
    	  
         //actions[i]=rand.nextFloat();
         
    	//Makes the creatures never move 
    	
      } 
      
      //implement a computational modeel that computes action vector from the 
      //percept vector. This model should be parametrised by the chromosome,
      //so that when the chromosome values change, the computation changes.
      //
      return actions; //return array of actions. The index of the largest value
      //element in the action array will be taken as the desired action. 
  }
  
  
}