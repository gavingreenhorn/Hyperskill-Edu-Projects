package blockchain;

import java.nio.charset.StandardCharsets;
import java.util.Random;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.ThreadFactory;
import java.util.concurrent.TimeUnit;
import java.util.concurrent.atomic.AtomicInteger;

class MiningPool {
    private final int MAX_TRANSACTIONS_PER_BLOCK = 10;
    private final Orchestrator orchestrator;
    private volatile boolean proved;
    private final int poolSize;
    ExecutorService executor;

    MiningPool(Orchestrator orchestrator) {
        this.orchestrator = orchestrator;
        this.poolSize = Runtime.getRuntime().availableProcessors();
    }

    void mineABlock() throws InterruptedException {
        proved = false;
        this.executor = Executors.newFixedThreadPool(poolSize, new MinerFactory());
        for (int i = 0; i < poolSize; i++) {
            if (!executor.isShutdown())
                executor.execute(new Miner());
        }
        executor.awaitTermination(300, TimeUnit.SECONDS);
    }

    static class MinerFactory implements ThreadFactory {
        private final AtomicInteger threadNumber = new AtomicInteger(1);

        @Override
        public Thread newThread(Runnable r) {
            String namePrefix = "miner";
            return new Thread(r,namePrefix + threadNumber.getAndIncrement());
        }
    }

    class Miner implements Runnable {
        private final Random wezurd = new Random();
        Blockchain chain = orchestrator.getChain();

        private Block generateBlock() {
            BlockImpl candidateBlock = new BlockImpl(
                chain.getLastId(),
                wezurd.nextLong(),
                chain.getLastHash()
            );

            for (Transaction tx : chain.getPendingTransactions(MAX_TRANSACTIONS_PER_BLOCK)) {
                if (
                    CryptoUtils.verifySignature(
                        tx.getHash().getBytes(StandardCharsets.UTF_8),
                        tx.getSignature(),
                        chain.getRegisteredWallet(tx.getOriginatorAddress()).getPublicKey()
                    )
                ) {
                    Wallet sender = chain.getRegisteredWallet(tx.getOriginatorAddress());
                    Wallet recipient = chain.getRegisteredWallet(tx.getRecipientAddress());
                    if (sender == null || recipient == null) {
                        System.out.println("Rejected: unable to resolve transaction participants");
                        continue;
                    }
                    if (tx.getAmount() > sender.getAmount()) {
                        continue;
                    }
                    candidateBlock.addTransaction(tx);
                }
            }
            return candidateBlock;
        }

        private boolean trySubmit(Block block) {
            boolean result = orchestrator.acceptWorkCompletion(Thread.currentThread().getName(), block);
            if (result) proved = true;
            return result;
        }

        @Override
        public void run() {
            Thread thread = Thread.currentThread();
            orchestrator.acceptWorkRequest(thread.getName());
            Block candidateBlock;
            do {
                candidateBlock = generateBlock();
            }
            while (
                !proved &&
                !thread.isInterrupted()
                && !trySubmit(candidateBlock)
            );
            executor.shutdown();
        }
    }
}