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
* @version 5.0
* @since   2017-04-05 
*/
public class MyCreature extends Creature {
	Random rand = new Random();
	
	//Initialising chromosome information 
    private final int numPercepts;
    private final int numActions;
    static int cID=0;  
    int creatureID=0;
    public int[] chromosome; 
    
    //Map containing gene encoding to action 
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
    

  /* 
  Initialisation of chromosome; its unique creature ID and randomly setting its 
  binary chromosome 
  
   Input: numPercept - number of percepts that creature will be receiving
          numAction - number of action output vector that creature will need
                      to produce on every turn
  */
  public MyCreature(int numPercepts, int numActions) { 
      this.numPercepts = numPercepts;
      this.numActions = numActions;  //expected from the agentfunction
      cID++; 
      creatureID = cID; //way to uniquelly identify a creature 
      chromosome = new int[11];
      //Index 0 = eat green stawberry or not
      //Index 1, 2, 3 = avoidance behaviour if x1, opposite behaviour if x2, or if both? 
      //Index 4, 5, 6 = attraction behaviour 
      //Index 7 = follow other creatures or not
      //Index 8 = always random behaviour  ??
      //Index 9, 10, 11 = default behaviour 
      for(int i=0; i < chromosome.length;i++){
    	  chromosome[i] = rand.nextInt(2); //initialises genes to either 1 or 0 
      }
  }
  

  /*
   Constructs the gene for movement given three integer values from the chromosome. 
   
   	Input: a, b, c = integers that each make up a bit of the gene 
   */
  public StringBuilder constructGene(int a, int b, int c){
	  StringBuilder gene = new StringBuilder();
	  gene.append(a);
	  gene.append(b);
	  gene.append(c);
	  return gene;
  }
  
  /*
   * This method takes in a given gene encoding movement behaviour, modifies it according
   * to the location of the monster/creature/food, and returns the associated action 
   * according to the direction map. 
   * 
   * Input: gene	  :  gene encoding movement behaviour
   * 		flip	  :  whether or not to flip a bit 
   * 		bitToFlip :  -1, 0 or 1. Indicates position of bit to flip. 
   */
  public int findDirection(StringBuilder gene, Boolean flip, int bitToFlip){ //have a bool value opposite? 
	  //If we are need to flip a bit 
	  if(flip){
		 //else replace character at bitToFlip position in gene, then get the new gene value
	     //Find the value of the bit we need to flip in position bitToFlip+1 and flip it (0 to 1, 1 to 0)
		 int toFlip = Character.getNumericValue(gene.charAt(bitToFlip+1));
		 toFlip ^= 1; 
		 
		 //This should just be a String not a string builder! 
		 StringBuilder flipString = new StringBuilder(); 
		 flipString.append(toFlip);
		 
		 //Replace the old bit with the modified bit 
		 gene.setCharAt(bitToFlip+1, flipString.charAt(0));
	 }
	  //Return the associated action of the new gene
	 return directionMap.get(gene.toString()); 
  }
  
  
  /*
   * Remove? 
   */
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

	  //Intialise informaion  
      float actions[] = new float[numExpectedActions];
      int moveDirection;
      Boolean eat= (chromosome[0]==1) ? true : false;
      Boolean flipBit; 
      Boolean reactToOthers = (chromosome[7]==1) ? true : false; 
      StringBuilder avoidance = constructGene(chromosome[1], chromosome[2], chromosome[3]);
	  StringBuilder attraction = constructGene(chromosome[4], chromosome[5], chromosome[6]);
	  StringBuilder defaultBehaviour = constructGene(chromosome[8], chromosome[9], chromosome[10]);
	  final int ACTIONEXECUTED = 10;
	  
      
      //the random values must be changed so they are based on the parameters of a
      //given creature's chromosome.
    	  //setting to arbitrary values, though could be used as priority as the action with
    	  //the largest value will be executed.
    	  
    	  //Note: more than one percept could be set!  - use priorities 
  
	 if(percepts[7]==1){ //on red strawberry 
		 actions[9] = ACTIONEXECUTED;   //ALWAYS eat the strawberry regardless of chromosome - should it be?
	 }else if(eat && percepts[6]==1){ //on green strawberry, 
		 actions[9] = ACTIONEXECUTED; 
	 }else if(percepts[0]!=0 || percepts[1]!=0){ //monsters in vicinity  - should be priority! 
	//	 String monsterLocation = findLocation(percepts[0], percepts[1]); //gets the location of monster  		 
		 //Do some computation to find a direction to avoid the monster using avoidance gene. 
	//	 if(percepts[0]==-1){
	//		actions[10] = ACTIONEXECUTED;  //do random movement - this means we'll never react if monster is in a certain row/column! 
		//	System.out.println("So random")
//		 }else{
			 flipBit = (percepts[0]==1) ? true : false; 
			 moveDirection = findDirection(avoidance, flipBit, percepts[1]);
			 actions[moveDirection] = ACTIONEXECUTED;
	//	 }
		// moveDirection = findDirection(avoidance, monsterLocation);
		// System.out.println("Moving in direction " + moveDirection);
		  //0 to 7 inclusive for movement in some direction 
	
	 }else{ //no monsters in vicinity
		if(reactToOthers && (percepts[2]!=0 || percepts[3]!=0)){
    			//String foodLocation = findLocation(percepts[2], percepts[3]);
    			flipBit = (percepts[2]==1) ? true : false;  
    			moveDirection = findDirection(attraction, flipBit, percepts[3]); //move in some direction in response to creature  
    			actions[moveDirection] = ACTIONEXECUTED; 
    		 
		}
		
		//If the creature senses there is food - use a reactToFood variable?  
		 if(percepts[4]!=0 || percepts[5]!=0){ 
  			 flipBit = (percepts[4]==1) ? true : false;  
		//	 String creatureLocation = findLocation(percepts[4], percepts[5]);
			 moveDirection = findDirection(attraction, flipBit, percepts[5]);   
 			 actions[moveDirection] = ACTIONEXECUTED; 
	     }
		 
		 //If everything is 0, execute the default behaviour at the lowest priority 
		 moveDirection= directionMap.get(defaultBehaviour.toString());
		 actions[moveDirection] = ACTIONEXECUTED/2; //currently do random movement - change to be based on chromosome??    
	 }
	 
	//return array of actions. The index of the largest value will be the action executed 
      return actions; 
  }
}