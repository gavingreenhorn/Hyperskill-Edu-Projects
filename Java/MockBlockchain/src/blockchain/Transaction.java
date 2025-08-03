package blockchain;

interface Transaction {

    String getOriginatorAddress();
    String getRecipientAddress();
    String getHash();
    byte[] getSignature();
    long getAmount();
}
