package blockchain;

public class Main {
    public static void main(String[] args) throws InterruptedException {
        Orchestrator orchestrator = Orchestrator.get();
        orchestrator.runSimulation();
    }
}

