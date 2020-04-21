
//Set appropriate package name

import java.util.ArrayList;
import java.util.Arrays;
import java.util.Iterator;
import java.util.List;

import org.apache.spark.api.java.JavaRDD;
import org.apache.spark.api.java.function.FlatMapFunction;
import org.apache.spark.api.java.function.MapFunction;
import org.apache.spark.sql.Dataset;

import org.apache.spark.sql.Row;
import org.apache.spark.sql.RowFactory;
import org.apache.spark.sql.SparkSession;
import org.apache.spark.sql.catalyst.encoders.ExpressionEncoder;
import org.apache.spark.sql.catalyst.encoders.RowEncoder;
import org.apache.spark.sql.types.DataTypes;
import org.apache.spark.sql.types.StructType;

/**
 * This class uses Dataset APIs of spark to count number of articles per month
 * The year-month is obtained as a dataset of Row
 * */

public class NewsMonthRow {

	public static void main(String[] args) {
		
		//Input dir - should contain all input json files
		String inputPath="/home/mathews/Desktop/Sem 6/DB Lab/Mar 3/newsdata"; //Use absolute paths 
		
		//Ouput dir - this directory will be created by spark. Delete this directory between each run
		String outputPath="/home/mathews/Desktop/Sem 6/DB Lab/Mar 3/output";   //Use absolute paths
		
		StructType structType = new StructType();
		structType = structType.add("year-month", DataTypes.StringType, false); // false => not nullable
	    structType = structType.add("word", DataTypes.StringType, false); // false => not nullable
	    
	    ExpressionEncoder<Row> dateRowEncoder = RowEncoder.apply(structType);
		
		SparkSession sparkSession = SparkSession.builder()
				.appName("Month wise news articles")		//Name of application
				.master("local")								//Run the application on local node
				.config("spark.sql.shuffle.partitions","2")		//Number of partitions
				.getOrCreate();
		
		//Read multi-line JSON from input files to dataset
		Dataset<Row> inputDataset=sparkSession.read().option("multiLine", true).json(inputPath);   
		
		
		// Apply the map function to extract the year-month
		Dataset<Row> yearMonthDataset=inputDataset.flatMap(new FlatMapFunction<Row,Row>(){
			public Iterator<Row> call(Row row) throws Exception {
				// The first 7 characters of date_published gives the year-month 
				String yearMonthPublished=((String)row.getAs("date_published")).substring(0, 7);

                // RowFactory.create() takes 1 or more parameters, and creates a row out of them.
//				Row returnRow=RowFactory.create(yearMonthPublished);
				String line = ((String)row.getAs("article_body"));
				line = line.toLowerCase().replaceAll("[^A-Za-z]", " ");  //Remove all punctuation and convert to lower case
				line = line.replaceAll("( )+", " ");   //Remove all double spaces
				line = line.trim(); 
				List<String> wordList = Arrays.asList(line.split(" ")); //Get words

				
				
				List<Row> returnRow = new ArrayList<>();
				Iterator<String> iterator = wordList.iterator();
				
				for(int a=0; a<wordList.size();++a) {
					returnRow.add(RowFactory.create(yearMonthPublished, wordList.get(a) ));
					
				}
				return returnRow.iterator();	  
			}
			
		}, dateRowEncoder);
		
		
		// Group by the desired column(s) and take count. groupBy() takes 1 or more parameters
		Dataset<Row> count=yearMonthDataset.groupBy("year-month","word").count();  
		
		
		//Outputs the dataset to the standard output
		//count.show();
		
		
		//Ouputs the result to a file
		count.toJavaRDD().saveAsTextFile(outputPath);	
		
	}
	
}
