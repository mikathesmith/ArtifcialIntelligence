import cosc343.assig2.World;
import cosc343.assig2.Creature;
import java.util.*;
import java.io.*;


/**
* The MyWorld extends the cosc343 assignment 2 World.  Here you can set 
* some variables that control the simulations and override functions that
* generate populations of creatures that the World requires for its
* simulations.
* 
* Implement fitness evaluation and creation of new generations of creatures 
*
* @author  Mika Smith
* @version 5.0
* @since   2017-04-05 
*/

public class MyWorld extends World {
	
 
  /* Here you can specify the number of turns in each simulation
   * and the number of generations that the genetic algorithm will 
   * execute.
  */
  private final int _numTurns = 85;
  private final int _numGenerations = 1500;
  
  //The name of the file to write the fitness data to to produce a graph from 
  private static final String FILENAME = "fitnessdata.txt";
  public int genIndex = 1; //keeps the index of the generations. 
  public static FileWriter fw = null;
  public static BufferedWriter bw = null; 
  public Random rand = new Random(); 
  
  /* Constructor.  
   
     Input: gridSize - the size of the world
            windowWidth - the width (in pixels) of the visualisation window
            windowHeight - the height (in pixels) of the visualisation window
            repeatableMode - if set to true, every simulation in each
                             generation will start from the same state
            perceptFormat - format of the percepts to use: choice of 1, 2, or 3
  */
  public MyWorld(int gridSize, int windowWidth, int windowHeight, boolean repeatableMode, int perceptFormat) {   
      // Initialise the parent class - don't remove this
      super(gridSize, windowWidth,  windowHeight, repeatableMode, perceptFormat);
      // Set the number of turns and generations
      this.setNumTurns(_numTurns);
      this.setNumGenerations(_numGenerations); 
  }
 
  /* The main function for the MyWorld application

  */
  public static void main(String[] args) {
     int gridSize = 36;
     int windowWidth =  1800;
     int windowHeight = 1200;
     boolean repeatableMode = false;
     int perceptFormat = 1;     
     
     // Instantiate MyWorld object.  The rest of the application is driven
     // from the window that will be displayed.
     MyWorld sim = new MyWorld(gridSize, windowWidth, windowHeight, repeatableMode, perceptFormat);
     
  }
  

  /* The MyWorld class must override this function, which is
     used to fetch a population of creatures at the beginning of the
     first simulation.  This is the place where you need to  generate
     a set of creatures with random behaviours.
  
     Input: numCreatures - this variable will tell you how many creatures
                           the world is expecting
                            
     Returns: An array of MyCreature objects - the World will expect numCreatures
              elements in that array     
  */  
  @Override
  public MyCreature[] firstGeneration(int numCreatures) {

    int numPercepts = this.expectedNumberofPercepts();
    int numActions = this.expectedNumberofActions();
      
    // This is just an example code.  You may replace this code with
    // your own that initialises an array of size numCreatures and creates
    // a population of your creatures
    
    //create an array of MyCreature of size numCreatures. 
    MyCreature[] population = new MyCreature[numCreatures];
    for(int i=0;i<numCreatures;i++) {
        population[i] = new MyCreature(numPercepts, numActions);
        //initialise the creature's chromosome to some random value. 
        //creatures do not behave intelligently at the beginning of the
        //evolution. they need to learn their behaviour through the GA
    }
    return population;
  }
  
  public double calculateFitness(int energy, Boolean dead){
	  if(!dead) return 15; //If they survived, give them maximum value 
	  double fitness = (double)energy/10; //if not, set their fitness as their energy from 1 to 10 
	//  System.out.println(energy + " " + fitness);
	  return fitness;
  }
  
  //pass in map of calculated fitnesses to creature. 
  //Find two creatures with maximal fitnesses and breed
  //need to update so that we are using roulette wheel or tournament selection!  
  public MyCreature parentSelection(HashMap<MyCreature, Double> creatureFitnessMap){
	/*Testing its entering the hashmap   
	  for(Map.Entry<MyCreature, Integer> entry : creatureFitnessMap.entrySet()){
		  System.out.println(entry.getKey().getEnergy() + " " + entry.getValue());
	  }
	  */
	  
	  //Is there a better way to do this!! Takes in the ENTIRE map of creatures and their fitnesses. 
	  
	  //Choose a subset to iterate!  creatureFitnessMap.size()/4
	  double max = 0;
	  ArrayList<MyCreature> fitCandidates = new ArrayList<MyCreature>();
	  
	  //starts at 19, goes to 0?? 
	  int subsetSize = creatureFitnessMap.size()/4; 
	//  System.out.println("Subset Size: "+subsetSize);
	  for(int i = 0; i < subsetSize; i++){
		  int cand = rand.nextInt(creatureFitnessMap.size()); 
		  fitCandidates.add(creatureFitnessMap.get()); //get in position cand?? 
	  }
	  
	/*  for(Map.Entry<MyCreature, Double> entry : creatureFitnessMap.entrySet()){
		  
		  double currentFitness = entry.getValue(); 
		  if(currentFitness >= max){
			  if(currentFitness > max){
				  max = currentFitness;
				  fitCandidates.clear(); 
			  }
			  fitCandidates.add(entry.getKey());
		  }
	  }*/ 
	  int candIndex = rand.nextInt(fitCandidates.size()); 
	  MyCreature candidate = fitCandidates.get(candIndex);
	  
	  //Is this step necessary? Can we choose the same parent twice?  While parentID == old parent ID, do again? 
	 // creatureFitnessMap.remove(candidate); 
	  return candidate;  
  }
  
  //Takes two chromosomes and returns a new one by crossing them over 
  public MyCreature crossOver(MyCreature p1, MyCreature p2){
	  //set crossover point. 
	  int numPercepts = this.expectedNumberofPercepts();
	  int numActions = this.expectedNumberofActions();
	  
	  //This is the midpoint of the chromosome. Should this be a random point? 
	  int crossoverIndex = p1.chromosome.length/2;
	 // System.out.println(crossoverIndex);
	  MyCreature offspring = new MyCreature(numPercepts, numActions);
	  
	  //Replace offspring's random chromosome with half of p1 and half of p2 at the crossover point. 
	  for(int i=0; i <= crossoverIndex; i++){
		  offspring.chromosome[i] = p1.chromosome[i];
	  }
	  for(int i= crossoverIndex + 1; i < p1.chromosome.length ;i++){
		  offspring.chromosome[i] = p2.chromosome[i];
	  }
	  
	  //With some probability, call mutation 
	  double probMutate = rand.nextDouble();
	  //System.out.println(probMutate);
	  if(probMutate < 0.002){ //Change this prob? 
		  for(int x : offspring.chromosome){
	   		  System.out.print(x);
	   	  }
		  offspring = mutation(offspring);
		  System.out.println("I've been mutated!");
		  for(int x : offspring.chromosome){
	   		  System.out.print(x);
	   	  }
	  }
	  return offspring; 
  }
  
  //Mutates with some random probability by flipping a random bit
  public MyCreature mutation(MyCreature child){
	  int flipBitIndex = rand.nextInt(8); //make sure we're not missing one! 
	  int bitToFlip = child.chromosome[flipBitIndex]; 
	  bitToFlip ^= 1;  //Inverts bit 
	  child.chromosome[flipBitIndex] = bitToFlip;
	  return child;   
  }
  
  /* The MyWorld class must override this function, which is
     used to fetch the next generation of the creatures.  This World will
     provide you with the old_generation of creatures, from which you can
     extract information relating to how they did in the previous simulation...
     and use them as parents for the new generation.
  
     Input: old_population_btc - the generation of old creatures before type casting. 
                              The World doesn't know about MyCreature type, only
                              its parent type Creature, so you will have to
                              typecast to MyCreatures.  These creatures 
                              have been simulated over and their state
                              can be queried to compute their fitness
            numCreatures - the number of elements in the old_population_btc
                           array
                        
                            
  Returns: An array of MyCreature objects - the World will expect numCreatures
           elements in that array.  This is the new population that will be
           use for the next simulation.  
  */  
  @Override //called in the evolution phase. 
  public MyCreature[] nextGeneration(Creature[] old_population_btc, int numCreatures) {
    // Typcast old_population of Creatures to array of MyCreatures - is this always the ORIGINAL population?
     MyCreature[] old_population = (MyCreature[]) old_population_btc;
     // Create a new array for the new population
     MyCreature[] new_population = new MyCreature[numCreatures];
     
     HashMap<MyCreature,Double> creatureFitnessMap = new HashMap<MyCreature, Double>(); 

     float avgLifeTime=0f;
     int nSurvivors = 0;
     float avgFitness =0f; 
     
     for(MyCreature creature : old_population) {
        int energy = creature.getEnergy();
        boolean dead = creature.isDead();
        double fitness = calculateFitness(energy, dead); 
        creatureFitnessMap.put(creature, fitness); 
        avgFitness += (float)fitness; 
        
        if(dead) {
           int timeOfDeath = creature.timeOfDeath();
           avgLifeTime += (float) timeOfDeath;
        } else {
           nSurvivors += 1;
           avgLifeTime += (float) _numTurns;
        }
     }
     //crossover, add random mutation to the chromosome. 
     //print average fitness of all creatures and plot this over generations. 

     avgLifeTime /= (float) numCreatures;
     avgFitness /= (float) numCreatures; 
     System.out.println("Simulation stats:");
     System.out.println("  Survivors    : " + nSurvivors + " out of " + numCreatures);
     System.out.println("  Avg life time: " + avgLifeTime + " turns");
     System.out.println("  Avg fitness: " + avgFitness);
     
    
    //Writing data to text file to plot on graph using FitnessLineChart 
     //Do I have to open and close each time? 
     try{
    	 fw = new FileWriter(FILENAME, true);
         bw = new BufferedWriter(fw);
    	 bw.write(genIndex + " " + Float.toString(avgFitness)+" "+ Float.toString(avgLifeTime) +"\n");
     }catch(IOException e){
    	 e.printStackTrace();
     }finally{
    	 try{
    		 if (bw != null)
				bw.close();

			if (fw != null)
				fw.close();

		}catch (IOException e) {
			e.printStackTrace();
		}
     }
     genIndex++; 
     
     MyCreature parent1, parent2, offspring;
 
     for(int i=0;i<numCreatures/2; i++) {
    	 
    	 parent1 = parentSelection(creatureFitnessMap); 
         parent2 = parentSelection(creatureFitnessMap);
         
         offspring = crossOver(parent1, parent2);
         new_population[i] = offspring; 
         
         System.out.print("Parent 1:  " + parent1.creatureID + " Genotype: ");
	   	  for(int x : parent1.chromosome){
	   		  System.out.print(x);
	   	  }
	   	  System.out.println();
	   	  
	   	  System.out.print("Parent 2:  " + parent2.creatureID + " Genotype: ");
	   	  for(int x : parent2.chromosome){
	   		  System.out.print(x);
	   	  }
	   	  System.out.println();
	   	  
	   	  System.out.print("Offspring: " + offspring.creatureID + " Genotype: ");
	   	  for(int x : offspring.chromosome){
	   		  System.out.print(x);
	   	  }
	   	  System.out.println();
         
     }
     
     //Elitism! - keep half of old population - change to subset n 
     //should not exceed 10% of the total population to maintian diversity
     //5% may be direct part of next generation and remaining should go through crossover
     
     for(int i=numCreatures/2; i < numCreatures; i++) {
         new_population[i] = old_population[i];
     }

     // Return new population of cratures. same number as old population. 
     return new_population;
  }
  
}