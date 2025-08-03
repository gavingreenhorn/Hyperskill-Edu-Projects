package blockchain;

import java.util.List;

interface Block {
    String getHash();
    String getPreviousHash();
    List<Transaction> getBlockTransactions();
}