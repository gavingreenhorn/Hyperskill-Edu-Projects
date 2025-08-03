package blockchain;

import java.util.*;
import java.util.concurrent.ConcurrentLinkedDeque;
import java.util.concurrent.atomic.AtomicInteger;
import java.util.stream.Collectors;

public class Blockchain {
    private static final String POW_OFFSET = "0";
    private static final int INITIAL_ID = 1;
    private static final int MEMPOOL_MAX_SIZE = 50;
    private final AtomicInteger lastId = new AtomicInteger(INITIAL_ID);
    private final Map<String, Wallet> registeredWallets = new HashMap<>();
    private final Deque<Transaction> mempool = new ConcurrentLinkedDeque<>();
    private final List<Block> chain = new ArrayList<>();
    private int difficulty = 0;
    private static Blockchain instance;

    private Blockchain() {}

    static Blockchain get() {
        if (instance == null) {
            instance = new Blockchain();
        }
        return instance;
    }

    int getLastId() {
        return lastId.get();
    }

    String getLastHash() {
        return chain.isEmpty() ? "0" : getHeadBlock().getHash();
    }

    String resolveDifficulty(long workDuration) {
        String message = "N stays the same";
        if (difficulty < 3 && workDuration < 10L) {
            difficulty++;
            message = "N was increased to %d".formatted(difficulty);
        }
        else if (workDuration > 60L) {
            difficulty--;
            message = "N was decreased by 1";
        }
        return message;
    }

    Block getHeadBlock() {
        return chain.getLast();
    }

    void registerWallet(Wallet wallet) {
        if (registeredWallets.containsKey(wallet.getAddress())) {
            throw new IllegalStateException("Rejected: Wallet is already registered");
        }
        if (registeredWallets.containsValue(wallet)) {
            throw new IllegalStateException("Rejected: Provided key is already associated with existing wallet");
        }
        registeredWallets.put(wallet.getAddress(), wallet);
    }

    Wallet getRegisteredWallet(String walletAddress) {
        if (!registeredWallets.containsKey(walletAddress)) {
            throw new IllegalStateException("The sender address is not registered");
        }
        return registeredWallets.get(walletAddress);
    }

    boolean stageTransaction(Transaction transaction) {
        if (mempool.size() >= MEMPOOL_MAX_SIZE) {
            return false;
        }
        return mempool.add(transaction);
    }

    private boolean unstageTransaction(Transaction transaction) {
        return mempool.remove(transaction);
    }

    List<Transaction> getPendingTransactions(int transactionCount) {
        return mempool.stream().limit(transactionCount).toList();
    }

    boolean acceptBlock(Block block) {
        if (isProved(block) && isValid(block)) {
            chain.add(block);
            lastId.incrementAndGet();
            for (Transaction tx : block.getBlockTransactions()) {
                unstageTransaction(tx);
                Wallet sender = getRegisteredWallet(tx.getOriginatorAddress());
                Wallet recipient = getRegisteredWallet(tx.getRecipientAddress());
                if (tx.getAmount() > sender.getAmount()) {
                    System.out.println("Rejected: not enough funds (%s < %s)".formatted(sender.getAmount(), tx.getAmount()));
                    continue;
                }
                sender.setAmount(sender.getAmount() - tx.getAmount());
                recipient.setAmount(recipient.getAmount() + tx.getAmount());
            }
            return true;
        }
        return false;
    }

    private boolean isProved(Block block) {
        return block.getHash().startsWith(POW_OFFSET.repeat(difficulty));
    }

    private boolean isValid(Block block) {
        if (chain.isEmpty() && block.getPreviousHash().equals("0")) {
            return true;
        }
        return getHeadBlock().getHash().equals(block.getPreviousHash());
    }

    @Override
    public String toString() {
        return chain.stream()
            .map(Block::toString)
            .collect((Collectors.joining("\n")));
    }
}
