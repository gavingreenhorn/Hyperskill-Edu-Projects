package SmartCalc;
import java.math.BigInteger;
import java.util.*;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

public class Utils {
    private static final String assignmentTemplate = "(?<LEFT>%s)\\s*?=\\s*?(?<RIGHT>%s)";
    private static final String operationsTemplate = "(%1$s)(\\s+?(%2$s)\\s+?(%1$s))*";
    private static final String tokenizerTemplate = "%1$s|%2$s|[()]";
    static final String operatorPattern = "[-+]+|[*/^]";
    static final String numberPattern = "[+-]?\\d+\\b";
    static final String variablePattern = "\\p{Alpha}+";
    static final String operandPattern = "(%s|%s)".formatted(numberPattern, variablePattern);
    static final String operationsPattern = operationsTemplate.formatted(operandPattern, operatorPattern);
    static final Pattern tokenizerPattern = Pattern.compile(
     tokenizerTemplate.formatted(operandPattern, operatorPattern));
    static final Pattern assignmentPattern = Pattern.compile(
     assignmentTemplate.formatted(variablePattern, operandPattern));
    static final HashMap<String, BigInteger> variableMap = new HashMap<String, BigInteger>();

    public static void AssignVariable(String assignmentExpression) {
        if (!assignmentExpression.split("=")[0].trim().matches(variablePattern)) {
            throw new IllegalArgumentException("Invalid identifier");
        }
        Matcher assignmentMatcher = assignmentPattern.matcher(assignmentExpression);
        if (assignmentExpression.replaceAll("[^=]", "").length() > 1 || !assignmentMatcher.find()) {
            throw new IllegalArgumentException("Invalid assignment");
        }
        variableMap.put(
                assignmentMatcher.group("LEFT"),
                ResolveOperand(assignmentMatcher.group("RIGHT"))
        );
    }

    public static BigInteger GetVariableValue(String name) {
        BigInteger value = variableMap.get(name);
        if (value == null) {
            throw new IllegalArgumentException("Unknown variable");
        }
        return value;
    }

    public static BigInteger ResolveOperand(String operandStr) {
        operandStr = operandStr.trim();
        if (!operandStr.matches(variablePattern)) {
            return new BigInteger(operandStr);
        }
        return GetVariableValue(operandStr);
    }

    public static boolean HasBalancedBrackets(String input) {
        if (!(input.contains("(") || input.contains(")"))) {
            return true;
        }
        Deque<String> deque = new ArrayDeque<>();
        Map<String, String> map = Map.of(
                ")","(",
                "}","{",
                "]","["
        );
        boolean isBalanced = true;
        for (String c : input.replaceAll("[^\\[\\](){}]", "").split("")) {
            if ("({[".contains(c)) {
                deque.push(c);
            }
            else {
                if (deque.isEmpty() || !map.get(c).equals(deque.pop())) {
                    isBalanced = false;
                    break;
                }
            }
        }
        return isBalanced && deque.isEmpty();
    }

    public static List<String> InfixToPostfixSequence(List<String> infixSequence) {
        List<String> postfixSequence = new ArrayList<>();
        Deque<String> stack = new ArrayDeque<>();
        for (String elem : infixSequence) {
            if (elem.matches(operandPattern)) {
                postfixSequence.add(elem);
            }
            else if (elem.matches(operatorPattern)) {
                Operator optr = Operator.fromString(elem);
                if (stack.isEmpty() || stack.peek().equals("(") || optr.lt(Operator.fromString(stack.peek()))) {
                    stack.push(elem);
                }
                else {
                    while (!stack.isEmpty() && !stack.peek().equals("(") && optr.gte(Operator.fromString(stack.peek()))) {
                        postfixSequence.add(stack.pop());
                    }
                    stack.push(elem);
                }
            }
            else if (elem.equals("(")) {
                stack.push(elem);
            }
            else if (elem.equals(")")) {
                while (!stack.isEmpty() && !stack.peek().equals("(")) {
                    postfixSequence.add(stack.pop());
                }
                stack.pop();
            }
        }
        while (!stack.isEmpty()) {
            postfixSequence.add(stack.pop());
        }
        return postfixSequence;
    }

    public static BigInteger CalculatePostfix(List<String> postfixSequence) {
        Deque<BigInteger> stack = new ArrayDeque<>();
        for (String elem : postfixSequence) {
            if (elem.matches(operandPattern)) {
                stack.push(ResolveOperand(elem));
            }
            else if (elem.matches(operatorPattern)) {
                var b = stack.pop();
                var a = stack.pop();
                stack.push(Operator.fromString(elem).apply(a, b));
            }
        }
        return stack.pop();
    }
}

