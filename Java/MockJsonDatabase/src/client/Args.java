package client;

import com.beust.jcommander.Parameter;
import com.beust.jcommander.Parameters;

@Parameters(parametersValidators = Validator.class)
public class Args {

    @Parameter(names = {"-t", "--type"}, description = "Request type")
    String type = null;

    @Parameter(names = {"-k", "--key"}, description = "A key to perform the chosen operation on")
    String key = null;

    @Parameter(names = {"-v", "--value"}, description = "Value to insert")
    String value = null;

    @Parameter(names = {"-in"}, description = "Path to a file with JSON payload")
    String in = null;
}
