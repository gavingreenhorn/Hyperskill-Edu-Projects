package SmartCalc;
import static SmartCalc.Utils.*;
import java.util.*;
import java.util.regex.Matcher;

public class Main {
    private static void InvokeCommand(String commandName) {
        switch (commandName) {
            case "help":
                System.out.println("Much calculator, very smart");
                break;
            default:
                throw new IllegalArgumentException("Unknown command");

        }
    }

    public static void main(String[] args) {
        Scanner s = new Scanner(System.in);
        String input;
        while (!(input = s.nextLine()).equals("/exit")) {
            try {
                if (!input.isEmpty()) {
                    if (input.startsWith("/")) {
                        InvokeCommand(input.substring(1));
                    }
                    else if (input.matches("\\s*%s\\s*".formatted(operandPattern))) {
                        var oprnd = ResolveOperand(input);
                        System.out.print(oprnd);
                    }
                    else if (input.contains("=")) {
                        AssignVariable(input);
                    }
                    else if (
                            input.replaceAll("[()]", "").matches(operationsPattern)
                                    && HasBalancedBrackets(input)
                    ) {
                        Matcher matcher = tokenizerPattern.matcher(input);
                        List<String> tokens = new ArrayList<>();
                        while (matcher.find()) {
                            tokens.add(matcher.group());
                        }
                        var postfix = InfixToPostfixSequence(tokens);
                        System.out.println(CalculatePostfix(postfix));
                    }
                    else {
                        throw new InputMismatchException("Invalid expression");
                    }
                }
            }
            catch (RuntimeException ex) {
                System.out.println(ex.getMessage());
            }
        }
        System.out.println("Bye!");
    }
}