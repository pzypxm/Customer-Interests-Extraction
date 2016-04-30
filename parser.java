package parser;
import java.util.List;
import edu.stanford.nlp.process.DocumentPreprocessor;
import edu.stanford.nlp.ling.HasWord;
import edu.stanford.nlp.trees.*;
import edu.stanford.nlp.parser.lexparser.LexicalizedParser;
import java.io.*;
import java.util.*;

class parser {

    public static void GetNouns(Tree parse, String output_file)
    {
        try {
            String filename= output_file;
            FileWriter fw = new FileWriter(filename,true); //the true will append the new data

            List<Tree> phraseList = new ArrayList<Tree>();
            for (Tree subtree : parse) {

                if (subtree.label().value().equals("NN") || subtree.label().value().equals("NNP") || subtree.label().value().equals("NNS") || subtree.label().value().equals("NNPS")) {
                    phraseList.add(subtree);
                    fw.write(subtree.getLeaves().toArray()[0].toString() + "\n");
                }
            }
            fw.close();
        }
        catch(IOException e1) {
            System.out.println("Error during reading/writing");
        }
    }

    public static void demoDP(LexicalizedParser lp, String input, String output) {
        try {
            PrintWriter writer = new PrintWriter(output, "UTF-8");
            writer.close();
        }
        catch(IOException e1) {
            System.out.println("Error during reading/writing");
        }

        // Loading, sentence-segmenting and tokenizing the file using DocumentPreprocessor.
        TreebankLanguagePack tlp = lp.treebankLanguagePack();
        GrammaticalStructureFactory gsf = null;
        if (tlp.supportsGrammaticalStructures()) {
            gsf = tlp.grammaticalStructureFactory();
        }

        // Create a tokenizer and pass it to DocumentPreprocessor
        for (List<HasWord> sentence : new DocumentPreprocessor(input)) {
            Tree parse = lp.apply(sentence);

            GetNouns(parse, output);

            // Print sentence structure
            //parse.pennPrint();
        }
    }

    public static void main(String[] args) {
        // User can chose to manually assign model
        String input_file = (args.length > 2) ? args[1] : args[0];
        String output_file = (args.length > 2) ? args[2] : args[1];
        String parserModel = (args.length > 2) ? args[0] : "edu/stanford/nlp/models/lexparser/englishPCFG.ser.gz";

        LexicalizedParser lp = LexicalizedParser.loadModel(parserModel);
        demoDP(lp, input_file, output_file);

    }

}
