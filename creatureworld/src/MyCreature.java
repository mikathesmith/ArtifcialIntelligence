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
    private int[] percepts;
    private int[] actions;
    private int[] chromosome; 

  /* Empty constructor - might be a good idea here to put the code that 
   initialises the chromosome to some random state  
  
  Initialisation of chromosome and anything else the creature requires should 
  go in here 
  
   Input: numPercept - number of percepts that creature will be receiving
          numAction - number of action output vector that creature will need
                      to produce on every turn
  */
  public MyCreature(int numPercepts, int numActions) {
      this.numPercepts = numPercepts;
      this.numActions = numActions;  //expected from the agentfunction
      percepts = new int[numPercepts];
      actions = new int[numActions];
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
      
      // This is where your chromosome gives rise to the model that maps
      // percepts to actions.  This function governs your creature's behaviour.
      // You need to figure out what model you want to use, and how you're going
      // to encode its parameters in a chromosome.
      
      // At the moment, the actions are chosen completely at random, ignoring
      // the percepts.  You need to replace this code.
      float actions[] = new float[numExpectedActions];
      for(int i=0;i<numExpectedActions;i++) {
    	  //setting to arbitrary values, though could be used as priority as the action with
    	  //the largest value will be executed 
    	 if(percepts[7]==1){ //on red strawberry 
    		 actions[9] = 10;   //eat the strawberry
    	 }else if(percepts[0]==1 || percepts[1]==1){ //monsters in vicinity 
    		 int moveDirection = rand.nextInt(10);
    		 System.out.println("Avoided!");
    		 actions[moveDirection] = 7; 
    		 
    	 }else{ //no mosters in vicinity
    		 
    		 actions[10] = 5; //currently don't move
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