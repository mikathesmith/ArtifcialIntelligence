import cosc343.assig2.Creature;
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
      
      //chromosome encoding goes here 
  }
  
  /* This function must be overridden by MyCreature, because it implements
     the AgentFunction which controls creature behavoiur.  This behaviour
     should be governed by a model (that you need to come up with) that is
     parameterise by the chromosome.  
  
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
      Boolean eat; 
      for(int i=0;i<numExpectedActions;i++) {
    	  //setting to arbitrary values, though could be used as priority as the action with
    	  //the largest value will be executed.
    	  
    	  //Note: more than one percept could be set! 
    	  
    	  //use a choose random action function. 
    	 if(percepts[7]==1){ //on red strawberry 
    		 actions[9] = 10;   //ALWAYS eat the strawberry
    	 }else if(percepts[6]==1){ //on green strawberry, 
    		 eat = rand.nextBoolean(); //randomly, either eat or dont 
    		 
    		 if(eat){ //eventually want this to be based on energy! 
    			 actions[9] = 10; 
    			// System.out.println("Chose to eat");
    		 }else{
    			 //System.out.println("Ew gross no thanks");
    		 }
    	 }else if(percepts[0]==1){ //monsters in vicinity  - should be priority! 
    		 moveDirection = rand.nextInt(10); 
    		// System.out.println("Avoided! direction 1" );
    		 actions[moveDirection] = 10; 
    	 }else if(percepts[1]==1){ //monsters in other vicinity 
    		 moveDirection = rand.nextInt(10); 
    		// System.out.println("Avoided! direction 2" );
    		 actions[moveDirection] = 10; 
    	 }else{ //no mosters in vicinity
    		 if(percepts[4]==1){
    			moveDirection = rand.nextInt(7); //there is food, move towards  
    			actions[moveDirection] = 10; 
    		 }
    		 if(percepts[5]==1){
    			 moveDirection = rand.nextInt(7); //there is food, move towards  
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