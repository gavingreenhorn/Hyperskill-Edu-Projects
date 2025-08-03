package blockchain;

import java.time.Instant;
import java.util.ArrayList;
import java.util.List;
import java.util.Objects;
import java.util.stream.Collectors;

class BlockImpl implements Block {
    private final long id;
    private final long timestamp;
    private final long magic;
    private final List<Transaction> transactions = new ArrayList<>();
    private final String previousHash;
    private String hash;

    BlockImpl(
        long id,
        long magic,
        String previousHash
    ) {
        this.id = id;
        this.magic = magic;
        this.previousHash = previousHash;
        this.timestamp = Instant.now().toEpochMilli();
    }

    public String getHash() {
        if (hash == null) {
            hash = CryptoUtils.applySha256(
                String.join("",
                    String.valueOf(id),
                    String.valueOf(timestamp),
                    String.valueOf(magic),
                    previousHash
                )
            );
        }
        return hash;
    }

    public String getPreviousHash() {
        return previousHash;
    }

    void addTransaction(Transaction transaction) {
        transactions.add(transaction);
    }

    @Override
    public List<Transaction> getBlockTransactions() {
        return List.copyOf(transactions);
    }

    @Override
    public String toString() {
        return new StringBuilder()
            .append("Id: %s\n".formatted(id))
            .append("Timestamp: %s\n".formatted(timestamp))
            .append("Magic number:%s\n".formatted(magic))
            .append("Hash of the previous block:\n%s\n".formatted(previousHash))
            .append("Hash of the block:\n%s\n".formatted(getHash()))
            .append("Block data:\n%s".formatted(
                transactions.isEmpty()
                    ? "Empty"
                    : transactions.stream()
                        .map(Objects::toString)
                        .collect(Collectors.joining("\n"))
                )
            )
            .toString();
    }

    @Override
    public boolean equals(Object other) {
        if (other == null) { return false; }
        if (other.getClass() != this.getClass()) { return false; }
        return this.getHash().equals(((Block)other).getHash());
    }
}
