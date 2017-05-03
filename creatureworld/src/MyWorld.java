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
* @version 3.0
* @since   2017-04-05 
*/



public class MyWorld extends World {
	
 
  /* Here you can specify the number of turns in each simulation
   * and the number of generations that the genetic algorithm will 
   * execute.
  */
  private final int _numTurns = 100;
  private final int _numGenerations = 1000;
  private static final String FILENAME = "fitnessdata.txt";
 // public float[] fitnessData = new float[_numGenerations];
  public int dataIndex = 1;
  public static FileWriter fw = null;
  public static BufferedWriter bw = null; 
  /* Constructor.  
   
     Input: griSize - the size of the world
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
     // Here you can specify the grid size, window size and whether torun
     // in repeatable mode or not
     int gridSize = 24;
     int windowWidth =  1600;
     int windowHeight = 900;
     boolean repeatableMode = false;
     
 
    
      /* Here you can specify percept format to use - there are three to
         chose from: 1, 2, 3.  Refer to the Assignment2 instructions for
         explanation of the three percept formats.
      */
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
  
  public int calculateFitness(int energy, Boolean dead){
	  if(!dead) return 10; //If they survived, give them maximum value 
	  return energy/10; //if not, set their fitness as their energy from 1 to 10 
  }
  
  
  //pass in map of calculated fitnesses to creature. 
  //Find two creatures with maximal fitnesses and breed
  //need to update so that we are using roulette wheel or tournament selection!  
  public MyCreature parentSelection(HashMap<MyCreature, Integer> creatureFitnessMap){
	/*Testing its entering the hashmap   
	  for(Map.Entry<MyCreature, Integer> entry : creatureFitnessMap.entrySet()){
		  System.out.println(entry.getKey().getEnergy() + " " + entry.getValue());
	  }
	  */
	  int max = 0; 
	  ArrayList<MyCreature> fitCandidates = new ArrayList<MyCreature>();
	  for(Map.Entry<MyCreature, Integer> entry : creatureFitnessMap.entrySet()){
		  int currentFitness = entry.getValue(); 
		  if(currentFitness >= max){
			  if(currentFitness > max){
				  max = currentFitness;
				  fitCandidates.clear(); 
			  }
			  fitCandidates.add(entry.getKey());
		  }
	  }
	//  System.out.println("Max is "+ max);
	  int candIndex = rand.nextInt(fitCandidates.size());
	  MyCreature candidate = fitCandidates.get(candIndex);
	  creatureFitnessMap.remove(candidate); //does this alter the global hashmap? 
	  return candidate;  
  }
  
  //Takes two chromosomes and returns a new one by crossing them over 
  public MyCreature crossOver(MyCreature p1, MyCreature p2){
	  //set crossover point. 
	  int numPercepts = this.expectedNumberofPercepts();
	  int numActions = this.expectedNumberofActions();
	  
	  int crossoverIndex = p1.chromosome.length/2; //make this the mid point, number of genes/2  
	  //find out how to access values in chromosome; 
	 // MyCreature offspring;
	  int[] offspringChromosome = new int[p1.chromosome.length];
	  for(int i=0; i < crossoverIndex; i++){
		  offspringChromosome[i] = p1.chromosome[i];
	  }
	  for(int i= crossoverIndex; i < p1.chromosome.length ;i++){
		  offspringChromosome[i] = p2.chromosome[i];
	  }
	//  System.out.println("Crossover point: "+ crossoverIndex);
	  
	/*  System.out.print("Parent 1:  ");
	  for(int i : p1.chromosome){
		  System.out.print(i);
	  }
	  System.out.println();
	  
	  System.out.print("Parent 2:  ");
	  for(int i : p2.chromosome){
		  System.out.print(i);
	  }
	  System.out.println();
	  
	  System.out.print("Offspring: ");
	  for(int i : offspringChromosome){
		  System.out.print(i);
	  }
	  System.out.println();*/ 

	  //append index 0 to crossoverIndex to offSpringChromosome. 
	  
	  //append crossoverIndex to chromosome.length-1 to offSpringChromosome
	  
	  MyCreature offspring = new MyCreature(numPercepts, numActions);
	  offspring.chromosome = offspringChromosome;
	  return offspring; 
	  //return null;
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
    // Typcast old_population of Creatures to array of MyCreatures
     MyCreature[] old_population = (MyCreature[]) old_population_btc;
     // Create a new array for the new population
     MyCreature[] new_population = new MyCreature[numCreatures];
   //  int[] fitnesses = new int[numCreatures];
     HashMap<MyCreature, Integer> creatureFitnessMap = new HashMap<MyCreature, Integer>(); 
     

     // Here is how you can get information about old creatures and how
     // well they did in the simulation
     //query the state of every creature by executing various methods that 
     //MyCreature inherits from its parent class. 
     //energy is only 0 when creature starves to death. Energy value will be 
     //taken at the time the creature ran into a monster. 
     
     //use this info to compute a fitness score for every creature. This should
     //guide the GA in selection of parents for the next generation. 
     float avgLifeTime=0f;
     int nSurvivors = 0;
   //  int fitCount = 0; 
     float avgFitness =0f; 
     for(MyCreature creature : old_population) {
        // The energy of the creature.  This is zero if creature starved to
        // death, non-negative otherwise.  If this number is zero, but the 
        // creature is dead, then this number gives the enrgy of the creature
        // at the time of death.
        int energy = creature.getEnergy();
      //  System.out.println("Creature's energy"+energy);

        // This query can tell you if the creature died during simulation
        // or not.  
        boolean dead = creature.isDead();

        int fitness = calculateFitness(energy, dead); 
      //  fitnesses[fitCount] = fitness;  //store in hashtable due to keyvalue pair 
        creatureFitnessMap.put(creature, fitness); 
      //  fitCount++; 
        //System.out.println(fitness);
        
        avgFitness += (float)fitness; 
        
        if(dead) {
           // If the creature died during simulation, you can determine
           // its time of death (in turns)
           int timeOfDeath = creature.timeOfDeath();
           avgLifeTime += (float) timeOfDeath;
        } else {
           nSurvivors += 1;
           avgLifeTime += (float) _numTurns;
        }
     }
     //move to below for loop, add offspring to new_population in ith position  
     MyCreature parent1 = parentSelection(creatureFitnessMap); 
     MyCreature parent2 = parentSelection(creatureFitnessMap);
   //  System.out.println("Parent 1: " + parent1.parentID + " Energy at death: " + parent1.getEnergy());
     //System.out.println("Parent 2: " + parent2.parentID + " Energy at death: " + parent2.getEnergy());
     
     MyCreature offspring = crossOver(parent1, parent2);
  //   System.out.println("Offspring: " + offspring.parentID + "Genotype: " + offspring.chromosome);  
     System.out.print("Parent 1:  " + parent1.creatureID + " Genotype: ");
	  for(int i : parent1.chromosome){
		  System.out.print(i);
	  }
	  System.out.println();
	  
	  System.out.print("Parent 2:  " + parent2.creatureID + " Genotype: ");
	  for(int i : parent2.chromosome){
		  System.out.print(i);
	  }
	  System.out.println();
	  
	  System.out.print("Offspring: " + offspring.creatureID + " Genotype: ");
	  for(int i : offspring.chromosome){
		  System.out.print(i);
	  }
	  System.out.println();
     //crossover, add random mutation to the chromosome. 
     //print average fitness of all creatures and plot this over generations. 

     // Right now the information is used to print some stats...but you should
     // use this information to access creatures fitness.  It's up to you how
     // you define your fitness function.  You should add a print out or
     // some visual display of average fitness over generations.
     avgLifeTime /= (float) numCreatures;
     avgFitness /= (float) numCreatures; 
     System.out.println("Simulation stats:");
     System.out.println("  Survivors    : " + nSurvivors + " out of " + numCreatures);
     System.out.println("  Avg life time: " + avgLifeTime + " turns");
     System.out.println("  Avg fitness: " + avgFitness);
     
    // fitnessData[dataIndex] = avgFitness;
     
     try{
    	 fw = new FileWriter(FILENAME, true);
         bw = new BufferedWriter(fw);
    	 bw.write(dataIndex + " " + Float.toString(avgFitness)+"\n");
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
     dataIndex++; 
     

     
     // Having some way of measuring the fitness, you should implement a proper
     // parent selection method here and create a set of new creatures.  You need
     // to create numCreatures of the new creatures.  If you'd like to have
     // some elitism, you can use old creatures in the next generation.  This
     // example code uses all the creatures from the old generation in the
     // new generation.
     for(int i=0;i<numCreatures; i++) {
        new_population[i] = old_population[i];
     }
     

     // Return new population of cratures. same number as old population. 
     return new_population;
  }
  
}