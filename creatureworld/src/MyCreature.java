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
* @version 3.0
* @since   2017-04-05 
*/
public class MyCreature extends Creature {

  // Random number generator
	Random rand = new Random();
    private final int numPercepts;
    private final int numActions;
    static int cID=0;  
    int creatureID=0;
    public int[] chromosome; 
    public HashMap<String, Integer> directionMap = new HashMap<String, Integer>()
    {{
	    put("000", 0);
	    put("001", 1);
	    put("010", 2);
	    put("011", 3);
	    put("100", 8); //action 4 is dont move! should I change this back? 
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
      cID++; 
      creatureID = cID; //way to uniquelly identify a creature 
      chromosome = new int[8];
      //Index 0 = eat green stawberry or not
      //Index 1, 2, 3 = avoidance behaviour if x1, opposite behaviour if x2, or if both? 
      //Index 4, 5, 6 = attraction behaviour 
      //Index 7 = follow other creatures or not
      //Index 8 = always random behaviour 
      for(int i=0; i < chromosome.length;i++){
    	  chromosome[i] = rand.nextInt(2); //initialises genes to either 1 or 0 
    	//  System.out.println(chromosome[i]);
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
  
  //Finds the gene for direction - 3 bits, 8 possible values (8 possible directions) 
  public StringBuilder findGene(int a, int b, int c){
	  StringBuilder gene = new StringBuilder();
	  gene.append(a);
	  gene.append(b);
	  gene.append(c);
	  return gene;
  }
  
  //pass in a gene encoding movement behaviour, need to look it up and return the associated action
  public int findDirection(StringBuilder gene, Boolean flip, int bitToFlip){ //have a bool value opposite? 
	 if(flip){
		 //else replace character at bitToFlip position in gene, then get the new gene value
	     //does get value, need to convert -1,0,1 
	//	 System.out.print("Old gene: "+ gene.toString() + " Flipping at: " + bitToFlip);
		 int toFlip = Character.getNumericValue(gene.charAt(bitToFlip+1));
		 toFlip ^= 1; 
		 //or just make and return a whole new string? 
		 StringBuilder flipString = new StringBuilder(); 
		 flipString.append(toFlip);
		 gene.setCharAt(bitToFlip+1, flipString.charAt(0)); //need toFlip to be its literal character
		 //bit manipulation to flip bit 
		// System.out.print(" New gene: "+ gene.toString());
		// System.out.println(); 
	 }
	 return directionMap.get(gene.toString()); 
  }
  
  public String findLocation(int a, int b){
	  StringBuilder location = new StringBuilder();
	  location.append(a);
	  location.append(b);
	  return location.toString();
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
      Boolean flipBit; 
      Boolean reactToOthers = (chromosome[7]==1) ? true : false; 
      StringBuilder avoidance = findGene(chromosome[1], chromosome[2], chromosome[3]);
	  StringBuilder attraction = findGene(chromosome[4], chromosome[5], chromosome[6]);
      
      //the random values must be changed so they are based on the parameters of a
      //given creature's chromosome. 
      //for(int i=0;i<numExpectedActions;i++) { //get rid of loop eventually? 
    	  //setting to arbitrary values, though could be used as priority as the action with
    	  //the largest value will be executed.
    	  
    	  //Note: more than one percept could be set!  - use priorities 
  
	 if(percepts[7]==1){ //on red strawberry 
		 actions[9] = 10;   //ALWAYS eat the strawberry regardless of chromosome - should it be?
	 }else if(eat && percepts[6]==1){ //on green strawberry, 
		 actions[9] = 10; 
	 }else if(percepts[0]!=0 || percepts[1]!=0){ //monsters in vicinity  - should be priority! 
	//	 String monsterLocation = findLocation(percepts[0], percepts[1]); //gets the location of monster  		 
		 //Do some computation to find a direction to avoid the monster using avoidance gene. 
		 flipBit = (percepts[0]==1) ? true : false;  
		 moveDirection = findDirection(avoidance, flipBit, percepts[1]);

		// moveDirection = findDirection(avoidance, monsterLocation);
		// System.out.println("Moving in direction " + moveDirection);
		 actions[moveDirection] = 10; //0 to 7 inclusive for movement in some direction 
	
	 }else{ //no monsters in vicinity
		if(reactToOthers && (percepts[2]!=0 || percepts[3]!=0)){
    			//String foodLocation = findLocation(percepts[2], percepts[3]);
    			flipBit = (percepts[2]==1) ? true : false;  
    			moveDirection = findDirection(attraction, flipBit, percepts[3]); //move in some direction in response to creature  
    			actions[moveDirection] = 10; 
    		 
		}
		 if(percepts[4]!=0 || percepts[5]!=0){ //location of food  - reactToFood variable? 
  			 flipBit = (percepts[4]==1) ? true : false;  
		//	 String creatureLocation = findLocation(percepts[4], percepts[5]);
			 moveDirection = findDirection(attraction, flipBit, percepts[5]); //there is food, move towards  
 			 actions[moveDirection] = 10; 
	     }
		 
		 //If everything is 0, do random movements
		 actions[10] = 5; //currently do random movement - change to be based on chromosome  
	 }
    	
      
      
      //implement a computational modeel that computes action vector from the 
      //percept vector. This model should be parametrised by the chromosome,
      //so that when the chromosome values change, the computation changes.
      //
      return actions; //return array of actions. The index of the largest value
      //element in the action array will be taken as the desired action. 
  }
  
  
}