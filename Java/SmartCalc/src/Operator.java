package SmartCalc;
import static SmartCalc.Utils.*;
import java.math.BigInteger;
import java.util.Map;
import java.util.function.BinaryOperator;

public enum Operator {
    EXPONENTIATE(1, (a, b) -> a.pow(b.intValue())),
    MULTIPLY(2, BigInteger::multiply),
    DIVIDE(2, (a, b) -> {
        if (b.equals(BigInteger.ZERO)) throw new ArithmeticException("Division by zero");
        else return a.divide(b);
    }),
    ADD(3, BigInteger::add),
    SUBTRACT(3, BigInteger::subtract);

    private static final Map<Character, Operator> symbolMap = Map.of(
            '+', ADD,
            '-', SUBTRACT,
            '*', MULTIPLY,
            '/', DIVIDE,
            '^', EXPONENTIATE
    );
    private final int precedence;
    private final BinaryOperator<BigInteger> operation;

    Operator(int precedence, BinaryOperator<BigInteger> operation) {
        this.precedence = precedence;
        this.operation = operation;
    }

    public boolean eq(Operator other) {
        return this.precedence == other.precedence;
    }

    public boolean lt(Operator other) {
        return this.precedence < other.precedence;
    }

    public boolean gt(Operator other) {
        return this.precedence > other.precedence;
    }

    public boolean lte(Operator other) {
        return this.precedence <= other.precedence;
    }

    public boolean gte(Operator other) {
        return this.precedence >= other.precedence;
    }

    public BigInteger apply(BigInteger a, BigInteger b) { return operation.apply(a, b); }

    public static Operator fromString(String str) {
        if (!str.matches(operatorPattern)) {
            throw new IllegalArgumentException("Invalid operator expression");
        }
        char c = str.charAt(0);
        int l = str.length();
        if (l == 1) {
            return fromChar(c);
        }
        else {
            return fromChar(c == '-' && l % 2 == 0  ? '+' : c);
        }
    }

    public static Operator fromChar(char c) {
        return symbolMap.get(c);
    }
}
