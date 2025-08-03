package blockchain;

import java.time.Instant;
import java.time.temporal.ChronoUnit;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

class Orchestrator {
    static private Orchestrator instance;
    private Blockchain chain;
    private MiningPool pool;
    private MockClients clients;
    Map<String, Instant> workRequestLog = new HashMap<>();

    private Orchestrator() {};

    static Orchestrator get() {
        if (instance == null) {
            instance = new Orchestrator();
            instance.chain = Blockchain.get();
            instance.pool = new MiningPool(instance);
            instance.clients = new MockClients();
        }
        return instance;
    }

    Blockchain getChain() {
        return chain;
    }

    MiningPool getPool() {
        return pool;
    }

    public void runSimulation() throws InterruptedException {
        int blocksCount = 15;
        int walletCount = 5;
        for (int i = 0; i < blocksCount; i++) {
            System.out.println("REQUESTING BLOCK %d\n".formatted(i + 1));
            List<Wallet> group1 = clients.generateMockWallets(walletCount);
            List<Wallet> group2 = clients.generateMockWallets(walletCount);
            group1.forEach(w -> chain.registerWallet(w));
            group2.forEach(w -> chain.registerWallet(w));
            for (int j = 0; j < walletCount; j++) {
                Wallet wallet1 = group1.get(j);
                Wallet wallet2 = group2.get(walletCount - 1 - j);
                chain.stageTransaction(wallet1.generateTransaction(wallet2.getAddress(), 20));
            }
            for (int j = 0; j < walletCount; j++) {
                Wallet wallet1 = group1.get(j);
                Wallet wallet2 = group2.get(walletCount - 1 - j);
                chain.stageTransaction(wallet2.generateTransaction(wallet1.getAddress(), 120));
            }
            getPool().mineABlock();
        }
    }

    synchronized void acceptWorkRequest(String minerName) {
        workRequestLog.put(minerName, Instant.now());
    }

    synchronized boolean acceptWorkCompletion(String minerName, Block block) {
        if (chain.acceptBlock(block)) {
            long completionTime = workRequestLog.get(minerName).until(Instant.now(), ChronoUnit.SECONDS);
            String difficultyMessage = chain.resolveDifficulty(completionTime);
            System.out.println(
                String.join(
                    "\n",
                    "Block: ",
                    "Created by %s".formatted(minerName),
                    "%s gets 100 VC".formatted(minerName),
                    block.toString(),
                    "Block was generating for %s seconds".formatted(completionTime),
                    difficultyMessage + "\n"
                )
            );
            return true;
        }
        return false;
    }
}