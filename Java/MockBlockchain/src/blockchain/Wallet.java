package blockchain;

import java.security.PublicKey;

interface Wallet {
    String getAddress();
    long getAmount();
    PublicKey getPublicKey();
    Transaction generateTransaction(String targetWalletAddress, long amount);
    void setAmount(long newAmount);
}
