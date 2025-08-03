package client;

import com.beust.jcommander.IParametersValidator;
import com.beust.jcommander.ParameterException;

import java.util.Map;
import java.util.Objects;

public class Validator implements IParametersValidator {
    @Override
    public void validate(Map<String, Object> parameters) throws ParameterException {
        if (parameters.get("-in") == null && parameters.get("--type") == null) {
            throw new ParameterException(
                "Arguments should have either -in or -t. Found: %s"
                .formatted(parameters.values().stream().filter(Objects::nonNull).toList()));
        }
        if (parameters.values().stream().filter(Objects::nonNull).count() > 1
            && parameters.get("-in") != null)
            throw new ParameterException(
                "Parameter -in can only be used on its own. Provided: %s"
                .formatted(parameters.values().stream().filter(Objects::nonNull).toList()));
        if (parameters.get("--type") != null) {
            String type = String.valueOf(parameters.get("--type"));
            if (
                !type.equals("exit")
                && parameters.get("--key") == null
            )
                throw new ParameterException(
                    "You must specify the parameter -k --key for this request. Provided: %s"
                    .formatted(parameters.values().stream().filter(Objects::nonNull).toList()));
            else if (
                !type.equals("set")
                && parameters.get("--value") != null
            )
                throw new ParameterException("Can only use -v --value parameter with 'set' request type");
            else if (
                type.equals("set")
                && parameters.get("--value") == null
            )
                throw new ParameterException("Cannot use 'set' request type without -v --v parameter");
        }
    }
}
