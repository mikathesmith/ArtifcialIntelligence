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
* @version 6.0
* @since   2017-14-05 
*/

public class MyWorld extends World {
	
  private final int _numTurns = 85;
  private final int _numGenerations = 500;
  
  //The name of the file to write the fitness data to to produce a graph from 
  private static final String FILENAME = "fitnessdata.txt";
  public int genIndex = 1; //Keeps the index of the generations. 
  public static FileWriter fw = null;
  public static BufferedWriter bw = null; 
  public Random rand = new Random(); 
  public static final double MUTATIONRATE = 0.002; 
  public static final boolean elitism = true;  
  
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
     int windowWidth =  1500;
     int windowHeight = 1200;
     boolean repeatableMode = false;
     int perceptFormat = 1;     
   
     MyWorld sim = new MyWorld(gridSize, windowWidth, windowHeight, repeatableMode, perceptFormat);  
  }
  

  /* The MyWorld class must override this function, which is
     used to fetch a population of creatures at the beginning of the
     first simulation.  This is the place where you need to  generate
     a set of creatures with random behaviours.
  
     Input: numCreatures - how many creatures the world is expecting

     Returns: An array of MyCreature objects   
  */  
  @Override
  public MyCreature[] firstGeneration(int numCreatures) {

    int numPercepts = this.expectedNumberofPercepts();
    int numActions = this.expectedNumberofActions();
      
    //Create an array of MyCreature of size numCreatures. 
    MyCreature[] population = new MyCreature[numCreatures];
    for(int i=0;i<numCreatures;i++) {
        population[i] = new MyCreature(numPercepts, numActions);
    }
    return population;
  }
  
  /*
   * Calulates the fitness of a given individual. 
   * 
   * Input: 	energy  : energy of creature at death or end of simulation
   * 			dead 	: whether the creature survived or not
   * 
   * Return: 	fitness : double value indicating the creature's fitness. 
   */
  public double calculateFitness(int energy, Boolean dead){
	  if(!dead) return 15; //If they survived, give them maximum value 
	  double fitness = (double)energy/10; //if not, set their fitness as their energy from 1 to 10 
	  return fitness;
  }
  
  /*
  This method finds the creature with the maximal fitnesses to be the parent of
  a fit offspring. It uses tournament selection to choose a random subset of 
  individuals to find the maximum of in order to give all creatures a chance to 
  have their alleles passed to the new generation. 
   
  	Input  : 	creatureFitnessMap :  contains all creatures from the old population
  		   		and their associated fitness values. 
  	Return : 	fittest 			: the creature with the maximum fitness value
  									  to be the parent
  *
  */
  public MyCreature parentSelection(HashMap<MyCreature, Double> creatureFitnessMap){

	  double maxFitness = 0;
	  ArrayList<MyCreature> fitCandidates = new ArrayList<MyCreature>();  
	  int subsetSize = 5; //This is the number of individuals we will randomly select and choose the best of 
	  int minID = Integer.MAX_VALUE;
	  int maxID = Integer.MIN_VALUE;
	  //Loop through to get min and max values to find range
	  for(Map.Entry<MyCreature, Double> entry : creatureFitnessMap.entrySet()){
		  int currentID = entry.getKey().creatureID; 
		  if(currentID > maxID){
			  maxID = currentID;
		  }
		  if(currentID < minID){
			  minID = currentID; 
		  }
	  }  
	  
	  //Get 5 random inidividuals to add to 
	  while(fitCandidates.size() < subsetSize){
		  int cand = minID + rand.nextInt(maxID - minID + 1); //Random index in range of creature ID's 
		  
		  for(Map.Entry<MyCreature, Double> entry : creatureFitnessMap.entrySet()){
			  MyCreature creat = entry.getKey(); 
			  if(creat.creatureID == cand){ 
				  fitCandidates.add(creat);
				  break; 
			  }
		  }
	  }
	  
	  //Iterate through our subset to find the one with the maximum fitness
	  MyCreature fittest = null; 
	  for(MyCreature creat : fitCandidates){
		  double currentFitness = creatureFitnessMap.get(creat);
		  if(fittest==null) fittest = creat; //ensure we aren't returning a null 
	
		  if(currentFitness > maxFitness){
			  maxFitness = currentFitness;
			  fittest = creat; 
		  }
	  }
	  //Remove this statement if we would like to enable choosing the same parent twice
	  creatureFitnessMap.remove(fittest); 
	  
	  return fittest;   
  }
  
  /*
   * Takes two chromosomes and returns a new one by crossing them over.
   * 
   * Input :   p1, p2    : MyCreature parents with unique ID's whose chromosomes
   * 					   will be crossed over to create a new offspring chromsome. 
   * 
   * Return:   offspring : New MyCreature with a unique ID and a hybrid chromosome
   * 					   made from half of p1's chromosome and the other half of 
   * 					   p2's chromosome, at a given crossover index. 
   * 
   */
  public MyCreature crossOver(MyCreature p1, MyCreature p2){
	  //Create a child creature
	  int numPercepts = this.expectedNumberofPercepts();
	  int numActions = this.expectedNumberofActions();
	  MyCreature offspring = new MyCreature(numPercepts, numActions);
	  
	  //Find the crossover point; either between avoidance and attraction
	  //behaviour, or attraction and default behaviour so as to not 
	  //seperate gene segments 
	  int choice = rand.nextInt(2); //0 or 1
	  int crossoverIndex = (choice == 0) ? 3 : 6; 
	  
	  //Replace offspring's random chromosome with half of p1 and half of p2 at the crossover point. 
	  for(int i = 0; i <= crossoverIndex; i++){
		  offspring.chromosome[i] = p1.chromosome[i];
	  }
	  for(int i = crossoverIndex + 1; i < p1.chromosome.length; i++){
		  offspring.chromosome[i] = p2.chromosome[i];
	  }
	  
	  //With some probability, call mutation 
	  double probMutate = rand.nextDouble();
	  if(probMutate < MUTATIONRATE){ 
		  offspring = mutation(offspring);
	  }
	  
	  return offspring; 
  }
  
  /*Mutates with some random probability by flipping a random bit.
   * 
   * Input 	: child : the new offspring creature
   * 
   * Return : child : the offspring with its modified chromosome 
   * 				  with one bit flipped at random. 
   * 
   */
  public MyCreature mutation(MyCreature child){
	  int flipBitIndex = rand.nextInt(12); 
	  int bitToFlip = child.chromosome[flipBitIndex]; 
	  bitToFlip ^= 1;  //Inverts bit 
	  child.chromosome[flipBitIndex] = bitToFlip;
	  return child;   
  }
  
  /*
   * Print contents of chromosome for debugging to ensure crossover
   * and mutation are occuring
   * 
   * Input: parent1, parent2, offspring: creatures whose chromosomes to output. 
   * 
   */
  public void printChromosomeInformation(MyCreature parent1, MyCreature parent2, MyCreature offspring){
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
  
  /* The MyWorld class must override this function, which is
     used to fetch the next generation of the creatures.  This World will
     provide you with the old_generation of creatures, from which you can
     extract information relating to how they did in the previous simulation
     and use them as parents for the new generation.
  
     Input: old_population_btc : the generation of old creatures before type casting. 
            numCreatures 	   : the number of elements in the old array                      
                            
	  Returns: An array of MyCreature objects which will form the new population. 
  */  
  @Override
  public MyCreature[] nextGeneration(Creature[] old_population_btc, int numCreatures) {
  
     MyCreature[] old_population = (MyCreature[]) old_population_btc;
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
     avgLifeTime /= (float) numCreatures;
     avgFitness /= (float) numCreatures; 
     StringBuilder stats = new StringBuilder(); 
     stats.append("Simulation stats:\n");
     stats.append("  Survivors    : " + nSurvivors + " out of " + numCreatures+"\n");
     stats.append("  Avg life time: " + avgLifeTime + " turns\n");
     stats.append("  Avg fitness: " + avgFitness +"\n");
     System.out.println(stats);
      
    //Writing data to text file to plot on graph using FitnessLineChart 
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
     int elitismIndex = (int) (numCreatures * (9.0/10.0));
     int numElite = (int) (numCreatures * (1.0/10.0));
     
     //Create an Arraylist of elites who will not undergo crossover. 
     ArrayList<MyCreature> eliteList = new ArrayList<MyCreature>();
  
     for(int i=0; i < elitismIndex; i++) {
    	 parent1 = parentSelection(creatureFitnessMap); 
    	 if(eliteList.size() <= numElite){
    		 eliteList.add(parent1);
    	 }
         parent2 = parentSelection(creatureFitnessMap);
         offspring = crossOver(parent1, parent2);
    //     printChromosomeInformation(parent1, parent2, offspring); //Print for debugging. 
         
         //Add new offspring into new population and add it to the map of creatures. 
         new_population[i] = offspring;    
         double fitness = calculateFitness(100, false);  //Don't know fitness so give maximum. 
         creatureFitnessMap.put(offspring, fitness);
     }

     //Elitism - does not exceed 10% of the total new population in order to maintain diversity.
     int count = 0; 
    for(int i= elitismIndex; i < numCreatures; i++) {
         new_population[i] = eliteList.get(count);
         count++; 
     }

     // Return new population of creatures. Same number as old population. 
     return new_population;
  }
  
}